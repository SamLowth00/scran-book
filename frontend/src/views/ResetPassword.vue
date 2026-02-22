<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'

const router = useRouter()
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const message = ref('')
const ready = ref(false)

onMounted(() => {
  supabase.auth.onAuthStateChange((event) => {
    if (event === 'PASSWORD_RECOVERY') {
      ready.value = true
    }
  })
})

async function handleReset() {
  error.value = ''
  message.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  loading.value = true

  try {
    const { error: err } = await supabase.auth.updateUser({
      password: password.value,
    })
    if (err) throw err
    message.value = 'Password updated successfully. Redirecting...'
    setTimeout(() => router.push('/'), 2000)
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
      <div class="text-center mb-10">
        <div class="text-5xl mb-3">&#x1F4D6;</div>
        <h1 class="font-display text-4xl text-ink mb-2">Scranbook</h1>
      </div>

      <div class="card p-8">
        <h2 class="font-display text-xl text-center mb-6">Reset password</h2>

        <div v-if="!ready" class="text-sm text-ink-light text-center">
          Loading...
        </div>

        <form v-else @submit.prevent="handleReset" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-ink-light uppercase tracking-wider mb-1.5">
              New password
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

          <div>
            <label class="block text-xs font-medium text-ink-light uppercase tracking-wider mb-1.5">
              Confirm password
            </label>
            <input
              v-model="confirmPassword"
              type="password"
              required
              minlength="6"
              class="input-field"
              placeholder="Repeat your new password"
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
            {{ loading ? 'Updating...' : 'Update password' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <button
            @click="router.push('/login')"
            class="text-sm text-ink-light hover:text-terracotta transition-colors"
          >
            Back to sign in
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
