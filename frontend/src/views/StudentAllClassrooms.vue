<script setup lang="ts">
import { ref } from 'vue'
import TurtlHeader from '@/components/TurtlHeader.vue'
import Footer from '@/components/Footer.vue'

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
  <turtl-header></turtl-header>
  <v-main class="d-flex justify-center">
    <div class="main-container mt-5 ml-3 mr-3">
      <v-container fluid>
        <h1>All Classrooms</h1>
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
              <template v-slot:top>
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
                      <v-btn variant="text" color="primary" @click="close"> Cancel </v-btn>
                      <v-btn variant="elevated" color="primary" class="elevation-2" @click="join">
                        Join Classroom
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </template>
              <template #item.actions="{ item }">
                <v-btn
                  variant="tonal"
                  color="primary"
                  class="elevation-2"
                  @click="joinClassroomBtn(item.raw)"
                  >Join classroom</v-btn
                >
              </template>
              <template v-slot:no-data>
                <p>No data</p>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </v-main>
  <Footer></Footer>
</template>

<style>
.main-container {
  min-width: 75%;
  max-width: 960px;
}
</style>
