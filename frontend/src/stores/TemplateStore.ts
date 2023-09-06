import { useCloned } from '@vueuse/core'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeAxiosRequest } from './AxiosInstance'

type BasicTemplateData = {
  id: string
  title: string
  created_at: string
  updated_at: string
}

type TaskTemplate = {
  id: string
  title: string
  description: string
  difficulty: string
  type: string
  virtualization: Virtualization
  acceptance_criteria: AcceptanceCriteria
}

type Virtualization = {
  id: string
  name: string
  role: string
  compose_file: string
}

type AcceptanceCriteria = {
  acceptance_criteria_questionaire?: Question[]
}

type Question = {
  id: string
  question: string
  question_choice: QuestionChoice[]
}

type QuestionChoice = {
  answer: string
  is_correct: boolean
}

export type User = { id: string; email: string }

type AdditionalTemplateData = {
  project_templates: {
    id: string
    title: string
    task_templates: TaskTemplate[]
  }[]
  helpful_resources: { id: string; title: string; url: string }[]
  managers: User[]
}

export type TemplateData = BasicTemplateData & AdditionalTemplateData

export const useTemplateStore = defineStore('template', () => {
  const classroomTemplate = ref<TemplateData | undefined>()
  const basicTemplateData = ref<BasicTemplateData[]>()

  async function fetchTemplate(id: string) {
    const response = await makeAxiosRequest(`/templates/classrooms/${id}`, 'GET', true, true)
    if (response.success) {
      classroomTemplate.value = response.data
    }
    return classroomTemplate
  }

  async function changeTemplateData(id: string, templateData: TemplateData) {
    const response = await makeAxiosRequest(
      `/templates/classrooms/${id}`,
      'PUT',
      true,
      true,
      templateData
    )
    console.log(response)
    console.log('templatData', templateData)
    if (response.success) {
      classroomTemplate.value = response.data
    } else {
      console.error
    }
    return classroomTemplate
  }

  async function deleteClassroomTemplate(id: string) {
    const response = await makeAxiosRequest(`/templates/classrooms/${id}`, 'DELETE', true, true)
    return response.success
  }

  async function getBasicTemplateData() {
    const response = await makeAxiosRequest('/templates/classrooms', 'GET', true, true)
    if (response.success) {
      basicTemplateData.value = response.data
    } else {
      console.error
    }
    return basicTemplateData
  }

  async function createProjectTemplate(projectName: string) {
    const data = {
      title: projectName
    }
    const response = await makeAxiosRequest('templates/classrooms', 'POST', true, true, data)
    if (response.success) {
      return { success: true, id: response.data.id }
    }
    return { success: false, id: null }
  }

  async function addManager(id: string, email: string) {
    const { cloned } = useCloned(classroomTemplate)
    cloned.value?.managers.push({ id, email })
    const response = await makeAxiosRequest('templates/classrooms/', 'PUT', true, true, cloned)
    if (response.success) {
      classroomTemplate.value = response.data
    }
  }

  function getTask(taskId: string) {
    // classroomTemplate.value = mockdata

    let task: TaskTemplate | undefined

    classroomTemplate.value?.project_templates.forEach((project) => {
      project.task_templates.forEach((task_template) => {
        if (task_template.id === taskId) {
          task = task_template
        }
      })
    })
    return task
  }

  return {
    classroomTemplate,
    basicTemplateData,
    fetchTemplate,
    changeTemplateData,
    deleteClassroomTemplate,
    getBasicTemplateData,
    createProjectTemplate,
    addManager,
    getTask
  }
})

// const mockdata: TemplateData = {
//   id: '12',
//   title: 'Computer Networks',
//   created_at: '2022.01.11',
//   updated_at: '2023.03.06',
//   helpful_resources: [
//     { id: '0', title: 'moodle course', url: 'https://www.google.com' },
//     { id: '1', title: 'Introduction to DHCP', url: 'https://www.google.com' }
//   ],
//   managers: [
//     { id: 'John Doe', email: 'john.doe@mailservice.com' },
//     { id: 'John Doe2', email: 'john.doe2@mailservice.com' }
//   ],
//   project_templates: [
//     {
//       id: '0',
//       title: 'Computer Network Project 1',
//       task_templates: [
//         {
//           id: '0',
//           title: 'task 1 name',
//           description: 'Eine BEschreibung',
//           difficulty: 'Beginner',
//           type: 'Attack',
//           virtualization: {
//             id: '0',
//             name: 'Docker',
//             role: 'User Shell',
//             compose_file: 'file'
//           },
//           acceptance_criteria: {
//             acceptance_criteria_questionaire: [
//               {
//                 id: '0',
//                 question: 'xdtgfchWhat is the IP Adress?',
//                 question_choice: [
//                   {
//                     answer: '123.456.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '1333.232.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '234.333.242',
//                     is_correct: true
//                   }
//                 ]
//               },
//               {
//                 id: '1',
//                 question: '1What is the IP Adress?',
//                 question_choice: [
//                   {
//                     answer: '123.456.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '333.232.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '234.333.242',
//                     is_correct: true
//                   }
//                 ]
//               },
//               {
//                 id: '2',
//                 question: '1What is the IP Adress?',
//                 question_choice: [
//                   {
//                     answer: '1123.456.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '333.232.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '234.333.242',
//                     is_correct: true
//                   }
//                 ]
//               }
//             ]
//           }
//         },
//         {
//           id: '1',
//           title: 'task 2 name',
//           description: 'Eine Beschreibung',
//           difficulty: 'Advanced',
//           type: 'Attack',
//           virtualization: {
//             id: '0',
//             name: 'Docker',
//             role: 'User Shell',
//             compose_file: 'file'
//           },
//           acceptance_criteria: {
//             acceptance_criteria_questionaire: [
//               {
//                 id: '5',
//                 question: 'ööööWhat is the IP Adress?',
//                 question_choice: [
//                   {
//                     answer: '123.456.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '333.232.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '234.333.242',
//                     is_correct: true
//                   }
//                 ]
//               }
//             ]
//           }
//         },
//         {
//           id: '2',
//           title: 'task 1 name',
//           description: 'Eine BEschreibung',
//           difficulty: 'Beginner',
//           type: 'Attack',
//           virtualization: {
//             id: '0',
//             name: 'Docker',
//             role: 'User Shell',
//             compose_file: 'file'
//           },
//           acceptance_criteria: {
//             acceptance_criteria_questionaire: [
//               {
//                 id: '7',
//                 question: 'What is the IP Adress?',
//                 question_choice: [
//                   {
//                     answer: '123.456.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '333.232.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '234.333.242',
//                     is_correct: true
//                   }
//                 ]
//               }
//             ]
//           }
//         }
//       ]
//     },
//     {
//       id: '2',
//       title: '2 Computer Network Project 2',
//       task_templates: [
//         {
//           id: '3',
//           title: '2 task 1 name',
//           description: 'Eine BEschreibung',
//           difficulty: 'Beginner',
//           type: 'Attack',
//           virtualization: {
//             id: '0',
//             name: 'Docker',
//             role: 'User Shell',
//             compose_file: 'file'
//           },
//           acceptance_criteria: {
//             acceptance_criteria_questionaire: [
//               {
//                 id: '9',
//                 question: 'What is the IP Adress?',
//                 question_choice: [
//                   {
//                     answer: '123.456.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '333.232.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '234.333.242',
//                     is_correct: true
//                   }
//                 ]
//               }
//             ]
//           }
//         },
//         {
//           id: '4',
//           title: 'task 2 name',
//           description: 'Eine Beschreibung',
//           difficulty: 'Advanced',
//           type: 'Attack',
//           virtualization: {
//             id: '0',
//             name: 'Docker',
//             role: 'User Shell',
//             compose_file: 'file'
//           },
//           acceptance_criteria: {
//             acceptance_criteria_questionaire: [
//               {
//                 id: '10',
//                 question: 'What is the IP Adress?',
//                 question_choice: [
//                   {
//                     answer: '123.456.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '333.232.789',
//                     is_correct: false
//                   },
//                   {
//                     answer: '234.333.242',
//                     is_correct: true
//                   }
//                 ]
//               }
//             ]
//           }
//         }
//       ]
//     }
//   ]
// }
