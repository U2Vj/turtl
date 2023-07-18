<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import PrimaryButton from '@/components/layouts/PrimaryButton.vue'
import SecundaryButton from '@/components/layouts/SecundaryButton.vue'
import TextButton from '@/components/layouts/TextButton.vue'
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

function close() {
  dialog.value = false
}

function join() {
  dialog.value = false
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
            <template #top>
              <v-dialog v-model="dialog" persistent width="50%">
                <v-card>
                  <v-toolbar :title="selectedClassroomName"> </v-toolbar>
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
                          <v-text-field
                            label="Enter Code"
                            clearable
                            variant="underlined"
                            base-color="primary"
                            color="primary"
                          ></v-text-field>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <TextButton buttonName="Cancel" @atClick="close"></TextButton>
                    <PrimaryButton buttonName="Join Classroom" @atClick="join"> </PrimaryButton>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </template>
            <template #[`item.actions`]="{ item }">
              <SecundaryButton buttonName="Join Classroom" @atClick="joinClassroomBtn(item.raw)">
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
