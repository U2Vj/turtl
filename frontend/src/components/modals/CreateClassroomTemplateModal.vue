<script setup lang="ts">
import PrimaryButton from '@/components/layouts/PrimaryButton.vue'
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const showDialog = ref(false)
const titleNewClassroom = ref('')

async function createClassroomTemplate(title: string) {
  const response = await axios.post(`${import.meta.env.VITE_API_URL}/templates/classrooms`, {
    title
  })
  const router = useRouter()
  router.push(`/templates/${response.data.id}`)
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent">
    <v-card>
      <template #title>Create Classroom Template</template>
      <template #text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="titleNewClassroom"
          label="Name of new classroom template"
        ></v-text-field>
        <v-btn variant="text" color="primary" @click="showDialog = false">Close</v-btn>
        <PrimaryButton buttonName="Create" @atClick="createClassroomTemplate(titleNewClassroom)">
        </PrimaryButton>
      </template>
    </v-card>
  </v-dialog>
</template>
