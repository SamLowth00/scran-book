-- ============================================
-- Scranbook database schema
-- Run this in the Supabase SQL Editor
-- ============================================

-- Recipes table
create table if not exists public.recipes (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id) on delete cascade not null,
  name text not null,
  steps text[] not null default '{}',
  image_url text,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- Ingredients table
create table if not exists public.ingredients (
  id uuid default gen_random_uuid() primary key,
  recipe_id uuid references public.recipes(id) on delete cascade not null,
  name text not null,
  amount numeric not null,
  unit text not null,
  sort_order integer default 0 not null
);

-- Indexes
create index if not exists idx_recipes_user_id on public.recipes(user_id);
create index if not exists idx_ingredients_recipe_id on public.ingredients(recipe_id);

-- Updated_at trigger
create or replace function public.set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger recipes_updated_at
  before update on public.recipes
  for each row execute function public.set_updated_at();

-- ============================================
-- Row Level Security
-- ============================================

alter table public.recipes enable row level security;
alter table public.ingredients enable row level security;

-- Recipes: users can only CRUD their own
create policy "Users can view own recipes"
  on public.recipes for select
  using (auth.uid() = user_id);

create policy "Users can insert own recipes"
  on public.recipes for insert
  with check (auth.uid() = user_id);

create policy "Users can update own recipes"
  on public.recipes for update
  using (auth.uid() = user_id);

create policy "Users can delete own recipes"
  on public.recipes for delete
  using (auth.uid() = user_id);

-- Ingredients: access scoped through recipe ownership
create policy "Users can view ingredients of own recipes"
  on public.ingredients for select
  using (recipe_id in (select id from public.recipes where user_id = auth.uid()));

create policy "Users can insert ingredients for own recipes"
  on public.ingredients for insert
  with check (recipe_id in (select id from public.recipes where user_id = auth.uid()));

create policy "Users can update ingredients of own recipes"
  on public.ingredients for update
  using (recipe_id in (select id from public.recipes where user_id = auth.uid()));

create policy "Users can delete ingredients of own recipes"
  on public.ingredients for delete
  using (recipe_id in (select id from public.recipes where user_id = auth.uid()));

-- ============================================
-- Storage bucket (run separately or via dashboard)
-- ============================================
-- Create a public bucket called "recipe-images" in the Supabase dashboard
-- under Storage, then add this policy:
--
-- insert policy: (auth.uid() is not null)
-- select policy: true  (public read)
