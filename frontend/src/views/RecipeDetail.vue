<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchRecipe, deleteRecipe } from '../lib/api'

const route = useRoute()
const router = useRouter()

const recipe = ref(null)
const loading = ref(true)
const servings = ref(1)
const baseServings = ref(1)
const confirmDelete = ref(false)

const scale = computed(() => servings.value / baseServings.value)

function scaledAmount(amount) {
  const val = amount * scale.value
  return val % 1 === 0 ? val : val.toFixed(1)
}

onMounted(async () => {
  try {
    recipe.value = await fetchRecipe(route.params.id)
  } catch {
    router.push('/')
  } finally {
    loading.value = false
  }
})

async function handleDelete() {
  await deleteRecipe(route.params.id)
  router.push('/')
}

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  })
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 py-8">
    <!-- Loading -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <svg class="animate-spin h-6 w-6 text-terracotta" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
      </svg>
    </div>

    <template v-else-if="recipe">
      <!-- Back link -->
      <router-link to="/" class="inline-flex items-center text-sm text-ink-light hover:text-terracotta transition-colors mb-6">
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        All recipes
      </router-link>

      <!-- Hero image -->
      <div v-if="recipe.image_url" class="rounded-xl overflow-hidden mb-8 shadow-warm-lg">
        <img :src="recipe.image_url" :alt="recipe.name" class="w-full max-h-96 object-cover" />
      </div>

      <!-- Header -->
      <div class="mb-8">
        <h1 class="font-display text-3xl sm:text-4xl text-ink leading-tight">{{ recipe.name }}</h1>
        <p class="text-sm text-ink-light/60 mt-2">Saved {{ formatDate(recipe.created_at) }}</p>
      </div>

      <!-- Serving adjuster -->
      <div class="card p-4 mb-8 flex items-center gap-4 flex-wrap">
        <span class="text-sm font-medium text-ink-light uppercase tracking-wider">Servings</span>
        <div class="flex items-center gap-2">
          <button
            @click="servings = Math.max(1, servings - 1)"
            class="w-8 h-8 rounded-full bg-parchment hover:bg-ink/5 flex items-center justify-center transition-colors text-ink"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
            </svg>
          </button>
          <input
            v-model.number="servings"
            type="number"
            min="1"
            max="100"
            class="w-14 text-center font-display text-xl bg-transparent border-none outline-none text-ink"
          />
          <button
            @click="servings++"
            class="w-8 h-8 rounded-full bg-parchment hover:bg-ink/5 flex items-center justify-center transition-colors text-ink"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
          </button>
        </div>
        <span v-if="scale !== 1" class="text-xs text-terracotta font-medium">
          ({{ scale > 1 ? scale.toFixed(1) + 'x' : scale.toFixed(1) + 'x' }})
        </span>
      </div>

      <!-- Ingredients -->
      <div class="mb-10">
        <h2 class="font-display text-2xl mb-4">Ingredients</h2>
        <div class="card divide-y divide-ink/5">
          <div
            v-for="(ing, i) in recipe.ingredients"
            :key="i"
            class="flex items-center px-5 py-3"
          >
            <span class="font-display text-lg text-terracotta w-16 text-right mr-3">
              {{ scaledAmount(ing.amount) }}
            </span>
            <span class="text-ink-light text-sm w-12">{{ ing.unit }}</span>
            <span class="text-ink">{{ ing.name }}</span>
          </div>
        </div>
      </div>

      <!-- Steps -->
      <div class="mb-10">
        <h2 class="font-display text-2xl mb-4">Method</h2>
        <ol class="space-y-4">
          <li
            v-for="(step, i) in recipe.steps"
            :key="i"
            class="flex gap-4"
          >
            <span class="flex-shrink-0 w-8 h-8 rounded-full bg-terracotta text-cream text-sm font-medium flex items-center justify-center mt-0.5">
              {{ i + 1 }}
            </span>
            <p class="text-ink leading-relaxed pt-1">{{ step }}</p>
          </li>
        </ol>
      </div>

      <!-- Delete -->
      <div class="border-t border-ink/5 pt-6">
        <template v-if="!confirmDelete">
          <button
            @click="confirmDelete = true"
            class="text-sm text-ink-light/40 hover:text-red-500 transition-colors"
          >
            Delete this recipe
          </button>
        </template>
        <template v-else>
          <div class="flex items-center gap-3">
            <span class="text-sm text-red-600">Are you sure?</span>
            <button @click="handleDelete" class="text-sm text-red-600 font-medium hover:underline">
              Yes, delete
            </button>
            <button @click="confirmDelete = false" class="text-sm text-ink-light hover:text-ink">
              Cancel
            </button>
          </div>
        </template>
      </div>
    </template>
  </div>
</template>
