import { createRouter, createWebHistory } from 'vue-router'
import { supabase } from '../lib/supabase'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { guest: true },
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: () => import('../views/ResetPassword.vue'),
  },
  {
    path: '/',
    name: 'Recipes',
    component: () => import('../views/Recipes.vue'),
    meta: { auth: true },
  },
  {
    path: '/scan',
    name: 'Scan',
    component: () => import('../views/Scan.vue'),
    meta: { auth: true },
  },
  {
    path: '/recipe/:id',
    name: 'RecipeDetail',
    component: () => import('../views/RecipeDetail.vue'),
    meta: { auth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const { data } = await supabase.auth.getSession()
  const loggedIn = !!data.session

  if (to.meta.auth && !loggedIn) return '/login'
  if (to.meta.guest && loggedIn) return '/'
})

export default router
