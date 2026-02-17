<script setup>
import { useRoute } from 'vue-router'

defineProps(['user'])
defineEmits(['logout'])

const route = useRoute()
</script>

<template>
  <nav class="sticky top-0 z-50 bg-cream/80 backdrop-blur-md border-b border-ink/5">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <router-link to="/" class="flex items-center gap-2 group">
        <span class="text-2xl">&#x1F4D6;</span>
        <span class="font-display text-xl text-ink group-hover:text-terracotta transition-colors">
          Scranbook
        </span>
      </router-link>

      <div class="flex items-center gap-2 sm:gap-4">
        <router-link
          to="/scan"
          class="btn-primary text-sm !px-4 !py-2"
          :class="{ '!bg-terracotta-dark': route.path === '/scan' }"
        >
          <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          Scan
        </router-link>

        <button
          @click="$emit('logout')"
          class="text-sm text-ink-light hover:text-terracotta transition-colors px-2 py-1"
        >
          Sign out
        </button>
      </div>
    </div>
  </nav>
</template>
