import { supabase } from './supabase'

const API = import.meta.env.VITE_API_URL

async function authHeaders() {
  const { data } = await supabase.auth.getSession()
  return {
    Authorization: `Bearer ${data.session?.access_token}`,
  }
}

export async function parseRecipeImage(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API}/api/parse-image`, {
    method: 'POST',
    headers: await authHeaders(),
    body: form,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Failed to parse image')
  }
  return res.json()
}

export async function uploadImage(file) {
  const form = new FormData()
  form.append('file', file)
  const res = await fetch(`${API}/api/upload-image`, {
    method: 'POST',
    headers: await authHeaders(),
    body: form,
  })
  if (!res.ok) throw new Error('Failed to upload image')
  return res.json()
}

export async function saveRecipe(recipe) {
  const res = await fetch(`${API}/api/recipes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(await authHeaders()),
    },
    body: JSON.stringify(recipe),
  })
  if (!res.ok) throw new Error('Failed to save recipe')
  return res.json()
}

export async function fetchRecipes() {
  const res = await fetch(`${API}/api/recipes`, {
    headers: await authHeaders(),
  })
  if (!res.ok) throw new Error('Failed to fetch recipes')
  return res.json()
}

export async function fetchRecipe(id) {
  const res = await fetch(`${API}/api/recipes/${id}`, {
    headers: await authHeaders(),
  })
  if (!res.ok) throw new Error('Failed to fetch recipe')
  return res.json()
}

export async function deleteRecipe(id) {
  const res = await fetch(`${API}/api/recipes/${id}`, {
    method: 'DELETE',
    headers: await authHeaders(),
  })
  if (!res.ok) throw new Error('Failed to delete recipe')
  return res.json()
}
