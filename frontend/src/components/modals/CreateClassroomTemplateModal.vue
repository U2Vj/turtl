<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
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
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Create Classroom Template</v-card-title>
      <v-card-text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="titleNewClassroom"
          label="Name of new classroom template"
        ></v-text-field>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Create" @click="createClassroomTemplate(titleNewClassroom)">
        </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
