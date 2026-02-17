import os
import base64
import json
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
from pydantic import BaseModel
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Scranbook API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Auth dependency ---

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")
    token = authorization.removeprefix("Bearer ")
    try:
        user_resp = supabase.auth.get_user(token)
        return user_resp.user
    except Exception:
        raise HTTPException(401, "Invalid or expired token")


# --- Models ---

class IngredientIn(BaseModel):
    name: str
    amount: float
    unit: str


class RecipeSave(BaseModel):
    name: str
    ingredients: list[IngredientIn]
    steps: list[str]
    image_url: str | None = None


# --- Endpoints ---

@app.post("/api/parse-image")
async def parse_recipe_image(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(413, "Image must be under 10 MB")

    b64 = base64.b64encode(contents).decode("utf-8")
    media_type = file.content_type or "image/jpeg"

    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract recipes from images of recipe books. "
                    "Return ONLY valid JSON with this exact structure:\n"
                    '{"name": "Recipe Name", "ingredients": [{"name": "flour", "amount": 200, "unit": "g"}], "steps": ["Step 1...", "Step 2..."]}\n'
                    "Rules:\n"
                    "- amount must always be a number (convert fractions like 1/2 to 0.5)\n"
                    "- unit should be a standard short form (g, kg, ml, l, tsp, tbsp, cup, oz, lb, piece, pinch, clove, bunch, can, slice)\n"
                    "- If no unit applies use \"piece\"\n"
                    "- steps should be clear and ordered\n"
                    "- Return ONLY the JSON object, no markdown fences"
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the recipe from this image."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{media_type};base64,{b64}"},
                    },
                ],
            },
        ],
        max_tokens=2000,
        temperature=0.1,
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(502, "Failed to parse recipe from image — try a clearer photo")

    return parsed


@app.post("/api/upload-image")
async def upload_image(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    contents = await file.read()
    ext = (file.filename or "img.jpg").rsplit(".", 1)[-1]
    path = f"{user.id}/{os.urandom(8).hex()}.{ext}"

    supabase.storage.from_("recipe-images").upload(
        path, contents, {"content-type": file.content_type or "image/jpeg"}
    )
    public_url = supabase.storage.from_("recipe-images").get_public_url(path)
    return {"url": public_url}


@app.post("/api/recipes")
async def save_recipe(
    body: RecipeSave,
    user=Depends(get_current_user),
):
    recipe_row = (
        supabase.table("recipes")
        .insert(
            {
                "user_id": user.id,
                "name": body.name,
                "steps": body.steps,
                "image_url": body.image_url,
            }
        )
        .execute()
    )
    recipe_id = recipe_row.data[0]["id"]

    if body.ingredients:
        rows = [
            {
                "recipe_id": recipe_id,
                "name": ing.name,
                "amount": ing.amount,
                "unit": ing.unit,
                "sort_order": i,
            }
            for i, ing in enumerate(body.ingredients)
        ]
        supabase.table("ingredients").insert(rows).execute()

    return {"id": recipe_id}


@app.get("/api/recipes")
async def list_recipes(user=Depends(get_current_user)):
    result = (
        supabase.table("recipes")
        .select("*")
        .eq("user_id", user.id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data


@app.get("/api/recipes/{recipe_id}")
async def get_recipe(recipe_id: str, user=Depends(get_current_user)):
    recipe = (
        supabase.table("recipes")
        .select("*")
        .eq("id", recipe_id)
        .eq("user_id", user.id)
        .single()
        .execute()
    )
    if not recipe.data:
        raise HTTPException(404, "Recipe not found")

    ingredients = (
        supabase.table("ingredients")
        .select("*")
        .eq("recipe_id", recipe_id)
        .order("sort_order")
        .execute()
    )

    return {**recipe.data, "ingredients": ingredients.data}


@app.delete("/api/recipes/{recipe_id}")
async def delete_recipe(recipe_id: str, user=Depends(get_current_user)):
    supabase.table("recipes").delete().eq("id", recipe_id).eq(
        "user_id", user.id
    ).execute()
    return {"ok": True}
