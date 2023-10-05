import StudentClassroom from '@/views/student/StudentClassroom.vue'
import StudentAllClassrooms from '@/views/student/StudentAllClassrooms.vue'
import StudentMyClassrooms from '@/views/student/StudentMyClassrooms.vue'
import StudentDashboard from '@/views/student/StudentDashboard.vue'
import StudentTask from '@/views/student/StudentTask.vue'

export const studentRoutes = [
  {
    path: '/student/dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard
  },
  {
    path: '/student/classrooms',
    name: 'StudentMyClassrooms',
    component: StudentMyClassrooms
  },
  {
    path: '/student/classrooms/:classroomId',
    name: 'StudentClassroom',
    component: StudentClassroom
  },
  {
    path: '/student/classrooms/:classroomId/tasks/:taskId',
    name: 'StudentTask',
    component: StudentTask
  },
  {
    path: '/student/classrooms/all',
    name: 'StudentAllClassrooms',
    component: StudentAllClassrooms
  }
]
