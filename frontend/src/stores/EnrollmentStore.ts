import { makeAPIRequest } from '@/communication/APIRequests'
import type {ClassroomShort, HelpfulResource} from '@/stores/CatalogStore'
import type { User } from '@/stores/UserStore'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import {AcceptanceCriteriaType, QuestionType, TaskDifficulty, TaskType} from '@/stores/CatalogStore'
import {EnrollmentNotLoadedError} from '@/stores/exceptions'

export type EnrollmentShort = {
  id: number
  student: User
  date_enrolled: string
  classroom: ClassroomShort
  progress: number
}

type FlagStudent = {
  id: number
  prompt: string
  solution?: string
}

type RegExStudent = {
  id: number
  prompt: string
  solution?: string
}

type QuestionChoiceStudent = {
  id: number
  answer: string
  checked?: boolean
}

export type QuestionStudent = {
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

export type TaskStudent = {
  id: number
  title: string
  description: string
  done: boolean
  task_type: TaskType
  difficulty: TaskDifficulty
  acceptance_criteria: AcceptanceCriteriaStudent
}

type ProjectStudent = {
  id: number
  title: string
  tasks: TaskStudent[]
  progress: number
}

export type ClassroomStudent = {
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

export enum AcceptanceCriteriaSolutionResult {
  Correct = "correct",
  Incorrect = "incorrect",
  Missing = "missing"
}

type TaskSubmitResponse = {
  regexes: Record<number, AcceptanceCriteriaSolutionResult>
  flags: Record<number, AcceptanceCriteriaSolutionResult>
  questions: Record<number, AcceptanceCriteriaSolutionResult>
  passed: boolean
}

export const useEnrollmentStore = defineStore('invitation', () => {
  const myEnrollments = ref<[EnrollmentShort]>()
  const enrollment = ref<EnrollmentDetail>()

  async function getMyEnrollments() {
    const response = await makeAPIRequest('/enrollments/my', 'GET', true, true)
    myEnrollments.value = response.data
    return response.data as EnrollmentShort[]
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
    if(enrollment.value?.id !== enrollmentId) {
      enrollment.value = undefined
    }
    const response = await makeAPIRequest(`/enrollments/${enrollmentId}`, 'GET', true, true)
    enrollment.value = response.data as EnrollmentDetail
    return enrollment.value
  }

  function getTask(targetTaskId: number): TaskStudent | undefined {
    if(!enrollment.value) {
      throw new EnrollmentNotLoadedError('Cannot get task: No enrollment was loaded yet')
    }
    let targetTask
    enrollment.value.classroom.projects.forEach((project) => {
      project.tasks.forEach((task) => {
        if (task.id === targetTaskId) {
          targetTask = task
          return
        }
      })
    })
    return targetTask
  }

  async function submitSolution(task: TaskStudent) {
    if(!enrollment.value) {
      throw new EnrollmentNotLoadedError('Cannot submit solution: No enrollment was loaded yet')
    }

    const requestBody: {
      questions: {
        id: number,
        selected_choices: number[]
      }[],
      regexes: RegExStudent[],
      flags: FlagStudent[]
    } = {
      questions: [],
      regexes: (task.acceptance_criteria.regexes) ? task.acceptance_criteria.regexes : [],
      flags: (task.acceptance_criteria.flags) ? task.acceptance_criteria.flags : []
    }

    task.acceptance_criteria.questions?.forEach((question) => {
      requestBody.questions.push({
        id: question.id,
        selected_choices: question.choices.filter(choice => choice.checked).map(choice => choice.id)
      })
    })

    const response = await makeAPIRequest(
      `/enrollments/${enrollment.value.id}/tasks/${task.id}/submit`,
      'POST',
      true,
      true,
      requestBody
      )

    return response.data as TaskSubmitResponse
  }

  return {
    myEnrollments,
    enrollment,
    getMyEnrollments,
    enroll,
    unenroll,
    getEnrollment,
    getTask,
    submitSolution
  }
})