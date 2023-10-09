import { defineStore } from 'pinia'
import {ref, toRaw} from 'vue'
import { makeAPIRequest } from '@/communication/APIRequests'
import type { User } from "@/stores/UserStore"

type ClassroomShort = {
  id: number
  title: string
  created_at: string
  updated_at: string
}

export type Task = {
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

type HelpfulResource = {
  id?: number
  title: string
  url: string
}

type Project = {
  id?: number
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
    const response = await makeAPIRequest('/catalog/classrooms', 'GET', true, true)
    classroomList.value = response.data
    return response.data
  }

  async function createClassroom(title: string) {
    const data = {
      title: title
    }
    const response = await makeAPIRequest('/catalog/classrooms', 'POST', true, true, data)
    return response.data
  }

  async function getClassroom(id: number) {
    const response = await makeAPIRequest(`/catalog/classrooms/${id}`, 'GET', true, true)
    classroom.value = response.data
    return classroom.value
  }

  async function updateClassroom(id: number, classroomData: ClassroomDetail) {
    const response = await makeAPIRequest(
      `/catalog/classrooms/${id}`,
      'PUT',
      true,
      true,
      classroomData
    )
    classroom.value = response.data
    return classroom.value
  }

  async function deleteClassroom(id: number) {
    await makeAPIRequest(`/catalog/classrooms/${id}`, 'DELETE', true, true)
  }

  async function createProject(title: string) {
    if(classroom.value === undefined) {
      throw new ClassroomNotLoadedError("Cannot create project: No classroom was loaded yet")
    }
    const updatedClassroomData = Object.assign({}, toRaw(classroom.value))
    updatedClassroomData.projects.push({
      title: title,
      tasks: []
    })
    return updateClassroom(classroom.value.id, updatedClassroomData)
  }

  async function getTask(id: number) {
    return (await makeAPIRequest(`/catalog/tasks/${id}`, 'GET', true, true)).data
  }

  return {
    classroom,
    classroomList,
    getClassroomList,
    createClassroom,
    getClassroom,
    updateClassroom,
    deleteClassroom,
    createProject,
    getTask
  }
})