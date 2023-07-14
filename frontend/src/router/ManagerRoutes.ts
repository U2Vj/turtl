import ManagerClassroomInstanceCreate from '@/views/manager/ManagerClassroomInstanceCreate.vue'
import ManagerClassrooms from '@/views/manager/ManagerClassrooms.vue'

export const managerRoutes = [
  {
    path: '/manager/classrooms',
    name: 'ManagerClassrooms',
    component: ManagerClassrooms
  },
  {
    path: '/mananager/classroom/create',
    name: 'ManagerClassroomInstanceCreate',
    component: ManagerClassroomInstanceCreate
  }
]
