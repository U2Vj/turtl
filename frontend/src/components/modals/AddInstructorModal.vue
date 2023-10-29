<script setup lang="ts">
import TextButton from '@/components/buttons/TextButton.vue'
import {ref, toRef} from 'vue'
import { makeAPIRequest } from "@/communication/APIRequests";
import {useToast} from "vue-toastification";
import type {User} from "@/stores/UserStore";
import {useCatalogStore} from "@/stores/CatalogStore";

const toast = useToast()
const instructors = ref<User[]>()

const catalogStore = useCatalogStore()
const classroom = toRef(catalogStore, 'classroom')

makeAPIRequest("/users/instructors", 'GET', true, true).then((response) => {
  instructors.value = response.data
}).catch((e) => {
  toast.error(e.message)
})

const showDialog = ref(false)

function instructorInClassroom(id: number): boolean {
  if(!classroom.value) {
    return false
  }
  return classroom.value.instructors.filter(item => item.instructor.id === id).length > 0
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
                  catalogStore.removeInstructor(item.raw.id)
                    .then(() => toast.info('Instructor removed'))
                    .catch((e) => toast.error(e.message))
                }
              "
              v-if="instructorInClassroom(item.raw.id)"
            />
            <v-btn
              icon="mdi-plus"
              variant="text"
              @click="
                () => {
                  catalogStore.addInstructor(item.raw.id)
                    .then(() => toast.success('Instructor added'))
                    .catch((e) => toast.error(e.message))
                }
              "
              v-else
            />
          </template>
        </v-data-table>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
