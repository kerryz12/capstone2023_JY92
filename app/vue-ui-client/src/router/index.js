import { createRouter, createWebHistory } from 'vue-router'
import MainDash from '../views/MainDash.vue'
import BodyPositionVue from '@/components/BodyPosition.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'maindash',
      component: MainDash
    },
    {
      path: '/test',
      name: 'test',
      component: BodyPositionVue
    },

  ]
})

export default router