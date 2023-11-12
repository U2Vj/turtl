import StudentClassroom from '@/views/student/StudentClassroom.vue'
import StudentAllClassrooms from '@/views/student/StudentAllClassrooms.vue'
import StudentMyEnrollments from '@/views/student/StudentMyEnrollments.vue'
import StudentDashboard from '@/views/student/StudentDashboard.vue'
import StudentTask from '@/views/student/StudentTask.vue'

export const studentRoutes = [
  {
    path: '/student/dashboard',
    name: 'StudentDashboard',
    component: StudentDashboard
  },
  {
    path: '/student/enrollments',
    name: 'StudentMyEnrollments',
    component: StudentMyEnrollments
  },
  {
    path: '/student/enrollment/:enrollmentId',
    name: 'StudentClassroom',
    component: StudentClassroom,
    props: (route: any) => {
      return {
        enrollmentId: Number.parseInt(route.params.enrollmentId)
      }
    }
  },
  {
    path: '/student/enrollment/:enrollmentId/task/:taskId',
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
