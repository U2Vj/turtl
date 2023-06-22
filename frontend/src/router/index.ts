import SignIn from '@/views/general/SignIn.vue'
import PasswordRecovery from '@/views/general/PasswordRecovery.vue'
import PasswordChange from '@/views/general/PasswordChange.vue'
import UserProfile from '@/views/general/UserProfile.vue'
import PrivacyPolicy from '@/views/general/PrivacyPolicy.vue'
import ImprintTurtl from '@/views/general/ImprintTurtl.vue'

import { studentRoutes } from './StudentRoutes'
import { adminRoutes } from './AdminRoutes'
import { managerRoutes } from './ManagerRoutes'
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/UserStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    ...studentRoutes,
    ...adminRoutes,
    ...managerRoutes,
    {
      path: '/',
      component: SignIn
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignIn
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: PasswordRecovery
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: PasswordChange
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

router.beforeEach((to) => {
  const userStore = useUserStore()
  if (
    to.name !== 'signin' &&
    to.name !== 'forgot-password' &&
    to.name !== 'reset-password' &&
    !userStore.loggedIn
  ) {
    return { name: 'signin' }
  }
})

export default router
