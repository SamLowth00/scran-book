<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { parseRecipeImage, uploadImage, saveRecipe } from '../lib/api'

const router = useRouter()

const file = ref(null)
const preview = ref(null)
const dragging = ref(false)
const parsing = ref(false)
const saving = ref(false)
const error = ref('')
const parsed = ref(null)

function handleFile(f) {
  if (!f || !f.type.startsWith('image/')) return
  file.value = f
  preview.value = URL.createObjectURL(f)
  parsed.value = null
  error.value = ''
}

function onDrop(e) {
  dragging.value = false
  const f = e.dataTransfer?.files?.[0]
  if (f) handleFile(f)
}

function onFileInput(e) {
  const f = e.target.files?.[0]
  if (f) handleFile(f)
}

async function handleParse() {
  if (!file.value) return
  parsing.value = true
  error.value = ''
  try {
    parsed.value = await parseRecipeImage(file.value)
  } catch (err) {
    error.value = err.message
  } finally {
    parsing.value = false
  }
}

function removeIngredient(index) {
  parsed.value.ingredients.splice(index, 1)
}

function addIngredient() {
  parsed.value.ingredients.push({ name: '', amount: 0, unit: 'piece' })
}

function removeStep(index) {
  parsed.value.steps.splice(index, 1)
}

function addStep() {
  parsed.value.steps.push('')
}

async function handleSave() {
  if (!parsed.value) return
  saving.value = true
  error.value = ''
  try {
    let imageUrl = null
    if (file.value) {
      const { url } = await uploadImage(file.value)
      imageUrl = url
    }
    await saveRecipe({
      name: parsed.value.name,
      ingredients: parsed.value.ingredients,
      steps: parsed.value.steps,
      image_url: imageUrl,
    })
    router.push('/')
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}

function reset() {
  file.value = null
  preview.value = null
  parsed.value = null
  error.value = ''
}
</script>

<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-8">
      <h1 class="font-display text-3xl text-ink">Scan a recipe</h1>
      <p class="text-ink-light mt-1">Snap or upload a photo from your recipe book.</p>
    </div>

    <!-- Upload zone -->
    <div v-if="!parsed" class="space-y-6">
      <div
        @dragover.prevent="dragging = true"
        @dragleave="dragging = false"
        @drop.prevent="onDrop"
        :class="[
          'card relative flex flex-col items-center justify-center p-12 border-2 border-dashed cursor-pointer transition-all',
          dragging ? 'border-terracotta bg-terracotta/5' : 'border-ink/10 hover:border-ink/20',
          preview ? '!p-4' : ''
        ]"
        @click="$refs.fileInput.click()"
      >
        <input ref="fileInput" type="file" accept="image/*" capture="environment" class="hidden" @change="onFileInput" />

        <template v-if="!preview">
          <div class="w-16 h-16 rounded-full bg-parchment flex items-center justify-center mb-4">
            <svg class="w-7 h-7 text-ink-light" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <p class="text-ink-light text-sm text-center">
            <span class="text-terracotta font-medium">Click to upload</span>
            or drag &amp; drop
          </p>
          <p class="text-ink-light/50 text-xs mt-1">PNG, JPG up to 10 MB</p>
        </template>

        <template v-else>
          <img :src="preview" alt="Recipe preview" class="max-h-80 rounded-lg object-contain" />
        </template>
      </div>

      <div v-if="preview" class="flex gap-3">
        <button @click="handleParse" :disabled="parsing" class="btn-primary flex-1">
          <svg v-if="parsing" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ parsing ? 'Reading recipe...' : 'Extract recipe' }}
        </button>
        <button @click="reset" class="btn-secondary">Change photo</button>
      </div>

      <div v-if="error" class="text-sm text-red-600 bg-red-50 rounded-lg px-4 py-3">
        {{ error }}
      </div>
    </div>

    <!-- Parsed result for editing -->
    <div v-if="parsed" class="space-y-8">
      <div class="flex items-start gap-4">
        <img v-if="preview" :src="preview" alt="" class="w-24 h-24 rounded-lg object-cover flex-shrink-0" />
        <div class="flex-1">
          <label class="block text-xs font-medium text-ink-light uppercase tracking-wider mb-1.5">
            Recipe name
          </label>
          <input v-model="parsed.name" class="input-field text-lg font-display" />
        </div>
      </div>

      <!-- Ingredients -->
      <div>
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-display text-xl">Ingredients</h2>
          <button @click="addIngredient" class="text-sm text-terracotta hover:text-terracotta-dark transition-colors">
            + Add
          </button>
        </div>
        <div class="space-y-2">
          <div
            v-for="(ing, i) in parsed.ingredients"
            :key="i"
            class="flex items-center gap-2 group"
          >
            <input
              v-model.number="ing.amount"
              type="number"
              step="any"
              min="0"
              class="input-field w-20 text-center"
            />
            <input
              v-model="ing.unit"
              class="input-field w-20 text-center"
              placeholder="unit"
            />
            <input
              v-model="ing.name"
              class="input-field flex-1"
              placeholder="Ingredient"
            />
            <button
              @click="removeIngredient(i)"
              class="opacity-0 group-hover:opacity-100 text-ink-light hover:text-red-500 transition-all p-1"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Steps -->
      <div>
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-display text-xl">Steps</h2>
          <button @click="addStep" class="text-sm text-terracotta hover:text-terracotta-dark transition-colors">
            + Add
          </button>
        </div>
        <div class="space-y-2">
          <div
            v-for="(step, i) in parsed.steps"
            :key="i"
            class="flex items-start gap-3 group"
          >
            <span class="flex-shrink-0 w-7 h-7 rounded-full bg-parchment text-ink-light text-xs font-medium flex items-center justify-center mt-2">
              {{ i + 1 }}
            </span>
            <textarea
              v-model="parsed.steps[i]"
              rows="2"
              class="input-field flex-1 resize-none"
            />
            <button
              @click="removeStep(i)"
              class="opacity-0 group-hover:opacity-100 text-ink-light hover:text-red-500 transition-all p-1 mt-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-3 pt-4 border-t border-ink/5">
        <button @click="handleSave" :disabled="saving" class="btn-primary flex-1">
          <svg v-if="saving" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          {{ saving ? 'Saving...' : 'Save to Scranbook' }}
        </button>
        <button @click="reset" class="btn-secondary">Start over</button>
      </div>

      <div v-if="error" class="text-sm text-red-600 bg-red-50 rounded-lg px-4 py-3">
        {{ error }}
      </div>
    </div>
  </div>
</template>
