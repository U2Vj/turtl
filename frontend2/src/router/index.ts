import Signin from '@/views/SignIn.vue'
import ForgotPassword from '@/views/ForgotPassword.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Signin
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPassword
    }
    /* ,
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    } */
  ]
})

export default router
