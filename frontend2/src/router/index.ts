import SignIn from '@/views/SignIn.vue'
import ClassroomEnroled from '@/views/ClassroomsEnroled.vue'
import ClassroomSingle from '@/views/ClassroomSingle.vue'
import ForgotPassword from '@/views/ForgotPassword.vue'
import ResetPassword from '@/views/ResetPassword.vue'
import Profile from '@/views/UserProfile.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/UserStore'
import ClassroomTemplates from '@/views/ClassroomTemplates.vue'
import CreateClassroomInstance from '@/views/CreateClassroomInstance.vue'
import DashboardStudent from '@/views/DashboardStudent.vue'
import InstructorDashboard from '@/views/InstructorDashboard.vue'

import EditTaskTemplate from '@/views/EditTaskTemplate.vue'

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
      path: '/reset-password',
      name: 'reset-password',
      component: ResetPassword
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile
    },
    {
      path: '/classroomtemplates',
      name: 'ClassroomTemplates',
      component: ClassroomTemplates
    },
    {
      path: '/createclassroominstance',
      name: 'CreateClassroomInstance',
      component: CreateClassroomInstance
    },
    {
      path: '/dashboard',
      name: 'Dashboard',
      component: DashboardStudent
    },
    {
      path: '/dashboard-prof', // TODO: change to /dashboard
      name: 'InstructorDashboard',
      component: InstructorDashboard
    },
    {
      path: '/edittasktemplate',
      name: 'EditTaskTemplate',
      component: EditTaskTemplate
    }
    /*
      component: () => {
      if (userGroup === 'instructor') {
         return InstructorDashboard
      } else if (userGroup === 'manager') {
          return ManagerDashboard
      } else {
          return StudentDashboard
      }
       */
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
