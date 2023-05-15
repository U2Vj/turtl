<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import Footer from '@/components/Footer.vue'
import { ref } from 'vue'

const headers = [
  { title: 'Task', key: 'name' },
  { title: 'Classroom', key: 'classroom' },
  { title: 'Visited At', key: 'visited' }
]

const values = [
  {
    name: 'Nftables Beginner',
    classroom: 'Rechnernetze',
    visited: '2023-10-02',
    id: 1
  },
  {
    name: 'Nmap Scans',
    classroom: 'It-Sicherheit',
    visited: '2023-09-01',
    id: 2
  }
]

const classrooms = ref([
  {
    id: '1',
    room: 'Rechnernetze',
    progress: 20
  },
  {
    id: '2',
    room: 'IT-Sicherheit',
    progress: 50,
    completed: false
  }
])
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <div>
          <h1>Recently Opened Tasks</h1>
        </div>
        <v-data-table :headers="headers" :items="values"></v-data-table>
      </v-row>
    </v-container>

    <v-container fluid>
      <div class="d-flex align-left">
        <h1>Recently Visited Classrooms</h1>
      </div>
      <v-row>
        <v-col
          id="classrooms"
          v-for="classroom in classrooms"
          :key="classroom.id"
          cols="12"
          sm="6"
          md="3"
        >
          <v-card :key="classroom.id" :title="classroom.room">
            <v-progress-linear
              id="probar"
              color="primary"
              :height="20"
              :model-value="classroom.progress"
            >
              <template v-slot:default="{ value }">
                <strong>{{ Math.ceil(classroom.progress) }}%</strong>
              </template>
            </v-progress-linear>
            <v-card-actions>
              <v-btn variant="outlined">Go to Room</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
  <Footer></Footer>
</template>

<style scoped>
#probar {
  margin: auto;
  width: auto;
}

.classroom {
  margin-top: 100px;
}

.tasks {
  width: 50%;
  margin-left: 0px;
}
</style>
