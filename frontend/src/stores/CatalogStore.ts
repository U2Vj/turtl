import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeAxiosRequest } from './AxiosInstance'
import axios from "axios";

type ClassroomShort = {
  id: number
  title: string
  created_at: string
  updated_at: string
}

type Task = {
  id: number
  title: string
  description: string
  difficulty: string
  type: string
  virtualization: Virtualization
  acceptance_criteria: AcceptanceCriteria
}

enum VirtualizationRole {
  UserShell = "User Shell",
  UserAccessible = "User-accessible via IP"
}

type Virtualization = {
  id: number
  name: string
  role: VirtualizationRole
  dockerfile: string
}

type AcceptanceCriteria = {
  acceptance_criteria_questionnaire?: Question[]
}

enum QuestionType {
  SingleChoice = "Single choice",
  MultipleChoice = "Multiple choice"
}

type Question = {
  id: number
  title: string
  type: QuestionType
  choices: QuestionChoice[]
}

type QuestionChoice = {
  answer: string
  is_correct: boolean
}

type ClassroomInstructor = {
  id?: number
  instructor: User
  added_at: string
  added_by: User
}

export type User = {
  id: number
  username: string | null
  email: string
}

type HelpfulResource = {
  id?: number
  title: string
  url: string
}

type Project = {
  id: number
  title: string
  tasks: Task[]
}

type AdditionalClassroomData = {
  projects: Project[]
  helpful_resources: HelpfulResource[]
  instructors: ClassroomInstructor[]
}

export type ClassroomDetail = ClassroomShort & AdditionalClassroomData

export const useCatalogStore = defineStore('catalog', () => {
  const classroom = ref<ClassroomDetail | undefined>()
  const classroomList = ref<ClassroomShort[]>()

  async function getClassroomList() {
    const response = await makeAxiosRequest('/catalog/classrooms', 'GET', true, true)
    if (response.success) {
      classroomList.value = response.data
    } else {
      console.error
    }
    return classroomList
  }

  async function createClassroom(title: string) {
    const data = {
      title: title
    }
    const response = await makeAxiosRequest('/catalog/classrooms', 'POST', true, true, data)
    if (response.success) {
      return { success: true, id: response.data.id }
    }
    return { success: false, id: null }
  }

  async function getClassroom(id: number) {
    const response = await makeAxiosRequest(`/catalog/classrooms/${id}`, 'GET', true, true)
    if (response.success) {
      classroom.value = response.data
    }
    return classroom
  }

  async function updateClassroom(id: number, classroomData: ClassroomDetail) {
    const response = await makeAxiosRequest(
      `/catalog/classrooms/${id}`,
      'PUT',
      true,
      true,
      classroomData
    )
    if (response.success) {
      classroom.value = response.data
    } else {
      // TODO: add notification
      console.error
    }
    return classroom
  }

  async function deleteClassroom(id: number) {
    const response = await makeAxiosRequest(`/catalog/classrooms/${id}`, 'DELETE', true, true)
    return response.success
  }

  async function getTask(id: number) {
    const response = await makeAxiosRequest(`/catalog/tasks/${id}`, 'GET', true, true)
    if (response.success) {
      return response.data
    }
    return undefined
  }

  return {
    classroom,
    classroomList,
    getClassroomList,
    createClassroom,
    getClassroom,
    updateClassroom,
    deleteClassroom,
    getTask
  }
})