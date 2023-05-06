<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import TemplateCard from '@/components/TemplateCard.vue'
import { ref } from 'vue'
import { useSortable, moveArrayElement } from '@vueuse/integrations/useSortable'
import { VDataTable } from 'vuetify/labs/VDataTable'

const tab = ref(0)

const templateData = ref({
  name: 'Computer Networks',
  projects: [
    {
      id: '0',
      name: 'Computer Network Project 1',
      tasks: [
        { id: '0', name: 'task 1 name' },
        { id: '1', name: 'task 2 name' }
      ]
    },
    {
      id: '1',
      name: 'Computer Network Project 2',
      tasks: [
        { id: '0', name: 'task 1 name' },
        { id: '1', name: 'task 2 name' }
      ]
    }
  ],
  generelInformation: {
    id: '12',
    classroomName: 'Computer Networks',
    creationDate: '2022.01.11'
  },
  resources: [
    { id: '0', name: 'moodle course', link: 'https://www.google.com' },
    { id: '1', name: 'Introduction to DHCP', link: 'https://www.google.com' }
  ],
  instructors: [
    { name: 'John Doe', email: 'john.doe@mailservice.com' },
    { name: 'John Doe2', email: 'john.doe2@mailservice.com' }
  ]
})

function handleUpdateTaskOrder(projectId: string, event: any) {
  const project = templateData.value.projects.find((project) => {
    return project.id === projectId
  })
  const tasks = project?.tasks
  if (tasks) {
    moveArrayElement(tasks, event.oldIndex, event.newIndex)
  }
}

useSortable('#cardWrapper', templateData.value.projects, {
  animation: 300
})
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col>
          <h1>{{ templateData.name }}</h1>
          <v-tabs v-model="tab" color="primary">
            <v-tab value="0">Projects and Settings</v-tab>
            <v-tab value="1">Information</v-tab>
            <v-tab value="2">Instructors</v-tab>
          </v-tabs>
          <v-window v-model="tab" class="mt-5">
            <v-window-item eager value="0">
              <div class="d-flex">
                <h2>Project Templates</h2>
                <v-btn prepend-icon="mdi-plus" color="primary" class="ml-10">
                  Add Project Template
                </v-btn>
              </div>
              <div id="cardWrapper">
                <template-card
                  v-for="project in templateData.projects"
                  :key="project.id"
                  :project-id="project.id"
                  :name="project.name"
                  :tasks="project.tasks"
                  @update:tasks="handleUpdateTaskOrder"
                  class="mt-5"
                ></template-card>
              </div>
            </v-window-item>
            <v-window-item value="1">
              <h2>Information</h2>
              <v-container fluid class="pa-0">
                <v-row>
                  <v-col md="3">
                    <v-card color="grey-lighten-4" class="mt-5 pa-5">
                      <h3>Generell Information</h3>
                      <div class="d-flex">
                        <div>
                          <div>Classroom Name:</div>
                          <div>Classroom ID:</div>
                          <div>Created At:</div>
                        </div>
                        <div class="ml-auto">
                          <div>{{ templateData.generelInformation.classroomName }}</div>
                          <div>{{ templateData.generelInformation.id }}</div>
                          <div>{{ templateData.generelInformation.creationDate }}</div>
                        </div>
                      </div>
                    </v-card>
                    <v-card color="grey-lighten-4" class="mt-5 pa-5">
                      <h3>Helpful resources</h3>
                      <div v-for="(resource, index) in templateData.resources" :key="resource.id">
                        <a :href="resource.link">
                          {{ `${index + 1}. ${resource.name}` }}
                        </a>
                      </div>
                    </v-card>
                  </v-col>
                  <v-col md="3" offset-md="2">
                    <v-card color="grey-lighten-4" class="mt-5 pa-5">
                      <h3>Export</h3>
                      <v-btn color="primary">Export Classroom Template</v-btn>
                    </v-card>
                    <v-card color="grey-lighten-4" class="mt-5 pa-5">
                      <h3>Delete</h3>
                      <v-btn color="error">Permanently Delete Template</v-btn>
                    </v-card>
                  </v-col>
                </v-row>
              </v-container>
            </v-window-item>
            <v-window-item value="2"
              ><div class="d-flex">
                <h2>Instructors</h2>
                <v-btn prepend-icon="mdi-plus" color="primary" class="ml-10">
                  Add Instructor
                </v-btn>
              </div>
              <v-data-table
                :headers="[
                  { title: 'E-Mail', key: 'email' },
                  { title: 'Name', key: 'name' },
                  { title: 'Remove', key: 'remove' }
                ]"
                :items="templateData.instructors"
              >
                <template v-slot:[`item.remove`]>
                  <v-btn icon="mdi-trash-can-outline" variant="text" />
                </template>
              </v-data-table>
            </v-window-item>
          </v-window>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>
