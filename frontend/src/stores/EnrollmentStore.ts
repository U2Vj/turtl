import {defineStore} from 'pinia'
import type {User} from '@/stores/UserStore'
import {ref} from 'vue/dist/vue'
import type {ClassroomShort} from '@/stores/CatalogStore'
import {makeAPIRequest} from '@/communication/APIRequests'

export type EnrollmentShort = {
  id: number
  student: User
  date_enrolled: string
  classroom: ClassroomShort
}

export const useEnrollmentStore = defineStore('invitation', () => {
  const myEnrollments = ref<[EnrollmentShort]>()

  async function getMyEnrollments() {
    const response = await makeAPIRequest('/enrollments/my', 'GET', true, true)
    myEnrollments.value = response.data
    return myEnrollments.value
  }

  async function enroll(classroomId: number) {
    const response = await makeAPIRequest(
      '/enrollments/my',
      'POST',
      true,
      true,
      {
        classroom: classroomId
      }
    )
    return response.data as EnrollmentShort
  }

  async function unenroll(enrollmentId: number) {
    await makeAPIRequest(`/enrollments/${id}`, 'DELETE', true, true)
  }

  return {
    myEnrollments,
    getMyEnrollments,
    enroll,
    unenroll
  }
})