import AdminAllClassrooms from '@/views/admin/AdminAllClassrooms.vue'
import NotFound from '@/views/general/NotFound.vue'

export const adminRoutes = [
  {
    path: '/admin/classrooms/all',
    name: 'AdminAllClassrooms',
    component: AdminAllClassrooms
  },
  {
    path: '/admin/:pathMatch(.*)*',
    name: 'AdminNotFound',
    component: NotFound
  }
]
