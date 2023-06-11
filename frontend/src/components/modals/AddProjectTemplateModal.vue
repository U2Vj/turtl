<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'
import { useTemplateStore } from '@/stores/TemplateStore'

const showDialog = ref(false)
const titleNewProject = ref('')

async function addProjectTemplate(title: string) {
  const templateStore = useTemplateStore()
  const classroomTemplateId = templateStore.classroomTemplate?.templateId
  const response = await axios.post(`${import.meta.env.VITE_API_URL}/templates/classrooms`, {
    title,
    classroomTemplateId
  })
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent">
    <v-card>
      <template #title>Create Project Template</template>
      <template #text>
        <v-text-field v-model="titleNewProject" label="Name of new project template"></v-text-field>
        <v-btn color="primary" @click="addProjectTemplate(titleNewProject)">Create</v-btn>
        <v-btn @click="showDialog = false">Close</v-btn>
      </template>
    </v-card>
  </v-dialog>
</template>
