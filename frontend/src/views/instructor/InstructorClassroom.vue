<script setup lang="ts">
import ProjectCard from '@/components/ProjectCard.vue'
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import AddHelpfulResourceModal from '@/components/modals/AddHelpfulResourceModal.vue'
import AddInstructorModal from '@/components/modals/AddInstructorModal.vue'
import AddProjectModal from '@/components/modals/AddProjectModal.vue'
import DeleteClassroomModal from '@/components/modals/DeleteClassroomModal.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import dayjs from 'dayjs'
import { ref, toRaw, toRef } from 'vue'
import { useToast } from 'vue-toastification'

const props = defineProps<{ classroomId: number }>()
const tab = ref(0)

const catalogStore = useCatalogStore()
const toast = useToast()

let classroom = toRef(catalogStore, 'classroom')

catalogStore.getClassroom(props.classroomId).catch((e) => {
  toast.error(e.message)
})

const formatDate = (datetime: string) => {
  return dayjs(datetime).format('DD.MM.YYYY HH:mm')
}

function deleteHelpfulResource(id: number) {
  if (!classroom.value) {
    return
  }
  const updatedClassroom = Object.assign({}, toRaw(classroom.value))
  updatedClassroom.helpful_resources = updatedClassroom.helpful_resources.filter(
    (resource) => resource.id !== id
  )
  catalogStore
    .updateClassroom(classroom.value.id, updatedClassroom)
    .catch((e) => toast.error(e.message))
}

function editClassroomTitle(newTitle: string) {
  if (!classroom.value) {
    return
  }
  const updatedTitle = Object.assign({}, toRaw(classroom.value))
  updatedTitle.title = newTitle
  catalogStore
    .updateClassroom(classroom.value.id, updatedTitle)
    .catch((e) => toast.error(e.message))
}
</script>

<template>
  <DefaultLayout v-if="classroom">
    <template #heading>{{ classroom.title }}</template>
    <template #default>
      <v-text-field
        label="Edit Title"
        clearable
        variant="underlined"
        base-color="primary"
        color="primary"
        v-model="classroom.title"
      ></v-text-field>
      <PrimaryButton
        button-name="Save Title"
        @click="editClassroomTitle(classroom.title)"
      ></PrimaryButton>
      <v-tabs v-model="tab" color="primary">
        <v-tab value="0">Projects</v-tab>
        <v-tab value="1">Settings</v-tab>
        <v-tab value="2">Instructors</v-tab>
      </v-tabs>
      <v-window v-model="tab" class="mt-5">
        <v-window-item eager value="0">
          <v-container fluid>
            <div class="d-flex flex-row mb-2 align-center justify-space-between">
              <h2>Projects</h2>
              <PrimaryButton buttonName="Add Project">
                <AddProjectModal />
              </PrimaryButton>
            </div>
            <div>
              <project-card
                v-for="project in classroom.projects"
                :classroom-id="props.classroomId"
                :key="project.id"
                :project-id="project.id"
                :project-title="project.title"
                :tasks="project.tasks"
                class="mt-5"
              ></project-card>
              <p class="mt-3" v-if="!classroom.projects.length">
                This classroom does not contain any projects yet.
              </p>
            </div>
          </v-container>
        </v-window-item>
        <v-window-item value="1">
          <v-container fluid>
            <v-row>
              <v-col cols="6">
                <div>
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>Stats</v-card-title>
                    <v-card-text>
                      <div><h3>Created at:</h3></div>
                      <div>{{ formatDate(classroom.created_at) }}</div>

                      <div class="mt-5"><h3>Updated at:</h3></div>
                      <div>{{ formatDate(classroom.updated_at) }}</div>
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
                              title: 'Title',
                              align: 'start',
                              key: 'title'
                            },
                            {
                              title: 'URL',
                              align: 'start',
                              key: 'url'
                            },
                            {
                              title: 'Delete',
                              key: 'id'
                            }
                          ]"
                          :items="classroom.helpful_resources"
                          no-data-text="This Classroom does not contain any Helpful Resources yet."
                        >
                          <template #[`item.url`]="{ item }">
                            <a :href="item.columns.url" target="_blank">{{ item.columns.url }}</a>
                          </template>
                          <template #[`item.id`]="{ item }">
                            <v-btn
                              icon="mdi-trash-can-outline"
                              variant="text"
                              @click="deleteHelpfulResource(item.columns.id)"
                            />
                          </template>
                        </v-data-table>
                      </div>
                      <div class="mt-5">
                        <SecondaryButton buttonName="Add Resource">
                          <AddHelpfulResourceModal :classroom-id="props.classroomId" />
                        </SecondaryButton>
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
              <v-col cols="6">
                <div>
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>Delete Classroom</v-card-title>
                    <v-card-actions>
                      <ErrorButton buttonName="Delete Classroom">
                        <DeleteClassroomModal :classroom-id="props.classroomId" />
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
              <h2>Instructors</h2>
              <PrimaryButton buttonName="Add Instructors">
                <AddInstructorModal />
              </PrimaryButton>
            </div>
            <v-data-table
              :headers="[
                { title: 'E-Mail', key: 'instructor.email' },
                { title: 'Username', key: 'instructor.username' },
                { title: 'Remove', key: 'remove' }
              ]"
              :items="classroom.instructors"
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
