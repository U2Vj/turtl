<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import { ref } from 'vue'

const items = ref([
  {
    id: '1',
    room: 'Brute-Force',
    role: 'Attack',
    description: 'testtext',
    progress: 33,
    manager_name: 'Frank Doe',
    completed: true
  },
  {
    id: '2',
    room: 'Man in the middle',
    role: 'Defense',
    description: 'testtext',
    progress: 33,
    manager_name: 'Jan Doe',
    completed: false
  },
  {
    id: '3',
    room: 'Computer Networks',
    role: 'Attack',
    description: 'testtext',
    progress: 100,
    manager_name: 'Tom Doe',
    completed: false
  },
  {
    id: '4',
    room: 'Firewall',
    role: 'Defense',
    description: 'testtext',
    progress: 50,
    manager_name: 'John Doe',
    completed: false
  }
])

const dialog = ref(false)

function joinClassroomBtn() {
  // TODO: Add which classroom to join
  dialog.value = true
}

function close() {
  dialog.value = false
}

function join() {
  dialog.value = false
}
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col cols="auto">
          <h1>My Classrooms</h1>
        </v-col>
        <v-col cols="auto">
          <v-btn @click="joinClassroomBtn()">
            Join Classroom
            <v-dialog v-model="dialog" persistent width="50%">
              <v-card>
                <v-toolbar title="Join Classroom"> </v-toolbar>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col>
                        <p>Enter the code to join the classroom.</p>
                      </v-col>
                    </v-row>
                    <v-row> </v-row>
                    <v-row>
                      <v-col cols="8">
                        <v-text-field label="Enter Code" variant="solo"></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn @click="close"> Cancel </v-btn>
                  <v-btn @click="join"> Join Classroom </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col v-for="item in items" :key="item.id" cols="12" sm="6" md="3">
          <v-card
            :key="item.id"
            :title="item.room"
            :subtitle="item.manager_name"
            :border-variant="item.completed === true ? 'success' : 'danger'"
          >
            <v-card-text v-if="item.role === 'Attack'">
              <v-icon icon="mdi-sword"></v-icon>
              Role: {{ item.role }}
            </v-card-text>
            <v-card-text v-else>
              <v-icon icon="mdi-shield"></v-icon>
              Role: {{ item.role }}
            </v-card-text>
            <v-card-text>
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
            <v-card-actions>
              <v-btn variant="outlined" to="StudentClassProjects">Visit Classroom</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>
