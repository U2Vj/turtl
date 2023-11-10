<script setup lang="ts">
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import { ref } from 'vue'
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import {useEnrollmentStore} from '@/stores/EnrollmentStore'
import {useToast} from 'vue-toastification'
import {useRouter} from 'vue-router'

const props = defineProps<{ enrollmentId: number }>()
const enrollmentStore = useEnrollmentStore()
const toast = useToast()
const router = useRouter()

const tab = ref(null)
const classroom = ref({
  name: 'Networks',
  information: {
    contactInfo: 'one.example@example.com',
    managers: {
      managerName: 'John Doe',
      managerMail: 'john.doe@example.com'
    },
    instructors: [
      {
        instructorName: 'Tom Night',
        instructorMail: 'tom.night@example.com'
      },
      {
        instructorName: 'Sepp Peter',
        instructorMail: 'sepp.peter@example.com'
      }
    ]
  },
  helpfulResources: [
    {
      name: 'Moodle',
      link: 'https://moodle.hs-duesseldorf.de/my/'
    },
    {
      name: 'Intro',
      link: 'https://de.wikipedia.org/wiki/Wiki'
    },
    {
      name: 'Doku',
      link: 'https://vuetifyjs.com/'
    }
  ],
  team: {
    attackers: ['exmpl@ample.com', 'tom@test.com'],
    defenders: ['exmpl@ample.com', 'tom@test.com']
  }
})

const projects = ref([
  {
    id: 1,
    room: 'Brute-Force',
    role: 'Attack',
    description: 'testtext',
    manager_name: 'Frank Doe',
    expanded: false,
    taskList: [
      {
        id: 1,
        task: 'Sieben Aufgabe',
        done: true
      },
      {
        id: 2,
        task: 'Acht Aufgabe',
        done: true
      },
      {
        id: 3,
        task: 'Neun Aufgabe',
        done: true
      }
    ]
  },
  {
    id: 2,
    room: 'Man in the middle',
    role: 'Defense',
    description: 'testtext',
    manager_name: 'Jan Doe',
    expanded: false,
    taskList: [
      {
        id: 1,
        task: 'Eins Aufgabe',
        done: true
      },
      {
        id: 2,
        task: 'Zwei Aufgabe',
        done: true
      },
      {
        id: 3,
        task: 'Drei Aufgabe',
        done: true
      },
      {
        id: 4,
        task: 'Viertel Aufgabe',
        done: false
      }
    ]
  },
  {
    id: 3,
    room: 'Computer Networks',
    role: 'Attack',
    description: 'testtext',
    manager_name: 'Tom Doe',
    expanded: false,
    taskList: [
      {
        id: 1,
        task: 'Vier Aufgabe',
        done: true
      },
      {
        id: 2,
        task: 'Fünf Aufgabe',
        done: true
      },
      {
        id: 3,
        task: 'Sechs Aufgabe',
        done: false
      },
      {
        id: 4,
        task: 'Drei Aufgabe',
        done: true
      },
      {
        id: 5,
        task: 'Viertel Aufgabe',
        done: true
      }
    ]
  },
  {
    id: 4,
    room: 'Firewall',
    role: 'Defense',
    description: 'testtext',
    manager_name: 'John Doe',
    expanded: false,
    taskList: [
      {
        id: 1,
        task: 'Elf Aufgabe',
        done: true
      },
      {
        id: 2,
        task: 'Zwölf Aufgabe',
        done: false
      },
      {
        id: 3,
        task: 'Dreizehn Aufgabe',
        done: false
      }
    ]
  }
])

const showTask = ref(false)

function getTasksDone() {
  let completedTasks = 0

  for (const project of projects.value) {
    for (const task of project.taskList) {
      if (task.done) {
        completedTasks++
      }
    }
  }
  return completedTasks
}

function getAllTasks() {
  let allTasks = 0

  for (const project of projects.value) {
    allTasks += project.taskList.length
  }
  return allTasks
}

function getDoneTasksOfProject(id: number): number {
  let completedTasks

  let project = projects.value.find((p) => p.id === id)
  if (project) {
    completedTasks = project.taskList.filter((t) => t.done).length
  } else {
    completedTasks = 0
  }
  return completedTasks
}

function getAllTasksOfProject(id: number): number {
  let allTasks
  let project = projects.value.find((p) => p.id === id)
  if (project) {
    allTasks = project.taskList.length
  } else {
    allTasks = 0
  }
  return allTasks
}

function getTaskProgress() {
  return 100 * (getTasksDone() / getAllTasks())
}

function getTaskProgressOfProject(id: number): number {
  if (getAllTasksOfProject(id) > 0) {
    return 100 * (getDoneTasksOfProject(id) / getAllTasksOfProject(id))
  } else {
    return 0
  }
}

function getNumberOfDoneProjects() {
  let count = 0
  for (const project of projects.value) {
    let allTasksDone = true
    for (const task of project.taskList) {
      if (!task.done) {
        allTasksDone = false
        break
      }
    }
    if (allTasksDone) {
      count++
    }
  }
  return count
}

function openResourceLink(link: string) {
  if (link) {
    window.open(link, '_blank')
  }
}

function unenroll() {
  enrollmentStore.unenroll(props.enrollmentId).then(async () => {
    // TODO: add classroom name
    toast.info("You have unenrolled from this classroom")
    await router.push({ name: 'StudentMyClassrooms' })
  }).catch((e) => toast.error(e.message))
}
</script>

<template>
  <DefaultLayout>
    <template #heading>The name of the classroom</template>
    <template #default>
      <v-tabs v-model="tab" color="primary" align-tabs="start">
        <v-tab value="1">Projects</v-tab>
        <v-tab value="2">Information</v-tab>
      </v-tabs>
      <v-window v-model="tab">
        <v-window-item value="1">
          <v-container>
            <v-row>
              <v-col v-for="item in projects" :key="item.id" cols="12" xs="12" sm="6" md="4">
                <v-card
                  :key="item.id"
                  :title="item.room"
                  variant="flat"
                  color="cardColor"
                  class="elevation-4"
                >
                  <v-card-text>
                    <v-progress-linear
                      :color="getTaskProgressOfProject(item.id) === 100 ? 'finished' : 'progress'"
                      :height="25"
                      rounded
                      rounded-bar
                      bg-color="#ffffff"
                      bg-opacity="1"
                      :model-value="getTaskProgressOfProject(item.id)"
                    >
                      <template #default>
                        <strong>{{ Math.ceil(getTaskProgressOfProject(item.id)) }}%</strong>
                      </template>
                    </v-progress-linear>
                  </v-card-text>
                  <v-card-text>
                    <div>
                      <div v-for="task in item.taskList" :key="task.id">
                        <TextButton :button-name="task.task"></TextButton>
                        <v-icon
                          v-if="task.done === true"
                          icon="mdi-check-circle-outline"
                          color="success"
                        ></v-icon>
                      </div>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-window-item>

        <v-window-item value="2">
          <v-container>
            <v-row>
              <v-col cols="6">
                <div>
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>Instructors</v-card-title>
                    <v-card-text>
                      <div
                        v-for="instructors in classroom.information.instructors"
                        :key="instructors.instructorMail"
                      >
                        {{ instructors.instructorName }} <br />
                        {{ instructors.instructorMail }}
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
              <v-col cols="6">
                <div>
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>My Progress</v-card-title>
                    <v-card-text>
                      {{ getTasksDone() }} / {{ getAllTasks() }} Tasks Done:

                      <v-progress-linear
                        :color="getTaskProgress() === 100 ? 'finished' : 'progress'"
                        :height="25"
                        :model-value="getTaskProgress()"
                        rounded
                        rounded-bar
                        bg-color="#ffffff"
                        bg-opacity="1"
                      >
                        <template #default>
                          <strong>{{ Math.ceil(getTaskProgress()) }}%</strong>
                        </template>
                      </v-progress-linear>

                      {{ getNumberOfDoneProjects() }} / {{ projects.length }} Projects Done

                      <v-progress-linear
                        :height="25"
                        rounded
                        rounded-bar
                        bg-color="#ffffff"
                        bg-opacity="1"
                        :color="
                          getNumberOfDoneProjects() / projects.length === 100
                            ? 'finished'
                            : 'progress'
                        "
                        :model-value="100 * (getNumberOfDoneProjects() / projects.length)"
                      >
                        <template #default>
                          <strong
                            >{{
                              Math.ceil(100 * (getNumberOfDoneProjects() / projects.length))
                            }}%</strong
                          >
                        </template>
                      </v-progress-linear>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <div class="mt-5">
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>Helpful Resources</v-card-title>
                    <v-card-text>
                      <div v-for="resource in classroom.helpfulResources">
                        <TextButton
                          :button-name="resource.name"
                          @click="openResourceLink(resource.link)"
                        ></TextButton>
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
              <v-col cols="6">
                <div class="mt-5">
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>Unenroll</v-card-title>
                    <v-card-subtitle>Unenroll from this classroom</v-card-subtitle>
                    <v-card-text>
                      <!-- TODO: add modal -->
                      <ErrorButton @click="unenroll">Unenroll</ErrorButton>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-window-item>
      </v-window>
    </template>
  </DefaultLayout>
</template>
