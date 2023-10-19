import { makeAPIRequest } from '@/communication/APIRequests'
import type { User } from '@/stores/UserStore'
import { ClassroomNotLoadedError } from '@/stores/exceptions'
import { defineStore } from 'pinia'
import { ref, toRaw } from 'vue'

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
  task_type: string
  difficulty: string
  virtualization: Virtualization
  acceptance_criteria: AcceptanceCriteria
}

enum VirtualizationRole {
  UserShell = 'User Shell',
  UserAccessible = 'User-accessible via IP'
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
  SingleChoice = 'Single choice',
  MultipleChoice = 'Multiple choice'
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
  const project = ref<Project | undefined>()

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
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot create project: No classroom was loaded yet')
    }
    const updatedClassroomData = Object.assign({}, toRaw(classroom.value))
    updatedClassroomData.projects.push({
      title: title,
      tasks: []
    })
    return updateClassroom(classroom.value.id, updatedClassroomData)
  }

  async function deleteProject(idToRemove: number) {
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot delete project: No classroom was loaded yet')
    }
    const updatedClassroomData = Object.assign({}, toRaw(classroom.value))
    updatedClassroomData.projects = updatedClassroomData.projects.filter(
      (project) => project.id !== idToRemove
    )
    return updateClassroom(classroom.value.id, updatedClassroomData)
  }

  function getTask(targetId: number) {
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot get task: No classroom was loaded yet')
    }
    let targetTask
    classroom.value.projects.forEach((project) => {
      project.tasks.forEach((task) => {
        if (task.id === targetId) {
          targetTask = task
        }
      })
    })
    return targetTask
  }

  async function createTask(
    projectId: number,
    title: string,
    description: string,
    task_type: string,
    difficulty: string
  ) {
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot get task: No classroom was loaded yet')
    }
    let newTask
    const updatedClassroomData = Object.assign({}, toRaw(classroom.value))

    newTask = { title, description, task_type, difficulty }
    updatedClassroomData.projects.forEach((project) => {
      if (project.id === projectId) {
        project.tasks.push({
          id: 1,
          title: title,
          description: description,
          task_type: task_type,
          difficulty: difficulty,
          virtualization: [],
          acceptance_criteria: {}
        })
      }
    })
    return updateClassroom(classroom.value.id, updatedClassroomData)
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
    deleteProject,
    getTask,
    createTask
  }
})
