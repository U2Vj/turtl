import AdminClassroomTemplatesOverview from '@/views/admin/AdminClassroomTemplatesOverview.vue'
import AdminTemplateClassroom from '@/views/admin/AdminTemplateClassroom.vue'
import AdminTemplateTask from '@/views/admin/AdminTemplateTask.vue'

export const adminRoutes = [
  {
    path: '/admin/templates',
    name: 'AdminClassroomTemplatesOverview',
    component: AdminClassroomTemplatesOverview
  },
  {
    path: '/admin/templates/:templateId',
    name: 'AdminTemplateClassroom',
    component: AdminTemplateClassroom,
    props: true
  },
  {
    path: '/admin/templates/:templateId/tasks/:taskId',
    name: 'AdminTemplateTask',
    component: AdminTemplateTask,
    props: true
  }
]
