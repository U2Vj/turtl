<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { ref } from 'vue'

const showDialog = ref(false)
const newQuestionnaire = ref('')

const singleChoice = ref(false)
const answer1 = ref(false)
const labelAnswer1 = ref('')
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
        <div style="display: flex; justify-content: start">
          <div>
            <v-checkbox v-model="answer1"></v-checkbox>
          </div>
          <div style="flex: 1">
            <v-text-field
              clearable
              variant="underlined"
              base-color="primary"
              color="primary"
              v-model="labelAnswer1"
              label="Answer"
            ></v-text-field>
          </div>
        </div>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Create"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
