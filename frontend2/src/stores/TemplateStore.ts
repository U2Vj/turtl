import axios from 'axios'
import { defineStore } from 'pinia'
import { ref, watchEffect } from 'vue'

type BasicTemplateData = {
  templateId: string
  templateName: string
  creationDate: string
}

type Task = { id: string; name: string }

type AdditionalTemplateData = {
  projects: {
    id: string
    name: string
    tasks: Task[]
  }[]
  resources: { id: string; name: string; link: string }[]
  instructors: { name: string; email: string }[]
}

export type TemplateData = BasicTemplateData & AdditionalTemplateData

export const useTemplateStore = defineStore('template', () => {
  const template = ref<TemplateData>()
  const basicTemplateData = ref<BasicTemplateData[]>()

  async function fetchTemplate(templateId: string) {
    template.value = mockdata
    //template.value = await axios.get(`${import.meta.env.VITE_API_URL}/templates/${templateId}`)

    return template
  }

  async function changeTemplateData(templateId: string, templateData: TemplateData) {
    /* template.value = await axios.post(
      `${import.meta.env.VITE_API_URL}/templates/${templateId}`,
      templateData
    ) */
    return template
  }

  async function deleteTemplate(templateId: string) {
    await axios.delete(`${import.meta.env.VITE_API_URL}/templates/${templateId}`)
  }

  async function getBasicTemplateData() {
    basicTemplateData.value = await axios.get(`${import.meta.env.VITE_API_URL}/templates`)
    return basicTemplateData
  }

  return {
    template,
    basicTemplateData,
    fetchTemplate,
    changeTemplateData,
    deleteTemplate,
    getBasicTemplateData
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
    { name: 'John Doe', email: 'john.doe@mailservice.com' },
    { name: 'John Doe2', email: 'john.doe2@mailservice.com' }
  ]
}
