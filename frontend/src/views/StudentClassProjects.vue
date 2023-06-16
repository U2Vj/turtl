<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import Footer from '@/components/Footer.vue'
import { ref } from 'vue'

const tab = ref(null)
const expandedItem = ref<{ id: string; expanded: boolean } | null>(null)
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
    for (const task of project.taskList) {
      allTasks++
    }
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

function getExpandIcon(item: any) {
  return item.expanded ? 'mdi-chevron-up' : 'mdi-chevron-down'
}
</script>

<template>
  <turtl-header></turtl-header>
  <v-main class="d-flex justify-center">
    <div class="main-container mt-5 ml-3 mr-3">
      <v-container>
        <h1>The name of the classroom</h1>
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
                        <template v-slot:default>
                          <strong>{{ Math.ceil(getTaskProgressOfProject(item.id)) }}%</strong>
                        </template>
                      </v-progress-linear>
                    </v-card-text>
                    <v-card-actions>
                      <v-btn
                        v-if="!showTask"
                        append-icon="mdi-chevron-down"
                        @click="showTask = true"
                        variant="text"
                        color="primary"
                      >
                        View Tasks
                      </v-btn>
                      <v-btn
                        v-if="showTask"
                        variant="text"
                        color="primary"
                        append-icon="mdi-chevron-down"
                        @click="showTask = false"
                      >
                        Hide Tasks
                      </v-btn>
                      <v-spacer></v-spacer>
                      <v-btn
                        variant="tonal"
                        color="primary"
                        class="elevation-2"
                        v-if="getTaskProgressOfProject(item.id) < 100"
                        >Continue</v-btn
                      >
                    </v-card-actions>
                    <v-card-text v-show="showTask">
                      <div :id="`taskWrapper${item.id}`">
                        <div v-for="(task, index) in item.taskList" :key="task.id">
                          {{ index + 1 }}. {{ task.task }}
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
                      <v-card-title>Information</v-card-title>
                      <v-card-text>
                        <div><h3>Contact Information</h3></div>
                        <div>{{ classroom.information.contactInfo }}</div>
                        <div class="mt-5"><h3>Manager</h3></div>
                        {{ classroom.information.managers.managerName }} <br />
                        {{ classroom.information.managers.managerMail }}
                        <div class="mt-5"><h3>Instructors</h3></div>
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
                  <div class="mt-5">
                    <v-card variant="flat" color="cardColor" class="elevation-4">
                      <v-card-title>Helpful Ressources</v-card-title>
                      <v-card-text>
                        <a
                          v-for="(resource, index) in classroom.helpfulResources"
                          :key="index"
                          :href="resource.link"
                        >
                          {{ index + 1 }}. {{ resource.name }}<br />
                        </a>
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
                          <template v-slot:default>
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
                          <template v-slot:default>
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
                  <div class="mt-5">
                    <v-card variant="flat" color="cardColor" class="elevation-4">
                      <v-card-title>My Team</v-card-title>
                      <v-card-text>
                        <h3>Attacker</h3>
                        <div v-for="attacker in classroom.team.attackers">
                          {{ attacker }}
                        </div>
                        <div class="mt-5"><h3>Defender</h3></div>
                        <div v-for="defnder in classroom.team.defenders">
                          {{ defnder }}
                        </div>
                      </v-card-text>
                    </v-card>
                  </div>
                </v-col>
              </v-row>
            </v-container>
          </v-window-item>
        </v-window>
      </v-container>
    </div>
  </v-main>
  <Footer></Footer>
</template>

<style scoped></style>
