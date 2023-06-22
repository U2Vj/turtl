import SignIn from '@/views/general/SignIn.vue'
import StudentClassroomsEnroled from '@/views/student/StudentClassroomsEnroled.vue'
import StudentTask from '@/views/student/StudentTask.vue'
import PasswordRecovery from '@/views/general/PasswordRecovery.vue'
import PasswordChange from '@/views/general/PasswordChange.vue'
import UserProfile from '@/views/general/UserProfile.vue'
import AdminClassroomTemplatesOverview from '@/views/admin/AdminClassroomTemplatesOverview.vue'
import AdminTemplateClassroom from '@/views/admin/AdminTemplateClassroom.vue'
import StudentDashboard from '@/views/student/StudentDashboard.vue'
import ManagerClassrooms from '@/views/manager/ManagerClassrooms.vue'
import ManagerClassroomInstanceCreate from '@/views/manager/ManagerClassroomInstanceCreate.vue'
import StudentClassroomsAll from '@/views/student/StudentClassroomsAll.vue'
import StudentClassroom from '@/views/student/StudentClassroom.vue'
import PrivacyPolicy from '@/views/general/PrivacyPolicy.vue'
import ImprintTurtl from '@/views/general/ImprintTurtl.vue'

import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/UserStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/student/dashboard',
      name: 'StudentDashboard',
      component: StudentDashboard
    },
    {
      path: '/student/classrooms',
      name: 'StudentClassroomsEnroled',
      component: StudentClassroomsEnroled
    },
    {
      path: '/student/classrooms/:id',
      name: 'ClassroomSingle',
      component: StudentClassroom
    },
    {
      path: '/student/tasks/:id',
      name: 'StudentTask',
      component: StudentTask
    },
    {
      path: '/student/classrooms/all',
      name: 'StudentClassroomsAll',
      component: StudentClassroomsAll
    },
    {
      path: '/admin/templates',
      name: 'AdminClassroomTemplatesOverview',
      component: AdminClassroomTemplatesOverview
    },
    {
      path: '/admin/templates/:templateId',
      name: 'AdminTemplateClassroom',
      component: AdminTemplateClassroom,
      props: true
    },
    {
      path: '/manager/classrooms',
      name: 'ManagerClassrooms',
      component: ManagerClassrooms
    },
    {
      path: '/mananager/classroom/create',
      name: 'ManagerClassroomInstanceCreate',
      component: ManagerClassroomInstanceCreate
    },
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
