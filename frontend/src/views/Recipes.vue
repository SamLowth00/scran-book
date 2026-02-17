<script setup>
import { ref, onMounted } from 'vue'
import { fetchRecipes } from '../lib/api'
import RecipeCard from '../components/RecipeCard.vue'

const recipes = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    recipes.value = await fetchRecipes()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 py-8">
    <div class="flex items-end justify-between mb-8">
      <div>
        <h1 class="font-display text-3xl text-ink">Your recipes</h1>
        <p class="text-ink-light mt-1">{{ recipes.length }} recipe{{ recipes.length !== 1 ? 's' : '' }} saved</p>
      </div>
      <router-link to="/scan" class="btn-primary text-sm">
        <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add recipe
      </router-link>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <svg class="animate-spin h-6 w-6 text-terracotta" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
    </div>

    <!-- Empty state -->
    <div v-else-if="recipes.length === 0" class="text-center py-20">
      <div class="w-20 h-20 rounded-full bg-parchment flex items-center justify-center mx-auto mb-4">
        <span class="text-3xl">&#x1F373;</span>
      </div>
      <h2 class="font-display text-xl text-ink mb-2">No recipes yet</h2>
      <p class="text-ink-light text-sm mb-6">Scan your first recipe to get started.</p>
      <router-link to="/scan" class="btn-primary">Scan a recipe</router-link>
    </div>

    <!-- Grid -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <RecipeCard
        v-for="recipe in recipes"
        :key="recipe.id"
        :recipe="recipe"
      />
    </div>
  </div>
</template>
