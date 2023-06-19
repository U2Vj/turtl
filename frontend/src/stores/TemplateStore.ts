import axios from 'axios'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useCloned } from '@vueuse/core'

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
  virtualization: Virtualization[]
  acceptance_criteria: AcceptanceCriteria[]
}

type Virtualization = {
  id: string
  name: string
  role: string
  compose_file: string
}

type AcceptanceCriteria = {
  acceptance_criteria_questionaire: AcceptanceCriteriaQuestionaire[]
}

type AcceptanceCriteriaQuestionaire = {
  questions: Question[]
}

type Question = {
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
    task_template: TaskTemplate[]
  }[]
  helpful_resources: { id: string; title: string; url: string }[]
  managers: User[]
}

export type TemplateData = BasicTemplateData & AdditionalTemplateData

export const useTemplateStore = defineStore('template', () => {
  const classroomTemplate = ref<TemplateData>()
  const basicTemplateData = ref<BasicTemplateData[]>()

  async function fetchTemplate(id: string) {
    classroomTemplate.value = mockdata
    classroomTemplate.value = await axios.get(`${import.meta.env.VITE_API_URL}/templates/${id}`)

    return classroomTemplate
  }

  async function changeTemplateData(id: string, templateData: TemplateData) {
    classroomTemplate.value = await axios.post(
      `${import.meta.env.VITE_API_URL}/templates/${id}`,
      templateData
    )
    return classroomTemplate
  }

  async function deleteClassroomTemplate(id: string) {
    await axios.delete(`${import.meta.env.VITE_API_URL}/templates/${id}`)
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

  async function addManager(id: string, email: string) {
    const { cloned } = useCloned(classroomTemplate)
    cloned.value?.managers.push({ id, email })
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
    addManager
  }
})

const mockdata: TemplateData = {
  id: '12',
  title: 'Computer Networks',
  created_at: '2022.01.11',
  updated_at: '2023.03.06',
  helpful_resources: [
    { id: '0', title: 'moodle course', url: 'https://www.google.com' },
    { id: '1', title: 'Introduction to DHCP', url: 'https://www.google.com' }
  ],
  managers: [
    { id: 'John Doe', email: 'john.doe@mailservice.com' },
    { id: 'John Doe2', email: 'john.doe2@mailservice.com' }
  ],
  project_templates: [
    {
      id: '0',
      title: 'Computer Network Project 1',
      task_template: [
        {
          id: '0',
          title: 'task 1 name',
          description: 'Eine BEschreibung',
          difficulty: 'Beginner',
          type: 'Attack',
          virtualization: [
            {
              id: '0',
              name: 'Docker',
              role: 'User Shell',
              compose_file: 'file'
            }
          ],
          acceptance_criteria: [
            {
              acceptance_criteria_questionaire: [
                {
                  questions: [
                    {
                      question: 'What is the IP Adress?',
                      question_choice: [
                        {
                          answer: '123.456.789',
                          is_correct: false
                        },
                        {
                          answer: '333.232.789',
                          is_correct: false
                        },
                        {
                          answer: '234.333.242',
                          is_correct: true
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          id: '1',
          title: 'task 2 name',
          description: 'Eine Beschreibung',
          difficulty: 'Advanced',
          type: 'Attack',
          virtualization: [
            {
              id: '0',
              name: 'Docker',
              role: 'User Shell',
              compose_file: 'file'
            }
          ],
          acceptance_criteria: [
            {
              acceptance_criteria_questionaire: [
                {
                  questions: [
                    {
                      question: 'What is the IP Adress?',
                      question_choice: [
                        {
                          answer: '123.456.789',
                          is_correct: false
                        },
                        {
                          answer: '333.232.789',
                          is_correct: false
                        },
                        {
                          answer: '234.333.242',
                          is_correct: true
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          id: '2',
          title: 'task 1 name',
          description: 'Eine BEschreibung',
          difficulty: 'Beginner',
          type: 'Attack',
          virtualization: [
            {
              id: '0',
              name: 'Docker',
              role: 'User Shell',
              compose_file: 'file'
            }
          ],
          acceptance_criteria: [
            {
              acceptance_criteria_questionaire: [
                {
                  questions: [
                    {
                      question: 'What is the IP Adress?',
                      question_choice: [
                        {
                          answer: '123.456.789',
                          is_correct: false
                        },
                        {
                          answer: '333.232.789',
                          is_correct: false
                        },
                        {
                          answer: '234.333.242',
                          is_correct: true
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    },
    {
      id: '2',
      title: '2 Computer Network Project 2',
      task_template: [
        {
          id: '0',
          title: '2 task 1 name',
          description: 'Eine BEschreibung',
          difficulty: 'Beginner',
          type: 'Attack',
          virtualization: [
            {
              id: '0',
              name: 'Docker',
              role: 'User Shell',
              compose_file: 'file'
            }
          ],
          acceptance_criteria: [
            {
              acceptance_criteria_questionaire: [
                {
                  questions: [
                    {
                      question: 'What is the IP Adress?',
                      question_choice: [
                        {
                          answer: '123.456.789',
                          is_correct: false
                        },
                        {
                          answer: '333.232.789',
                          is_correct: false
                        },
                        {
                          answer: '234.333.242',
                          is_correct: true
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        },
        {
          id: '1',
          title: 'task 2 name',
          description: 'Eine Beschreibung',
          difficulty: 'Advanced',
          type: 'Attack',
          virtualization: [
            {
              id: '0',
              name: 'Docker',
              role: 'User Shell',
              compose_file: 'file'
            }
          ],
          acceptance_criteria: [
            {
              acceptance_criteria_questionaire: [
                {
                  questions: [
                    {
                      question: 'What is the IP Adress?',
                      question_choice: [
                        {
                          answer: '123.456.789',
                          is_correct: false
                        },
                        {
                          answer: '333.232.789',
                          is_correct: false
                        },
                        {
                          answer: '234.333.242',
                          is_correct: true
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
