import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useCloned } from '@vueuse/core'

type BasicTemplateData = {
  templateId: string
  templateName: string
  creationDate: string
}

type Task = { id: string; name: string }

export type Instructor = { instructorId: string; email: string }

type AdditionalTemplateData = {
  projects: {
    id: string
    name: string
    tasks: Task[]
  }[]
  resources: { id: string; name: string; link: string }[]
  instructors: Instructor[]
}

export type TemplateData = BasicTemplateData & AdditionalTemplateData

export const useTemplateStore = defineStore('template', () => {
  const classroomTemplate = ref<TemplateData>()
  const basicTemplateData = ref<BasicTemplateData[]>()

  async function fetchTemplate(templateId: string) {
    classroomTemplate.value = mockdata
    classroomTemplate.value = await axios.get(
      `${import.meta.env.VITE_API_URL}/templates/${templateId}`
    )

    return classroomTemplate
  }

  async function changeTemplateData(templateId: string, templateData: TemplateData) {
    classroomTemplate.value = await axios.post(
      `${import.meta.env.VITE_API_URL}/templates/${templateId}`,
      templateData
    )
    return classroomTemplate
  }

  async function deleteClassroomTemplate(templateId: string) {
    await axios.delete(`${import.meta.env.VITE_API_URL}/templates/${templateId}`)
  }

  async function getBasicTemplateData() {
    basicTemplateData.value = await axios.get(`${import.meta.env.VITE_API_URL}/templates`)
    return basicTemplateData
  }

  async function createProjectTemplate(projectName: string) {
    classroomTemplate.value = await axios.put(
      `${import.meta.env.VITE_API_URL}/templates`,
      projectName
    )
  }

  async function addInstructor(instructorId: string, email: string) {
    const { cloned } = useCloned(classroomTemplate)
    cloned.value?.instructors.push({ instructorId, email })
    classroomTemplate.value = await axios.put(`${import.meta.env.VITE_API_URL}/templates`, cloned)
  }

  return {
    classroomTemplate,
    basicTemplateData,
    fetchTemplate,
    changeTemplateData,
    deleteClassroomTemplate,
    getBasicTemplateData,
    createProjectTemplate,
    addInstructor
  }
})

const mockdata: TemplateData = {
  templateId: '12',
  creationDate: '2022.01.11',
  templateName: 'Computer Networks',
  projects: [
    {
      id: '0',
      name: 'Computer Network Project 1',
      tasks: [
        { id: '0', name: 'task 1 name' },
        { id: '1', name: 'task 2 name' }
      ]
    },
    {
      id: '1',
      name: 'Computer Network Project 2',
      tasks: [
        { id: '0', name: 'task 1 name' },
        { id: '1', name: 'task 2 name' }
      ]
    }
  ],
  resources: [
    { id: '0', name: 'moodle course', link: 'https://www.google.com' },
    { id: '1', name: 'Introduction to DHCP', link: 'https://www.google.com' }
  ],
  instructors: [
    { instructorId: 'John Doe', email: 'john.doe@mailservice.com' },
    { instructorId: 'John Doe2', email: 'john.doe2@mailservice.com' }
  ]
}
