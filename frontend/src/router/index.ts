import { instructorRoutes } from './InstructorRoutes'
import { studentRoutes } from './StudentRoutes'
import { useUserStore } from '@/stores/UserStore'
import ImprintTurtl from '@/views/general/ImprintTurtl.vue'
import PrivacyPolicy from '@/views/general/PrivacyPolicy.vue'
import SignIn from '@/views/general/SignIn.vue'
import UserProfile from '@/views/general/UserProfile.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...studentRoutes,
    ...instructorRoutes,
    {
      path: '/',
      component: SignIn,
      beforeEnter: async () => {
        const userStore = useUserStore()
        if (await userStore.userIsSignedIn()) {
          await router.push('/profile')
        }
      }
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignIn,
      beforeEnter: async () => {
        const userStore = useUserStore()
        if (await userStore.userIsSignedIn()) {
          await router.push('/profile')
        }
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: UserProfile
    },
    {
      path: '/privacypolicy',
      name: 'PrivacyPolicy',
      component: PrivacyPolicy
    },
    {
      path: '/imprint',
      name: 'Imprint',
      component: ImprintTurtl
    }
  ]
})

// redirect to signin view if user is not signed in and route requires them to be logged in
router.beforeEach(async (to) => {
  const userStore = useUserStore()
  const allowedRouteNamesWhenNotSignedIn = ['signin', 'forgot-password', 'reset-password']
  if (
    !(await userStore.userIsSignedIn()) &&
    to.name &&
    !allowedRouteNamesWhenNotSignedIn.includes(to.name.toString())
  ) {
    return { name: 'signin' }
  }
})

export default router
