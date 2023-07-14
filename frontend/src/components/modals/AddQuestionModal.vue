<script setup lang="ts">
import { makeAxiosRequest } from '@/stores/AxiosInstance'
import { useTemplateStore } from '@/stores/TemplateStore'
import { ref } from 'vue'

const showDialog = ref(false)
const newQuestion = ref('')

async function addQuestion(title: string) {
  const templateStore = useTemplateStore()
  const classroomTemplateId = templateStore.classroomTemplate?.id
  const data = {
    title,
    classroomTemplateId
  }

  const response = await makeAxiosRequest('/templates/classrooms', 'POST', true, true, data)
  if (response.success) {
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
