<script setup lang="ts">
import { ref } from 'vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { useAxios } from '@vueuse/integrations/useAxios'
import type { Instructor } from '@/stores/TemplateStore'

const templateStore = useTemplateStore()
const { data: AllInstructors } = useAxios<Instructor[]>(
  `${import.meta.env.VITE_API_URL}/users/instructors`
)
const instructors = AllInstructors.value?.filter((element: Instructor) => {
  return !templateStore.classroomTemplate?.instructors.includes(element)
})
const showDialog = ref(false)
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent">
    <v-card>
      <template #title>Add Instructors</template>
      <template #text>
        <v-data-table
          :headers="[
            { title: 'E-Mail', key: 'email' },
            { title: 'Add', key: 'add' }
          ]"
          :items="instructors"
        >
          <template #[`item.add`]="{ item }">
            <v-btn
              icon="mdi-plus"
              variant="text" color="primary"
              @click="
                () => {
                  templateStore.addInstructor(item.raw.instructorId, item.raw.email)
                }
              "
            />
          </template>
        </v-data-table>
        <v-btn variant="text" color="primary" @click="showDialog = false">Close</v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>
