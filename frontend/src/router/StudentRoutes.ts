import StudentClassroomsEnroled from '@/views/student/StudentClassroomsEnroled.vue'
import StudentTask from '@/views/student/StudentTask.vue'
import StudentDashboard from '@/views/student/StudentDashboard.vue'
import StudentClassroomsAll from '@/views/student/StudentClassroomsAll.vue'
import StudentClassroom from '@/views/student/StudentClassroom.vue'

export const studentRoutes = [
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
  }
]
