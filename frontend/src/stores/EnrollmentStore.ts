import { makeAPIRequest } from '@/communication/APIRequests'
import type {ClassroomShort, HelpfulResource} from '@/stores/CatalogStore'
import type { User } from '@/stores/UserStore'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import {AcceptanceCriteriaType, QuestionType, TaskDifficulty, TaskType} from '@/stores/CatalogStore'

export type EnrollmentShort = {
  id: number
  student: User
  date_enrolled: string
  classroom: ClassroomShort
}

type FlagStudent = {
  id: number
  prompt: string
}

type RegExStudent = {
  id: number
  prompt: string
}

type QuestionChoiceStudent = {
  id: number
  answer: string
}

type QuestionStudent = {
  id: number
  question: string
  question_type: QuestionType
  choices: QuestionChoiceStudent[]
}

type AcceptanceCriteriaStudent = {
  id: number
  criteria_type: AcceptanceCriteriaType
  questions?: QuestionStudent[]
  flags?: FlagStudent[]
  regexes?: RegExStudent[]
}

type TaskStudent = {
  id: number
  title: string
  description: string
  task_type: TaskType
  difficulty: TaskDifficulty
  acceptance_criteria: AcceptanceCriteriaStudent
}

type ProjectStudent = {
  id: number
  title: string
  tasks: TaskStudent[]
}

type ClassroomStudent = {
  id: number
  title: string
  created_at: string
  updated_at: string
  projects: ProjectStudent[]
  helpful_resources: HelpfulResource[]
  instructors: User[]
}

export type EnrollmentDetail = {
  id: number
  student: User
  date_enrolled: string
  classroom: ClassroomStudent
}

export const useEnrollmentStore = defineStore('invitation', () => {
  const myEnrollments = ref<[EnrollmentShort]>()
  const enrollment = ref<EnrollmentDetail>()

  async function getMyEnrollments() {
    const response = await makeAPIRequest('/enrollments/my', 'GET', true, true)
    myEnrollments.value = response.data
    return myEnrollments.value
  }

  async function enroll(classroomId: number) {
    const response = await makeAPIRequest('/enrollments/my', 'POST', true, true, {
      classroom: classroomId
    })
    return response.data as EnrollmentShort
  }

  async function unenroll(enrollmentId: number) {
    await makeAPIRequest(`/enrollments/${enrollmentId}`, 'DELETE', true, true)
  }

  async function getEnrollment(enrollmentId: number) {
    const response = await makeAPIRequest(`/enrollments/${enrollmentId}`, 'GET', true, true)
    enrollment.value = response.data as EnrollmentDetail
    return enrollment.value
  }

  return {
    myEnrollments,
    enrollment,
    getMyEnrollments,
    enroll,
    unenroll,
    getEnrollment
  }
})
