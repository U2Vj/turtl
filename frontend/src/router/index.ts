import { useUserStore } from '@/stores/UserStore'
import AcceptInvitation from '@/views/general/AcceptInvitation.vue'
import Imprint from '@/views/general/Imprint.vue'
import PrivacyPolicy from '@/views/general/PrivacyPolicy.vue'
import SignIn from '@/views/general/SignIn.vue'
import UserProfile from '@/views/general/UserProfile.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { adminRoutes } from './AdminRoutes'
import { instructorRoutes } from './InstructorRoutes'
import { studentRoutes } from './StudentRoutes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...studentRoutes,
    ...instructorRoutes,
    ...adminRoutes,
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
      path: '/accept-invitation',
      name: 'AcceptInvitation',
      component: AcceptInvitation,
      beforeEnter: async () => {
        const userStore = useUserStore()
        if (await userStore.userIsSignedIn()) {
          await router.push('/profile')
        }
      }
    },
    {
      path: '/profile',
      name: 'UserProfile',
      component: UserProfile
    },
    {
      path: '/privacy-policy',
      name: 'PrivacyPolicy',
      component: PrivacyPolicy
    },
    {
      path: '/imprint',
      name: 'Imprint',
      component: Imprint
    }
  ]
})

// redirect to signin view if user is not signed in and route requires them to be logged in
router.beforeEach(async (to) => {
  const userStore = useUserStore()
  const allowedRouteNamesWhenNotSignedIn = ['signin', 'AcceptInvitation']
  if (
    !(await userStore.userIsSignedIn()) &&
    to.name &&
    !allowedRouteNamesWhenNotSignedIn.includes(to.name.toString())
  ) {
    return { name: 'signin' }
  }
})

export default router
