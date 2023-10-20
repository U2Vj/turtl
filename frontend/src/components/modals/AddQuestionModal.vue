<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { ref } from 'vue'

const showDialog = ref(false)
const newQuestionnaire = ref('')

const singleChoice = ref(false)
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Add Questionnaire</v-card-title>
      <v-card-text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="newQuestionnaire"
          label="New Questionnaire"
        ></v-text-field>
        <v-checkbox v-model="singleChoice" label="Single Choice"></v-checkbox>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Create"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
