<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import PrimaryButton from '@/components/layouts/PrimaryButton.vue'
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
</script>

<template>
  <DefaultLayout>
    <template #heading>My Classrooms</template>
    <template #postHeadingButton>
      <PrimaryButton buttonName="Join Classroom" goTo="/allclassrooms-stud"> </PrimaryButton>
    </template>
    <template #default>
      <v-row>
        <v-col v-for="item in items" :key="item.id" cols="12" xs="12" sm="6" md="4">
          <v-card
            :key="item.id"
            :title="item.room"
            :subtitle="item.manager_name"
            variant="elevated"
            class="elevation-4"
            color="cardColor"
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
                :color="item.progress === 100 ? 'finished' : 'progress'"
                :height="25"
                :model-value="item.progress"
                rounded
                rounded-bar
                bg-color="#ffffff"
                bg-opacity="1"
              >
                <template #default>
                  <strong>{{ Math.ceil(item.progress) }}%</strong>
                </template>
              </v-progress-linear>
            </v-card-text>
            <v-card-actions>
              <v-btn
                variant="tonal"
                color="primary"
                to="StudentClassProjects"
                class="d-flex flex-fill elevation-2"
                >Visit Classroom</v-btn
              >
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </DefaultLayout>
</template>

<style scoped></style>
