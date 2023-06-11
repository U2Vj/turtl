<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import Footer from '@/components/Footer.vue'
import TemplateCard from '@/components/TemplateCard.vue'
import { ref, toRef } from 'vue'
import { useSortable, moveArrayElement } from '@vueuse/integrations/useSortable'
import { VDataTable } from 'vuetify/labs/VDataTable'
import { useTemplateStore } from '@/stores/TemplateStore'
import { watchEffect } from 'vue'
import AddProjectTemplateModal from '@/components/modals/AddProjectTemplateModal.vue'
import AddInstructorModal from '@/components/modals/AddInstructorModal.vue'

const props = defineProps<{ templateId: string }>()

const tab = ref(0)
const showCreateModal = ref(false)

const templateStore = useTemplateStore()

let templateData = toRef(templateStore, 'classroomTemplate')
templateStore.fetchTemplate(props.templateId)

watchEffect(() => {
  if (!templateData.value) return

  useSortable('#cardWrapper', templateData.value.projects, {
    animation: 300,
    onUpdate: (event: any) => {
      if (!templateData.value) return
      const copyTemplateDataProjects = templateData.value.projects.slice()
      moveArrayElement(copyTemplateDataProjects, event.oldIndex, event.newIndex)
      templateData.value.projects = copyTemplateDataProjects
    }
  })
})

function handleUpdateTaskOrder(projectId: string, event: any) {
  if (!templateData.value) {
    return
  }
  const project = templateData.value.projects.find((project) => {
    if (project.id == projectId) {
      return true
    }
  })
  if (!project) {
    return
  }
  moveArrayElement(project.tasks, event.oldIndex, event.newIndex)
}
</script>

<template>
  <turtl-header></turtl-header>
  <v-main v-if="templateData">
    <v-container fluid>
      <v-row>
        <v-col>
          <h1>{{ templateData.templateName }}</h1>
          <v-tabs v-model="tab" color="primary">
            <v-tab value="0">Projects and Settings</v-tab>
            <v-tab value="1">Information</v-tab>
            <v-tab value="2">Instructors</v-tab>
          </v-tabs>
          <v-window v-model="tab" class="mt-5">
            <v-window-item eager value="0">
              <div class="d-flex">
                <h2>Project Templates</h2>
                <v-btn
                  prepend-icon="mdi-plus"
                  color="primary"
                  class="ml-10"
                  @click="showCreateModal = true"
                >
                  Add Project Template
                  <AddProjectTemplateModal></AddProjectTemplateModal>
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
                          <div>Template Name:</div>
                          <div>Template ID:</div>
                          <div>Created At:</div>
                        </div>
                        <div class="ml-auto">
                          <div>{{ templateData.templateName }}</div>
                          <div>{{ templateData.templateId }}</div>
                          <div>{{ templateData.creationDate }}</div>
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
                  Add Instructors
                  <AddInstructorModal></AddInstructorModal>
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
                <template #[`item.remove`]>
                  <v-btn icon="mdi-trash-can-outline" variant="text" />
                </template>
              </v-data-table>
            </v-window-item>
          </v-window>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
  <Footer></Footer>
</template>
