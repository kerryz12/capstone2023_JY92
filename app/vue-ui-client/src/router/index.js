import { createRouter, createWebHistory } from 'vue-router'
import MainDash from '../views/MainDash.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'maindash',
      component: MainDash
    },
  ]
})

export default router