<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import { ref } from 'vue'

const tab = ref(null)
const expandedItem = ref<{ id: string; expanded: boolean } | null>(null)
const selectedClassroom = 0
const classroom = ref(
  {
    name: 'Networks',
    information:
      {
        contactInfo: 'one.example@example.com',
        manager:
          {
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
    helpfulResources:
      {
        resource: ['Moodle', 'Intro', 'Doku']
      },
    team:
      {
        attacker: [
          {
            attackerName: 'max',
            attackerEmail: 'exmplample.com'
          }
        ],
        defender: [
          {
            defenderName: 'max',
            defenderEmail: 'exmplample.com'
          }
        ]
      }
  }
)

const projects = ref([
  {
    id: '1',
    room: 'Brute-Force',
    role: 'Attack',
    description: 'testtext',
    progress: 33,
    manager_name: 'Frank Doe',
    completed: true,
    expanded: false,
    taskList: [
      {
        task: 'Sieben Aufgabe',
        done: false
      },
      {
        task: 'Acht Aufgabe',
        done: true
      },
      {
        task: 'Neun Aufgabe',
        done: false
      }
    ]
  },
  {
    id: '2',
    room: 'Man in the middle',
    role: 'Defense',
    description: 'testtext',
    progress: 33,
    manager_name: 'Jan Doe',
    completed: false,
    expanded: false,
    taskList: [
      {
        task: 'Eins Aufgabe',
        done: false
      },
      {
        task: 'Zwei Aufgabe',
        done: true
      },
      {
        task: 'Drei Aufgabe',
        done: false
      }
    ]
  },
  {
    id: '3',
    room: 'Computer Networks',
    role: 'Attack',
    description: 'testtext',
    progress: 100,
    manager_name: 'Tom Doe',
    completed: false,
    expanded: false,
    taskList: [
      {
        task: 'Vier Aufgabe',
        done: true
      },
      {
        task: 'Fünf Aufgabe',
        done: false
      },
      {
        task: 'Sechs Aufgabe',
        done: false
      }
    ]
  },
  {
    id: '4',
    room: 'Firewall',
    role: 'Defense',
    description: 'testtext',
    progress: 50,
    manager_name: 'John Doe',
    completed: false,
    expanded: false,
    taskList: [
      {
        task: 'Elf Aufgabe',
        done: false
      },
      {
        task: 'Zwölf Aufgabe',
        done: true
      },
      {
        task: 'Dreizehn Aufgabe',
        done: true
      }
    ]
  }
])

function toggleExpansion(item: any) {
  if (expandedItem.value === item) {
    item.expanded = !item.expanded
  } else {
    if (expandedItem.value !== null) {
      expandedItem.value.expanded = false
    }
    item.expanded = true
    expandedItem.value = item
  }
}

function getExpandIcon(item: any) {
  return item.expanded ? 'mdi-chevron-up' : 'mdi-chevron-down'
}
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <h1>classroom name</h1>
      <v-tabs v-model="tab" color="primary" align-tabs="start">
        <v-tab value="1">Projects</v-tab>
        <v-tab value="2">Information</v-tab>
      </v-tabs>
      <v-window v-model="tab">
        <v-window-item value="1">
          <v-card elevation="0">
            <v-card-text>
              <div v-for="item in projects" :key="item.id" cols="12" sm="6" md="3">
                <v-card :key="item.id" :title="item.room" variant="outlined">
                  <v-card-text v-if="item.progress < 100">
                    <v-progress-linear
                      id="probar"
                      :color="item.progress === 100 ? 'success' : 'grey'"
                      :height="20"
                      :model-value="item.progress"
                      rounded
                    >
                      <template v-slot:default>
                        <strong>{{ Math.ceil(item.progress) }}%</strong>
                      </template>
                    </v-progress-linear>
                  </v-card-text>
                  <v-card-text class="text-success" v-else>
                    <v-icon icon="mdi-check-circle-outline" color="success"></v-icon>
                    Project Complete
                  </v-card-text>
                  <v-card-actions>
                    <div>
                      <v-btn
                        variant="outlined"
                        :append-icon="getExpandIcon(item)"
                        @click="toggleExpansion(item)"
                        >View Tasks</v-btn
                      >
                    </div>
                    <v-spacer></v-spacer>
                    <div>
                      <v-btn variant="outlined" v-if="item.progress < 100">Continue</v-btn>
                    </div>
                  </v-card-actions>
                  <v-expand-transition>
                    <div v-show="item.expanded">
                      <v-divider></v-divider>
                      <v-card-text>
                        <v-list-item v-for="(task, index) in item.taskList"
                          >{{ index + 1 }}. {{ task.task }}
                          <v-icon
                            v-if="task.done === true"
                            icon="mdi-check-circle-outline"
                            color="success"
                          ></v-icon>
                        </v-list-item>
                      </v-card-text>
                    </div>
                  </v-expand-transition>
                </v-card>
              </div>
            </v-card-text>
          </v-card>
        </v-window-item>

        <v-window-item value="2">
          <v-card elevation="0">
            <v-card-text>
              <v-row justify="space-around">
                <v-col cols="12" sm="8" md="5">
                  <div>
                    <v-card variant="outlined">
                      <v-card-title>Information</v-card-title>
                      <v-card-text>
                        <div class="d-flex">
                          <div>
                            <div>Contact Information:</div>
                            <div class="mt-5">Manager:</div>
                            <br>
                            <div class="mt-5">Instructors:</div>
                          </div>
                          <div class="ml-auto">
                            <div>{{ classroom.information.contactInfo }}</div>
                            <div class="mt-5">{{ classroom.information.manager.managerName }} <br> {{ classroom.information.manager.managerMail }}</div>
                            <div class="mt-5"></div>
                            <div v-for="instructors in classroom.information.instructors">{{ instructors.instructorName }} <br> {{ instructors.instructorMail }}</div>
                          </div>
                        </div>
                      </v-card-text>
                    </v-card>
                  </div>
                  <div class="mt-5">
                    <v-card variant="outlined">
                      <v-card-title>Helpful Ressources:</v-card-title>
                      <v-card-text>
                        1. Moodle <br />
                        2. Intro <br />
                        3. Doku <br />
                        4. Doku
                      </v-card-text>
                    </v-card>
                  </div>
                </v-col>
                <v-col cols="12" sm="8" md="5">
                  <div>
                    <v-card variant="outlined">
                      <v-card-title>My Progress:</v-card-title>
                      <v-card-text>
                        Tasks Done: <br />
                        Projects Done:
                      </v-card-text>
                    </v-card>
                  </div>
                  <div class="mt-5">
                    <v-card variant="outlined">
                      <v-card-title>My Team</v-card-title>
                      <v-card-text>
                        <h3>Attacker</h3>
                        Max (max.email) <br />
                        Jan (jan.email)<br />
                        <h3>Defender</h3>
                        Hans (hans.email) <br />
                        Sepp (sepp.email)
                      </v-card-text>
                    </v-card>
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-window-item>
      </v-window>
    </v-container>
  </v-main>
</template>
