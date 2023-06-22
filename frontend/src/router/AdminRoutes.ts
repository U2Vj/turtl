import AdminClassroomTemplatesOverview from '@/views/admin/AdminClassroomTemplatesOverview.vue'
import AdminTemplateClassroom from '@/views/admin/AdminTemplateClassroom.vue'

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
  }
]
