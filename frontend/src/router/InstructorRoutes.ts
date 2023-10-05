import InstructorClassroomList from '@/views/instructor/InstructorClassroomList.vue'
import InstructorClassroom from '@/views/instructor/InstructorClassroom.vue'
import InstructorTask from '@/views/instructor/InstructorTask.vue'

export const instructorRoutes = [
  {
    path: '/instructor/classrooms',
    name: 'InstructorClassroomList',
    component: InstructorClassroomList
  },
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
      console.log(route)
      return {
        classroomId: Number.parseInt(route.params.classroomId),
        taskId: Number.parseInt(route.params.taskId)
      }
    }
  }
]
