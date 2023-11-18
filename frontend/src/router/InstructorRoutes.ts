import InstructorClassroom from '@/views/instructor/InstructorClassroom.vue'
import InstructorInvitationList from '@/views/instructor/InstructorInvitationList.vue'
import InstructorMyClassrooms from '@/views/instructor/InstructorMyClassrooms.vue'
import InstructorSendInvitation from '@/views/instructor/InstructorSendInvitation.vue'
import InstructorTask from '@/views/instructor/InstructorTask.vue'

export const instructorRoutes = [
  {
    path: '/instructor/classrooms/:classroomId',
    name: 'InstructorClassroom',
    component: InstructorClassroom,
    props: (route: any) => {
      return {
        classroomId: Number.parseInt(route.params.classroomId)
      }
    }
  },
  {
    path: '/instructor/classrooms/:classroomId/tasks/:taskId',
    name: 'InstructorTask',
    component: InstructorTask,
    props: (route: any) => {
      return {
        classroomId: Number.parseInt(route.params.classroomId),
        taskId: Number.parseInt(route.params.taskId)
      }
    }
  },
  {
    path: '/instructor/invitations',
    name: 'InstructorInvitationList',
    component: InstructorInvitationList
  },
  {
    path: '/instructor/invitations/send',
    name: 'InstructorSendInvitation',
    component: InstructorSendInvitation
  },
  {
    path: '/instructor/classrooms/my',
    name: 'InstructorMyClassrooms',
    component: InstructorMyClassrooms
  }
]
