<script setup lang="ts">
import { makeAPIRequest } from '@/communication/APIRequests'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import type { User } from '@/stores/UserStore'
import { useUserStore } from '@/stores/UserStore'
import { ref, toRef } from 'vue'
import { useToast } from 'vue-toastification'
import PrimaryButton from '../buttons/PrimaryButton.vue'

const userStore = useUserStore()

const toast = useToast()
const instructors = ref<User[]>()

const catalogStore = useCatalogStore()
const classroom = toRef(catalogStore, 'classroom')
const currentInstructorId = ref()
const showDialogInstructor = ref(false)

makeAPIRequest('/users/instructors', 'GET', true, true)
  .then((response) => {
    instructors.value = response.data
  })
  .catch((e) => {
    toast.error(e.message)
  })

const showDialog = ref(false)

function instructorInClassroom(id: number): boolean {
  if (!classroom.value) {
    return false
  }
  return classroom.value.instructors.filter((item) => item.instructor.id === id).length > 0
}

function confirmInstructorRemoval(instructorId: number) {
  currentInstructorId.value = instructorId
  showDialogInstructor.value = true
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Add Instructors</v-card-title>
      <v-card-text>
        <v-data-table
          :headers="[
            { title: 'E-Mail', key: 'email' },
            { title: 'Add', key: 'add' }
          ]"
          :items="instructors"
        >
          <template #[`item.add`]="{ item }">
            <v-btn
              icon="mdi-trash-can-outline"
              variant="text"
              color="error"
              @click="
                () => {
                  if (item.raw.id === userStore.user?.id) {
                    confirmInstructorRemoval(item.raw.id)
                  } else {
                    catalogStore
                      .removeInstructor(item.raw.id)
                      .then(() => toast.info('Instructor removed'))
                      .catch((e) => toast.error(e.message))
                  }
                }
              "
              v-if="instructorInClassroom(item.raw.id)"
            />
            <v-btn
              icon="mdi-plus"
              variant="text"
              @click="
                () => {
                  catalogStore
                    .addInstructor(item.raw.id)
                    .then(() => toast.success('Instructor added'))
                    .catch((e) => toast.error(e.message))
                }
              "
              v-else
            />
            <v-dialog v-model="showDialogInstructor">
              <v-card>
                <v-card-title>Delete Task</v-card-title>
                <v-card-text>
                  <p>
                    Are you sure that you want to remove yourself from this classroom? You will no longer have access to
                    this classroom if you continue.
                  </p>
                </v-card-text>
                <v-card-actions>
                  <TextButton buttonName="Close" @click="showDialogInstructor = false"></TextButton>
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
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
