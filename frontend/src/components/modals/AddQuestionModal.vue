<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { makeAxiosRequest } from '@/stores/AxiosInstance'
import { useCatalogStore } from '@/stores/CatalogStore'
import { ref } from 'vue'

const showDialog = ref(false)
const newQuestion = ref('')

async function addQuestion(title: string) {
  // TODO: make this actually work
  const catalogStore = useCatalogStore()
  const classroomId = catalogStore.classroom?.id
  const data = {
    title,
    classroomId
  }

  const response = await makeAxiosRequest('/templates/classrooms', 'POST', true, true, data)
  if (response.success) {
    showDialog.value = false
  }
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
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
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Create" @click="addQuestion(newQuestion)"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
