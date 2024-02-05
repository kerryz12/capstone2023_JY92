import { createRouter, createWebHistory } from 'vue-router'
import MainDash from '../views/MainDash.vue'
import Login from '../views/Login.vue'

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
  ]
})
/*
router.beforeEach(function (to, from, next) {
  if ((to.path !== '/login' && to.path !== 'login')) {
    next({ path: '/login' })
  } else if ((to.path === '/login' || to.path === 'login')) {
    next({ path: '/' })
  } else {
   next()
  }
})
*/
export default router