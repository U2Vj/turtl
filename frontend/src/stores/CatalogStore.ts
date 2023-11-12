import { makeAPIRequest } from '@/communication/APIRequests'
import type { User } from '@/stores/UserStore'
import { ClassroomNotLoadedError } from '@/stores/exceptions'
import { defineStore } from 'pinia'
import { ref, toRaw } from 'vue'

export type ClassroomShort = {
  id: number
  title: string
  created_at: string
  updated_at: string
  instructors: User[]
}

export enum TaskType {
  Neutral = 'neutral',
  Attack = 'attack',
  Defense = 'defense'
}

export enum TaskDifficulty {
  Beginner = 'beginner',
  Intermediate = 'intermediate',
  Advanced = 'advanced'
}

export type Task = {
  id?: number
  title: string
  description: string
  task_type: TaskType
  difficulty: TaskDifficulty
  virtualizations: Virtualization[]
  acceptance_criteria: AcceptanceCriteria
}

export enum VirtualizationRole {
  UserShell = 'user_shell',
  UserAccessible = 'user_accessible'
}

export type Virtualization = {
  id?: number
  name: string
  virtualization_role: VirtualizationRole
  dockerfile: string
}

export enum AcceptanceCriteriaType {
  Disabled = 'disabled',
  Manual = 'manual',
  RegEx = 'regex',
  Flag = 'flag',
  Questionnaire = 'questionnaire',
  Mixed = 'mixed'
}

type AcceptanceCriteria = {
  id?: number
  criteria_type?: AcceptanceCriteriaType
  questions?: Question[]
  flags?: Flag[]
  regexes?: RegEx[]
}

export type Flag = {
  id?: number
  prompt: string
  value: string
}

export type RegEx = {
  id?: number
  prompt: string
  pattern: string
}

export enum QuestionType {
  SingleChoice = 'single_choice',
  MultipleChoice = 'multiple_choice'
}

export type Question = {
  id?: number
  question: string
  question_type: QuestionType
  choices: QuestionChoice[]
}

export type QuestionChoice = {
  id?: number
  answer: string
  is_correct: boolean
}

type ClassroomInstructor = {
  id?: number
  instructor: User
  added_at?: string
  added_by?: User
}

export type HelpfulResource = {
  id?: number
  title: string
  url: string
}

type Project = {
  id?: number
  title: string
  tasks: Task[]
}

export type ClassroomDetail = {
  id: number
  title: string
  created_at: string
  updated_at: string
  projects: Project[]
  helpful_resources: HelpfulResource[]
  instructors: ClassroomInstructor[]
}

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

  async function createTask(
    projectId: number,
    title: string,
    description: string,
    taskType: TaskType,
    difficulty: TaskDifficulty
  ) {
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot add task: No classroom was loaded yet')
    }
    const updatedClassroomData = Object.assign({}, toRaw(classroom.value))

    updatedClassroomData
        .projects
        .filter((project) => project.id == projectId)[0]
        .tasks
        .push({
          title: title,
          description: description,
          task_type: taskType,
          difficulty: difficulty,
          virtualizations: [],
          acceptance_criteria: {}
        })
    return updateClassroom(classroom.value.id, updatedClassroomData)
  }

  function getTask(targetId: number): Task | undefined {
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot get task: No classroom was loaded yet')
    }
    let targetTask
    classroom.value.projects.forEach((project) => {
      project.tasks.forEach((task) => {
        if (task.id === targetId) {
          targetTask = task
          return
        }
      })
    })
    return targetTask
  }

  async function updateTask(task: Task) {
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot get task: No classroom was loaded yet')
    }

    const updatedClassroomData = Object.assign({}, toRaw(classroom.value))
    updatedClassroomData.projects.forEach((project, projectIndex) => {
      project.tasks.forEach((t, tIndex) => {
        if (t.id === task.id) {
          if(classroom.value) {
            classroom.value.projects[projectIndex].tasks[tIndex] = task
          }
          return
        }
      })
    })

    return updateClassroom(classroom.value.id, updatedClassroomData)
  }

  async function deleteTask(taskIdToRemove: number) {
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot delete task: No classroom was loaded yet')
    }
    const updatedClassroomData = Object.assign({}, toRaw(classroom.value))

    updatedClassroomData.projects.forEach((project) => {
      project.tasks = project.tasks.filter((task) => task.id !== taskIdToRemove)
    })
    
    return updateClassroom(classroom.value.id, updatedClassroomData)
  }

  async function addInstructor(id: number) {
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot add instructor: No classroom was loaded yet')
    }
    const updatedClassroomData = Object.assign({}, toRaw(classroom.value))
    updatedClassroomData.instructors.push({
      instructor: {
        id: id
      }
    })
    return updateClassroom(classroom.value.id, updatedClassroomData)
  }

  async function removeInstructor(id: number) {
    if (classroom.value === undefined) {
      throw new ClassroomNotLoadedError('Cannot remove instructor: No classroom was loaded yet')
    }
    const updatedClassroomData = Object.assign({}, toRaw(classroom.value))
    updatedClassroomData.instructors = updatedClassroomData
        .instructors.filter(item => item.instructor.id !== id)
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
    createTask,
    getTask,
    updateTask,
    deleteTask,
    addInstructor,
    removeInstructor
  }
})
