import SignIn from '@/views/SignIn.vue'
import ClassroomEnroled from '@/views/ClassroomsEnroled.vue'
import ClassroomSingle from '@/views/ClassroomSingle.vue'
import ForgotPassword from '@/views/ForgotPassword.vue'
import Profile from '@/views/Profile.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/signin',
      name: 'signin',
      component: SignIn
    },
    {
      path: '/classrooms',
      name: 'ClassroomTable',
      component: ClassroomEnroled
    },
    {
      path: '/classrooms/:id',
      name: 'ClassroomSingle',
      component: ClassroomSingle
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPassword
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile
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
