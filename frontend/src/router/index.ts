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
import ManagerDashboard from '@/views/ManagerDashboard.vue'
import StudentAllClassrooms from '@/views/StudentAllClassrooms.vue'
import EditTaskTemplate from '@/views/EditTaskTemplate.vue'
import test from '@/views/test.vue'
import StudentClassrooms from '@/views/StudentClassrooms.vue'
import ModifyTemplate from '@/views/ModifyTemplate.vue'
import StudentClassProjects from '@/views/StudentClassProjects.vue'
import PrivacyPolicy from '@/views/PrivacyPolicy.vue'
import Imprint from '@/views/Imprint.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
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
      path: '/templates',
      name: 'ClassroomTemplates',
      component: ClassroomTemplates
    },
    {
      path: '/templates/:templateId',
      name: 'template',
      component: ModifyTemplate,
      props: true
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
      name: 'ManagerDashboard',
      component: ManagerDashboard
    },
    {
      path: '/edittasktemplate',
      name: 'EditTaskTemplate',
      component: EditTaskTemplate
    },
    {
      path: '/allclassrooms-stud', // TODO: change to allcllassrooms
      name: 'StudentAllClassrooms',
      component: StudentAllClassrooms
    },
    {
      path: '/test', // TODO: delete
      name: 'Test',
      component: test
    },
    {
      path: '/studentclassrooms',
      name: 'StudentClassrooms',
      component: StudentClassrooms
    },
    {
      path: '/studentclassprojects',
      name: 'StudentClassProjects',
      component: StudentClassProjects
    },
    {
      path: '/privacypolicy',
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
