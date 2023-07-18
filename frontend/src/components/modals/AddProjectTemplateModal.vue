<script setup lang="ts">
import PrimaryButton from '@/components/layouts/PrimaryButton.vue'
import TextButton from '@/components/layouts/TextButton.vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import axios from 'axios'
import { ref } from 'vue'

const showDialog = ref(false)
const titleNewProject = ref('')

async function addProjectTemplate(title: string) {
  const templateStore = useTemplateStore()
  const classroomTemplateId = templateStore.classroomTemplate?.id
  const response = await axios.post(`${import.meta.env.VITE_API_URL}/templates/classrooms`, {
    title,
    classroomTemplateId
  })

  if (response.data.success) {
    showDialog.value = false
  }
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent">
    <v-card>
      <template #title>Create Project Template</template>
      <template #text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="titleNewProject"
          label="Name of new project template"
        ></v-text-field>
        <TextButton buttonName="Close" @atClick="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Create" @atClick="addProjectTemplate(titleNewProject)">
        </PrimaryButton>
      </template>
    </v-card>
  </v-dialog>
</template>
