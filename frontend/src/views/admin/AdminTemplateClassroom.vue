<script setup lang="ts">
import TemplateCard from '@/components/TemplateCard.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import ErrorButton from '@/components/layouts/ErrorButton.vue'
import PrimaryButton from '@/components/layouts/PrimaryButton.vue'
import AddManagerModal from '@/components/modals/AddManagerModal.vue'
import AddProjectTemplateModal from '@/components/modals/AddProjectTemplateModal.vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { moveArrayElement, useSortable } from '@vueuse/integrations/useSortable'
import { ref, toRef, watchEffect } from 'vue'

const props = defineProps<{ templateId: string }>()
const tab = ref(0)
const showCreateModal = ref(false)

const templateStore = useTemplateStore()

let templateData = toRef(templateStore, 'classroomTemplate')
templateStore.fetchTemplate(props.templateId)

watchEffect(() => {
  if (!templateData.value) return

  useSortable('#cardWrapper', templateData.value.project_templates, {
    animation: 300,
    onUpdate: (event: any) => {
      if (!templateData.value) return
      const copyTemplateDataProjects = templateData.value.project_templates.slice()
      moveArrayElement(copyTemplateDataProjects, event.oldIndex, event.newIndex)
      templateData.value.project_templates = copyTemplateDataProjects
    }
  })
})

function handleUpdateTaskOrder(projectId: string, event: any) {
  if (!templateData.value) {
    return
  }
  const project = templateData.value.project_templates.find((project_templates) => {
    if (project_templates.id == projectId) {
      return true
    }
  })
  if (!project) {
    return
  }
  moveArrayElement(project.task_templates, event.oldIndex, event.newIndex)
}
</script>

<template>
  <DefaultLayout v-if="templateData">
    <template #heading>{{ templateData.title }}</template>
    <template #default>
      <v-tabs v-model="tab" color="primary">
        <v-tab value="0">Projects and Settings</v-tab>
        <v-tab value="1">Information</v-tab>
        <v-tab value="2">Managers</v-tab>
      </v-tabs>
      <v-window v-model="tab" class="mt-5">
        <v-window-item eager value="0">
          <v-container fluid>
            <div class="d-flex flex-row mb-2 align-center justify-space-between">
              <h2>Project Templates</h2>
              <PrimaryButton buttonName="Add Project Template" @atClick="showCreateModal = true">
                <AddProjectTemplateModal />
              </PrimaryButton>
            </div>
            <div id="cardWrapper">
              <template-card
                v-for="project in templateData.project_templates"
                :template-id="props.templateId"
                :key="project.id"
                :project-id="project.id"
                :title="project.title"
                :taskTemplates="project.task_templates"
                @update:task_template="handleUpdateTaskOrder"
                class="mt-5"
              ></template-card>
            </div>
          </v-container>
        </v-window-item>
        <v-window-item value="1">
          <v-container fluid>
            <v-row>
              <v-col cols="6">
                <div>
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title> Generell Information </v-card-title>
                    <v-card-text>
                      <div><h3>Template Name:</h3></div>
                      <div>{{ templateData.title }}</div>
                      <div class="mt-5"><h3>Template ID:</h3></div>
                      <div>{{ templateData.id }}</div>

                      <div class="mt-5"><h3>Created At:</h3></div>
                      <div>{{ templateData.created_at }}</div>

                      <div class="mt-5"><h3>Updated At:</h3></div>
                      <div>{{ templateData.updated_at }}</div>
                    </v-card-text>
                  </v-card>
                </div>
                <div class="mt-5">
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>Helpful resources</v-card-title>
                    <v-card-text>
                      <div
                        v-for="(resource, index) in templateData.helpful_resources"
                        :key="resource.id"
                      >
                        <a :href="resource.url">
                          {{ `${index + 1}. ${resource.title}` }}
                        </a>
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
              <v-col cols="6">
                <div>
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>Permanently Delete Template</v-card-title>
                    <v-card-actions>
                      <ErrorButton buttonName="Delete Template"></ErrorButton>
                    </v-card-actions>
                  </v-card>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-window-item>
        <v-window-item value="2">
          <v-container fluid>
            <div class="d-flex flex-row mb-2 align-center justify-space-between">
              <h2>Managers</h2>
              <PrimaryButton buttonName="Add Managers">
                <AddManagerModal />
              </PrimaryButton>
            </div>
            <v-data-table
              :headers="[
                { title: 'E-Mail', key: 'email' },
                { title: 'Name', key: 'name' },
                { title: 'Remove', key: 'remove' }
              ]"
              :items="templateData.managers"
            >
              <template #[`item.remove`]>
                <v-btn icon="mdi-trash-can-outline" variant="text" />
              </template>
            </v-data-table>
          </v-container>
        </v-window-item>
      </v-window>
    </template>
  </DefaultLayout>
</template>

<style scoped></style>
