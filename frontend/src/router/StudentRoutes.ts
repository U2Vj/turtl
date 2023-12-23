import StudentAllClassrooms from '@/views/student/StudentAllClassrooms.vue'
import StudentClassroom from '@/views/student/StudentClassroom.vue'
import StudentMyEnrollments from '@/views/student/StudentMyEnrollments.vue'
import StudentTask from '@/views/student/StudentTask.vue'

export const studentRoutes = [
  {
    path: '/student/enrollments',
    name: 'StudentMyEnrollments',
    component: StudentMyEnrollments
  },
  {
    path: '/student/enrollments/:enrollmentId',
    name: 'StudentClassroom',
    component: StudentClassroom,
    props: (route: any) => {
      return {
        enrollmentId: Number.parseInt(route.params.enrollmentId)
      }
    }
  },
  {
    path: '/student/enrollments/:enrollmentId/tasks/:taskId',
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
