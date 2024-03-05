import { createRouter, createWebHistory } from 'vue-router'
import MainDash from '../views/MainDash.vue'
import Login from '../views/Login.vue'
import alert from '@/components/alerts/alert.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'maindash',
      component: MainDash
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/alert',
      name: 'alert',
      component: alert
    },
  ]
})

export default router