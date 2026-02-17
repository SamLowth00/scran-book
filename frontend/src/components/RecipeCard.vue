<script setup>
defineProps(['recipe'])

function formatDate(d) {
  return new Date(d).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}
</script>

<template>
  <router-link
    :to="`/recipe/${recipe.id}`"
    class="card card-hover block overflow-hidden group"
  >
    <!-- Image -->
    <div class="aspect-[4/3] bg-parchment overflow-hidden">
      <img
        v-if="recipe.image_url"
        :src="recipe.image_url"
        :alt="recipe.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
      <div v-else class="w-full h-full flex items-center justify-center">
        <span class="text-4xl opacity-30">&#x1F372;</span>
      </div>
    </div>

    <!-- Info -->
    <div class="p-4">
      <h3 class="font-display text-lg text-ink leading-snug group-hover:text-terracotta transition-colors">
        {{ recipe.name }}
      </h3>
      <p class="text-xs text-ink-light/60 mt-2">
        {{ formatDate(recipe.created_at) }}
      </p>
    </div>
  </router-link>
</template>
