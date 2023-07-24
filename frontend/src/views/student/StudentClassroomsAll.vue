<script setup lang="ts">
import SecundaryButton from '@/components/buttons/SecondaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import JoinClassroomModal from '@/components/modals/JoinClassroomModal.vue'
import { ref } from 'vue'

const search = ref('')
const dialog = ref(false)
const headers = [
  { title: 'Name of Classroom', key: 'name_classroom' },
  { title: 'Manager', key: 'manager_name' },
  { title: '', key: 'actions', width: '10%', sortable: false }
]

const classrooms = [
  {
    name_classroom: 'Test Networks',
    manager_name: 'John Doe'
  },
  {
    name_classroom: 'Computer Networks',
    manager_name: 'Tom Doe'
  },
  {
    name_classroom: 'Secure Networks',
    manager_name: 'Finn Doe'
  }
]

const selectedClassroom = ref({})

const selectedClassroomName = ref('')

function joinClassroomBtn(item: any) {
  selectedClassroom.value = item
  selectedClassroomName.value = item.name_classroom
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
            label="Search Name of Classroom"
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
            item-value="classTemplates"
          >
            <template #top> </template>
            <template #[`item.actions`]="{ item }">
              <SecundaryButton buttonName="Join Classroom" @click="joinClassroomBtn(item.raw)">
                <JoinClassroomModal>
                  <template #classroomName>{{ selectedClassroomName }}</template>
                </JoinClassroomModal>
              </SecundaryButton>
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
