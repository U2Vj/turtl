<script setup lang="ts">
import { makeAPIRequest } from '@/communication/APIRequests'
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import ProjectCard from '@/components/layouts/ProjectCard.vue'
import AddHelpfulResourceModal from '@/components/modals/AddHelpfulResourceModal.vue'
import AddInstructorModal from '@/components/modals/AddInstructorModal.vue'
import AddProjectModal from '@/components/modals/AddProjectModal.vue'
import DeleteClassroomModal from '@/components/modals/DeleteClassroomModal.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { useUserStore } from '@/stores/UserStore'
import dayjs from 'dayjs'
import type { Ref } from 'vue'
import { onMounted, ref, toRaw, toRef } from 'vue'
import { useToast } from 'vue-toastification'

const props = defineProps<{ classroomId: number }>()
const tab = ref(0)
const catalogStore = useCatalogStore()
const toast = useToast()
const breadcrumbItems: Ref<any[]> = ref([])
const currentInstructorId = ref()
const showDialog = ref(false)
const userStore = useUserStore()

let classroom = toRef(catalogStore, 'classroom')

catalogStore
  .getClassroom(props.classroomId)
  .then(() => {
    breadcrumbItems.value = [
      {
        title: 'My Classrooms',
        disabled: false,
        to: {
          name: 'InstructorMyClassrooms'
        }
      },
      {
        title: classroom.value?.title,
        disabled: true
      }
    ]
  })
  .catch((e) => {
    toast.error(e.message)
  })

const formatDate = (datetime: string) => {
  return dayjs(datetime).format('DD.MM.YYYY')
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
    .then(() => toast.info("Resource deleted"))
    .catch((e) => toast.error(e.message))
}

const hasClassroomTitleChanged = ref(false)
const classroomTitleJustSaved = ref(false)

const classroomTitle = ref(classroom.value?.title)

function onClassroomTitleInputChange() {
  hasClassroomTitleChanged.value = classroomTitle.value !== classroom.value?.title
  if (hasClassroomTitleChanged.value) {
    classroomTitleJustSaved.value = false
  }
}

function editClassroomTitle(newTitle: string) {
  if (!classroom.value) {
    return
  }

  const updatedTitle = Object.assign({}, toRaw(classroom.value))
  updatedTitle.title = newTitle

  catalogStore
    .updateClassroom(classroom.value.id, updatedTitle)
    .then(() => {
      toast.success('Classroom title changed')
      classroomTitleJustSaved.value = true
    })
    .catch((e) => {
      toast.error(e.message)
    })
}

async function getEnrolledStudents(classroomId: number) {
  try {
    const response = await makeAPIRequest(
      `/enrollments/for-classroom/${classroomId}`,
      'GET',
      true,
      true
    )
    return response.data
  } catch (e: any) {
    toast.error(e.message)
  }
}

function confirmInstructorRemoval(instructorId: number) {
  currentInstructorId.value = instructorId
  showDialog.value = true
}

const enrolledStudents = ref([])

onMounted(async () => {
  enrolledStudents.value = await getEnrolledStudents(props.classroomId)
})
</script>

<template>
  <DefaultLayout v-if="classroom" :breadcrumb-items="breadcrumbItems">
    <template #heading>{{ classroom.title }}</template>
    <template #default>
      <v-text-field
        label="Edit Title"
        clearable
        variant="underlined"
        base-color="primary"
        color="primary"
        v-model="classroom.title"
        @input="onClassroomTitleInputChange"
      ></v-text-field>
      <PrimaryButton
        button-name="Save Title"
        :disabled="!hasClassroomTitleChanged || classroomTitleJustSaved"
        @click="editClassroomTitle(classroom.title)"
      ></PrimaryButton>
      <br /><br />
      <v-tabs v-model="tab" color="primary">
        <v-tab value="0">Projects</v-tab>
        <v-tab value="1">Settings</v-tab>
        <v-tab value="2">Instructors</v-tab>
        <v-tab value="3">Students</v-tab>
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
                          no-data-text="This classroom does not contain any helpful resources yet."
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
                { title: 'Added at', key: 'added_at' },
                { title: 'Added by', key: 'added_by.email' },
                { title: 'Remove', key: 'remove' }
              ]"
              :items="classroom.instructors"
            >
              <template #[`item.added_at`]="{ item }">{{ formatDate(item.raw.added_at) }}</template>
              <template #[`item.remove`]="{ item }">
                <v-btn
                  icon="mdi-trash-can-outline"
                  variant="text"
                  @click="
                    () => {
                      if (item.raw.instructor.id === userStore.user?.id) {
                        confirmInstructorRemoval(item.raw.instructor.id)
                      } else {
                        catalogStore
                          .removeInstructor(item.raw.instructor.id)
                          .then(() => toast.info('Instructor removed'))
                          .catch((e) => toast.error(e.message))
                      }
                    }
                  "
                />
                <v-dialog v-model="showDialog">
                  <v-card>
                    <v-card-title>Delete Task</v-card-title>
                    <v-card-text>
                      <p>Are you sure you want to remove yourself from this classroom?</p>
                    </v-card-text>
                    <v-card-actions>
                      <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
                      <PrimaryButton
                        buttonName="Delete"
                        @click="
                          () => {
                            catalogStore
                              .removeInstructor(currentInstructorId)
                              .then(() => toast.info('Instructor removed'))
                              .catch((e) => toast.error(e.message))
                            showDialog = false
                            $router.push({
                              name: 'InstructorMyClassrooms'
                            })
                          }
                        "
                      ></PrimaryButton>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </template>
            </v-data-table>
          </v-container>
        </v-window-item>
        <v-window-item value="3">
          <v-container fluid>
            <div class="d-flex flex-row mb-2 align-center justify-space-between">
              <h2>Enrolled Students</h2>
            </div>
            <v-data-table
              :headers="[
                { title: 'E-Mail', key: 'student.email' },
                { title: 'Username', key: 'student.username' },
                { title: 'Date Enrolled', key: 'date_enrolled' },
                { title: 'Progress', key: 'progress' }
              ]"
              :items="enrolledStudents"
              item-key="id"
              no-data-text="There are no students who are currently enrolled in this classroom."
            >
              <template #[`item.date_enrolled`]="{ item }">{{
                formatDate(item.raw.date_enrolled)
              }}</template>
              <template #[`item.progress`]="{ item }"> {{ item.raw.progress }}&percnt; </template>
            </v-data-table>
          </v-container>
        </v-window-item>
      </v-window>
    </template>
  </DefaultLayout>
  <div v-else class="center-screen">
    <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
  </div>
</template>

<style scoped>
.center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
