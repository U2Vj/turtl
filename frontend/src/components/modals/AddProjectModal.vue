<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import axios from 'axios'
import { ref } from 'vue'

const showDialog = ref(false)
const titleNewProject = ref('')

async function addProject(title: string) {
  // TODO: make this actually work
  const catalogStore = useCatalogStore()
  const classroomTemplateId = catalogStore.classroom?.id
  const response = await axios.post(`${import.meta.env.VITE_API_URL}/catalog/projects`, {
    title,
    classroomTemplateId
  })

  if (response.data.success) {
    showDialog.value = false
  }
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Create Project Template</v-card-title>
      <v-card-text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="titleNewProject"
          label="Name of new project template"
        ></v-text-field>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Create" @click="addProject(titleNewProject)">
        </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
