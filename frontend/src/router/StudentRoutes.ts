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
    path: '/student/classrooms/:enrollmentId',
    name: 'StudentClassroom',
    component: StudentClassroom,
    props: (route: any) => {
      return {
        enrollmentId: Number.parseInt(route.params.enrollmentId)
      }
    }
  },
  {
    path: '/student/classrooms/:enrollmentId/tasks/:taskId',
    name: 'StudentTask',
    component: StudentTask,
    props: (route: any) => {
      return {
        enrollmentId: Number.parseInt(route.params.enrollmentId),
        taskId: Number.parseInt(route.params.taskId)
      }
    }
  },
  {
    path: '/student/classrooms/all',
    name: 'StudentAllClassrooms',
    component: StudentAllClassrooms
  }
]
