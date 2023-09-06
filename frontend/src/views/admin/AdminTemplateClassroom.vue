<script setup lang="ts">
import TemplateCard from '@/components/TemplateCard.vue'
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import AddManagerModal from '@/components/modals/AddManagerModal.vue'
import AddProjectTemplateModal from '@/components/modals/AddProjectTemplateModal.vue'
import AddResourceModal from '@/components/modals/AddResourceModal.vue'
import DeleteClassroomResourceModal from '@/components/modals/DeleteClassroomResourceModal.vue'
import DeleteClassroomTemplateModal from '@/components/modals/DeleteClassroomTemplateModal.vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { moveArrayElement, useSortable } from '@vueuse/integrations/useSortable'
import { ref, toRef, watchEffect } from 'vue'

const props = defineProps<{ templateId: string }>()
const tab = ref(0)
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const showResourceModal = ref(false)

const templateStore = useTemplateStore()

let templateData = toRef(templateStore, 'classroomTemplate')
templateStore.fetchTemplate(props.templateId)

const formatDate = (datetime: string) => {
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }
  const formattedDate = new Date(datetime).toLocaleDateString('de-DE', options)
  return formattedDate.replace(',', ' um')
}

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
              <PrimaryButton buttonName="Add Project Template" @click="showCreateModal = true">
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
                      <div>{{ formatDate(templateData.created_at) }}</div>

                      <div class="mt-5"><h3>Updated At:</h3></div>
                      <div>{{ formatDate(templateData.updated_at) }}</div>
                    </v-card-text>
                  </v-card>
                </div>
                <div class="mt-5">
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>Helpful resources</v-card-title>
                    <v-card-text>
                      <div>
                        <v-data-table
                          :headers="[
                            {
                              title: 'Name',
                              align: 'start',
                              key: 'title'
                            },
                            {
                              title: 'Link',
                              align: 'start',
                              key: 'url'
                            },
                            {
                              title: 'Delete',
                              align: 'center',
                              key: 'link'
                            }
                          ]"
                          :items="templateData.helpful_resources"
                        >
                          <template v-slot:item.url="{ item }">
                            <a :href="item.columns.url" target="_blank">{{ item.columns.url }}</a>
                          </template>

                          <template #[`item.link`]="{ item }">
                            <TextButton buttonName="Delete">
                              <DeleteClassroomResourceModal :resourceId="item.columns.id" />
                            </TextButton>
                          </template>
                        </v-data-table>
                      </div>
                      <div class="mt-5">
                        <SecondaryButton
                          buttonName="Add Resource"
                          @click="showResourceModal = true"
                        >
                          <AddResourceModal :templateId="props.templateId" />
                        </SecondaryButton>
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
                      <ErrorButton buttonName="Delete Template" @click="showDeleteModal = true">
                        <DeleteClassroomTemplateModal :templateId="props.templateId" />
                      </ErrorButton>
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
