<script setup lang="ts">
import SecundaryButton from '@/components/buttons/SecondaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
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
  <DefaultLayout>
    <template #heading>Recently Opened Tasks</template>
    <template #default>
      <v-data-table :headers="headers" :items="values"></v-data-table>
      <div class="mb-5">
        <h1>Recently Visited Classrooms</h1>
      </div>
      <v-row>
        <v-col
          id="classrooms"
          v-for="classroom in classrooms"
          :key="classroom.id"
          cols="12"
          xs="12"
          sm="6"
          md="4"
        >
          <v-card
            :key="classroom.id"
            :title="classroom.room"
            variant="flat"
            color="cardColor"
            class="elevation-4"
          >
            <v-card-text>
              <v-progress-linear
                id="probar"
                :color="classroom.progress === 100 ? 'finished' : 'progress'"
                :height="25"
                rounded
                rounded-bar
                bg-color="#ffffff"
                bg-opacity="1"
                :model-value="classroom.progress"
              >
                <template #default>
                  <strong>{{ Math.ceil(classroom.progress) }}%</strong>
                </template>
              </v-progress-linear>
            </v-card-text>
            <v-card-actions>
              <SecundaryButton buttonName="Go to Room" class="d-flex flex-fill elevation-2">
              </SecundaryButton>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </DefaultLayout>
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
