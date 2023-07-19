<script setup lang="ts">
import PrimaryButton from '@/components/layouts/PrimaryButton.vue'
import TextButton from '@/components/layouts/TextButton.vue'
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
      <v-card-title>Add Question</v-card-title>
      <v-card-text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="newQuestion"
          label="New Question"
        ></v-text-field>
        <TextButton buttonName="Close" @atClick="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Create" @atClick="addQuestion(newQuestion)"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
