<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { supabase } from './lib/supabase'
import Navbar from './components/Navbar.vue'

const router = useRouter()
const route = useRoute()
const user = ref(null)

onMounted(() => {
  supabase.auth.getSession().then(({ data }) => {
    user.value = data.session?.user ?? null
  })
  supabase.auth.onAuthStateChange((_event, session) => {
    user.value = session?.user ?? null
  })
})

async function handleLogout() {
  await supabase.auth.signOut()
  router.push('/login')
}
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <Navbar v-if="user" :user="user" @logout="handleLogout" />
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>
