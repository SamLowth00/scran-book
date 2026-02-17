<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'

const router = useRouter()
const email = ref('')
const password = ref('')
const isSignUp = ref(false)
const loading = ref(false)
const error = ref('')
const message = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  message.value = ''

  try {
    if (isSignUp.value) {
      const { error: err } = await supabase.auth.signUp({
        email: email.value,
        password: password.value,
      })
      if (err) throw err
      message.value = 'Check your email for a confirmation link.'
    } else {
      const { error: err } = await supabase.auth.signInWithPassword({
        email: email.value,
        password: password.value,
      })
      if (err) throw err
      router.push('/')
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="w-full max-w-sm">
      <!-- Brand -->
      <div class="text-center mb-10">
        <div class="text-5xl mb-3">&#x1F4D6;</div>
        <h1 class="font-display text-4xl text-ink mb-2">Scranbook</h1>
        <p class="text-ink-light text-sm tracking-wide">
          Your recipes, collected &amp; kept.
        </p>
      </div>

      <!-- Card -->
      <div class="card p-8">
        <h2 class="font-display text-xl text-center mb-6">
          {{ isSignUp ? 'Create account' : 'Welcome back' }}
        </h2>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-ink-light uppercase tracking-wider mb-1.5">
              Email
            </label>
            <input
              v-model="email"
              type="email"
              required
              class="input-field"
              placeholder="you@example.com"
            />
          </div>

          <div>
            <label class="block text-xs font-medium text-ink-light uppercase tracking-wider mb-1.5">
              Password
            </label>
            <input
              v-model="password"
              type="password"
              required
              minlength="6"
              class="input-field"
              placeholder="At least 6 characters"
            />
          </div>

          <div v-if="error" class="text-sm text-red-600 bg-red-50 rounded-lg px-3 py-2">
            {{ error }}
          </div>
          <div v-if="message" class="text-sm text-sage bg-sage/10 rounded-lg px-3 py-2">
            {{ message }}
          </div>

          <button type="submit" :disabled="loading" class="btn-primary w-full mt-2">
            <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
            </svg>
            {{ loading ? 'Please wait...' : (isSignUp ? 'Sign up' : 'Sign in') }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <button
            @click="isSignUp = !isSignUp; error = ''; message = ''"
            class="text-sm text-ink-light hover:text-terracotta transition-colors"
          >
            {{ isSignUp ? 'Already have an account? Sign in' : "Don't have an account? Sign up" }}
          </button>
        </div>
      </div>

      <p class="text-center text-xs text-ink-light/40 mt-8">
        Snap a recipe, keep it forever.
      </p>
    </div>
  </div>
</template>
