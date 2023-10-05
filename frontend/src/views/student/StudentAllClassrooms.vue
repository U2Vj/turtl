<script setup lang="ts">
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import JoinClassroomModal from '@/components/modals/JoinClassroomModal.vue'
import { ref } from 'vue'

const search = ref('')
const dialog = ref(false)
const headers = [
  { title: 'Title', key: 'title' },
  { title: 'Instructors', key: 'instructors' },
  { title: '', key: 'actions', width: '10%', sortable: false }
]

const classrooms = [
  {
    title: 'Test Networks',
    instructors: 'John Doe'
  },
  {
    title: 'Computer Networks',
    instructors: 'Tom Doe'
  },
  {
    title: 'Secure Networks',
    instructors: 'Finn Doe'
  }
]

const selectedClassroom = ref({})

const selectedClassroomTitle = ref('')

function joinClassroomBtn(item: any) {
  selectedClassroom.value = item
  selectedClassroomTitle.value = item.title
  dialog.value = true
}
</script>

<template>
  <DefaultLayout>
    <template #heading>All Classrooms</template>
    <template #default>
      <v-row>
        <v-col cols="8">
          <v-text-field
            clearable
            label="Search title of Classroom"
            v-model="search"
            append-inner-icon="mdi-magnify"
            variant="underlined"
            base-color="primary"
            color="primary"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" xs="12" sm="12" md="12">
          <v-data-table
            :headers="headers"
            :items="classrooms"
            :search="search"
            item-value="classrooms"
          >
            <template #top> </template>
            <template #[`item.actions`]="{ item }">
              <SecondaryButton buttonName="Join Classroom" @click="joinClassroomBtn(item.raw)">
                <JoinClassroomModal>
                  <template #classroomName>{{ selectedClassroomTitle }}</template>
                </JoinClassroomModal>
              </SecondaryButton>
            </template>
            <template #no-data>
              <p>No data</p>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </template>
  </DefaultLayout>
</template>

<style></style>
