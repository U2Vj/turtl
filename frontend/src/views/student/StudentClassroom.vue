<script setup lang="ts">
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import VisitLinkModal from '@/components/modals/VisitLinkModal.vue'
import type { ClassroomStudent, EnrollmentDetail } from '@/stores/EnrollmentStore'
import { useEnrollmentStore } from '@/stores/EnrollmentStore'
import type { Ref } from 'vue'
import { ref, toRef } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const props = defineProps<{ enrollmentId: number }>()
const enrollmentStore = useEnrollmentStore()
const enrollment: Ref<EnrollmentDetail | undefined> = toRef(enrollmentStore, 'enrollment')
const toast = useToast()
const router = useRouter()

const tab = ref(null)

enrollmentStore
  .getEnrollment(props.enrollmentId)
  .then((result) => {
    enrollment.value = result
  })
  .catch((e) => toast.error(e.message))

function unenroll() {
  if (!enrollment.value) return
  enrollmentStore
    .unenroll(enrollment.value.id)
    .then(async () => {
      toast.info(`You have unenrolled from '${enrollment.value?.classroom.title}'`)
      await router.push({ name: 'StudentMyEnrollments' })
    })
    .catch((e) => toast.error(e.message))
}

function getTasksInClassroom(classroom: ClassroomStudent) {
  return classroom.projects.map((project) => project.tasks).flat(1)
}

function getTasksDone(): number {
  if (!enrollment.value) return 0
  const tasks = getTasksInClassroom(enrollment.value.classroom)
  return tasks.filter((task) => task.done).length
}
function getTasksTotal(): number {
  if (!enrollment.value) return 0
  return getTasksInClassroom(enrollment.value.classroom).length
}

function getTasksDonePercentage(): number {
  const doneTasks = getTasksDone()
  const totalTasks = getTasksTotal()
  if (totalTasks === 0) {
    return 100
  }

  return Math.round((doneTasks / totalTasks) * 100)
}

function getProjectsDone(): number {
  if (!enrollment.value) return 0
  return enrollment.value.classroom.projects.filter(
    (project) => !project.tasks.some((task) => !task.done)
  ).length
}
function getProjectsTotal(): number {
  if (!enrollment.value) return 0
  return enrollment.value.classroom.projects.length
}
function getProjectsDonePercentage(): number {
  const doneProjects = getProjectsDone()
  const totalProjects = getProjectsTotal()
  if (totalProjects === 0) {
    return 100
  }

  return Math.round((doneProjects / totalProjects) * 100)
}
</script>

<template>
  <DefaultLayout v-if="enrollment">
    <template #heading>{{ enrollment.classroom.title }}</template>
    <template #default>
      <v-tabs v-model="tab" color="primary" align-tabs="start">
        <v-tab value="1">Projects</v-tab>
        <v-tab value="2">Information</v-tab>
      </v-tabs>
      <v-window v-model="tab">
        <v-window-item value="1">
          <v-container>
            <v-row>
              <v-col
                v-for="project in enrollment.classroom.projects"
                :key="project.id"
                cols="12"
                xs="12"
                sm="6"
                md="4"
              >
                <v-card
                  :key="project.id"
                  :title="project.title"
                  variant="flat"
                  color="cardColor"
                  class="elevation-4"
                >
                  <v-card-text>
                    <v-progress-linear
                      color="progress"
                      :height="25"
                      rounded
                      rounded-bar
                      bg-color="#ffffff"
                      bg-opacity="1"
                      :model-value="project.progress"
                    >
                      <template #default>
                        <strong>{{ project.progress }}&percnt;</strong>
                      </template>
                    </v-progress-linear>
                  </v-card-text>
                  <v-card-text>
                    <div v-for="task in project.tasks" :key="task.id">
                      <TextButton
                        :button-name="task.title"
                        :go-to="`/student/enrollments/${enrollmentId}/tasks/${task.id}`"
                      ></TextButton>
                      <v-icon
                        v-if="task.done"
                        icon="mdi-check-circle-outline"
                        color="success"
                      ></v-icon>
                    </div>
                    <p v-if="project.tasks.length === 0">
                      This project does not contain any tasks.
                    </p>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col v-if="getProjectsTotal() === 0">
                <p>This classroom does not contain any projects yet.</p>
              </v-col>
            </v-row>
          </v-container>
        </v-window-item>

        <v-window-item value="2">
          <v-container>
            <v-row>
              <v-col cols="6">
                <div>
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>Instructors</v-card-title>
                    <v-card-text>
                      <div v-for="(instructor, index) in enrollment.classroom.instructors">
                        <a :href="`mailto:${instructor.email}`">
                          <span v-if="instructor.username"
                            >{{ instructor.username }} &lt;{{ instructor.email }}&gt;</span
                          >
                          <span v-else>{{ instructor.email }}</span>
                          <span v-if="!(index === enrollment.classroom.instructors.length - 1)"
                            >,</span
                          >
                        </a>
                      </div>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
              <v-col cols="6">
                <div>
                  <v-card variant="flat" color="cardColor" class="elevation-4">
                    <v-card-title>My Progress</v-card-title>
                    <v-card-text>
                      {{ getTasksDone() }} / {{ getTasksTotal() }} Tasks Done:

                      <v-progress-linear
                        color="progress"
                        :height="25"
                        :model-value="getTasksDonePercentage()"
                        rounded
                        rounded-bar
                        bg-color="#ffffff"
                        bg-opacity="1"
                      >
                        <template #default>
                          <strong>{{ getTasksDonePercentage() }}&percnt;</strong>
                        </template>
                      </v-progress-linear>

                      {{ getProjectsDone() }} / {{ getProjectsTotal() }} Projects Done

                      <v-progress-linear
                        :height="25"
                        rounded
                        rounded-bar
                        bg-color="#ffffff"
                        bg-opacity="1"
                        color="progress"
                        :model-value="getProjectsDonePercentage()"
                      >
                        <template #default>
                          <strong>{{ getProjectsDonePercentage() }}&percnt;</strong>
                        </template>
                      </v-progress-linear>
                    </v-card-text>
                  </v-card>
                </div>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="6">
                <v-card variant="flat" color="cardColor" class="elevation-4">
                  <v-card-title>Helpful Resources</v-card-title>
                  <v-card-subtitle
                    >These are helpful links that your instructors provided.</v-card-subtitle
                  >
                  <v-card-text>
                    <v-list bg-color="cardColor" base-color="primary">
                      <v-list-item v-for="resource in enrollment.classroom.helpful_resources">
                        <v-list-item-title style="cursor: pointer">
                          <v-icon icon="mdi-link-variant" size="small"></v-icon>&nbsp;
                          {{ resource.title }}
                          <visit-link-modal :url="resource.url">
                            <template #title>Visit external website</template>
                            <template #content>
                              You will be redirected to <em>{{ resource.url }}</em
                              ><br />
                              Are you sure that you want to visit this website?
                            </template>
                            <template #visitButtonText>Visit</template>
                          </visit-link-modal>
                        </v-list-item-title>
                      </v-list-item>
                    </v-list>
                    <p v-if="enrollment.classroom.helpful_resources.length === 0">
                      Your instructors did not provide any helpful resources.
                    </p>
                  </v-card-text>
                </v-card>
              </v-col>
              <v-col cols="6">
                <v-card variant="flat" color="cardColor" class="elevation-4">
                  <v-card-title>Unenroll</v-card-title>
                  <v-card-subtitle>Unenroll from this classroom</v-card-subtitle>
                  <v-card-text>
                    <!-- TODO: add modal to make users confirm their unenrollment -->
                    <ErrorButton @click="unenroll">Unenroll</ErrorButton>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
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
