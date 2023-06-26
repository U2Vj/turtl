<script setup lang="ts">
import { ref } from 'vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { axiosInstance } from '@/stores/AxiosInstance'

const showDialog = ref(false)
const newQuestion = ref('')

async function addQuestion(title: string) {
  const templateStore = useTemplateStore()
  const classroomTemplateId = templateStore.classroomTemplate?.id
  const response = await axiosInstance.post(
    `${import.meta.env.VITE_API_URL}/templates/classrooms`,
    {
      title,
      classroomTemplateId
    }
  )
  if (response.data.success) {
    showDialog.value = false
  }
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent">
    <v-card>
      <template #title>Add Question</template>
      <template #text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="newQuestion"
          label="New Question"
        ></v-text-field>
        <v-btn variant="text" color="primary" @click="showDialog = false">Close</v-btn>
        <v-btn
          variant="elevated"
          color="primary"
          class="elevation-2"
          @click="addQuestion(newQuestion)"
          >Create</v-btn
        >
      </template>
    </v-card>
  </v-dialog>
</template>
