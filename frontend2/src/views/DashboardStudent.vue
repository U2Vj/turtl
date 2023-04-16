<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import { ref } from 'vue'

const headers = [{ title: 'Task' }, { title: 'Classroom' }, { title: 'Visited At' }]

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
        <v-col>
          <div class="d-flex align-left">
            <h1>Recently Opened Tasks</h1>
          </div>
          <v-data-table
            v-model:items-per-page="itemsPerPage"
            :headers="headers"
            :items="recentTasks"
          ></v-data-table>
        </v-col>
      </v-row>
    </v-container>

    <v-container fluid>
      <v-row>
        <div class="d-flex align-left">
          <h1>Recently Visited Classrooms</h1>
        </div>
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
</template>

<style scoped>
#classrooms {
  margin-top: 3em;
}

#probar {
  margin: auto;
  width: auto;
}

.cardgroup {
  margin: auto;
  margin-top: 2%;
  width: 80%;
}
</style>
