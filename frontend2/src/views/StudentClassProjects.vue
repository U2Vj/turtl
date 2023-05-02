<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import { ref } from 'vue'

const tab = ref(null)
const expandedItem = ref<{ id: string, expanded: boolean } | null>(null)

const items = ref([
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
      },
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
      },
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
      },
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
      },
    ]
  }
])

function toggleExpansion(item:any) {
    if (expandedItem.value === item) {
      item.expanded = !item.expanded;
    } else {
      if (expandedItem.value !== null) {
        expandedItem.value.expanded = false;
      }
      item.expanded = true;
      expandedItem.value = item;
    }
}

function getExpandIcon(item:any) {
    return item.expanded ? "mdi-chevron-up" : "mdi-chevron-down";
}
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col>
          <h1>classroom name</h1>
          <v-card elevation="0">
            <v-tabs v-model="tab" color="primary" align-tabs="start">
              <v-tab value="1">Projects</v-tab>
              <v-tab value="2">Information</v-tab>
            </v-tabs>
            <v-card-text>
              <v-window v-model="tab">
                <v-window-item value="1">
                  <v-row>
                    <v-col v-for="item in items" :key="item.id" cols="12" sm="6" md="3">
                      <v-card :key="item.id" :title="item.room">
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
                          <v-row>
                            <v-col>
                              <v-btn
                                variant="outlined"
                                :append-icon="getExpandIcon(item)"
                                @click="toggleExpansion(item)"
                                >View Tasks</v-btn
                              >
                            </v-col>
                            <v-spacer></v-spacer>
                            <v-col>
                              <v-btn variant="outlined" v-if="item.progress < 100">Continue</v-btn>
                            </v-col>
                          </v-row>
                        </v-card-actions>
                        <v-expand-transition>
                          <div v-show="item.expanded">
                            <v-divider></v-divider>
                            <v-card-text>
                              <v-list-item v-for="(task, index) in item.taskList">{{index+1}}. {{task.task}}
                              <v-icon v-if="task.done===true" icon="mdi-check-circle-outline" color="success"></v-icon>
                              </v-list-item>
                            </v-card-text>
                          </div>
                        </v-expand-transition>
                      </v-card>
                    </v-col>
                  </v-row>
                  <p>SPACER</p>
                </v-window-item>
                <v-window-item value="2"> Information </v-window-item>
              </v-window>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>
