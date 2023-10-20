<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { ref } from 'vue'
import ErrorButton from '../buttons/ErrorButton.vue'
import SecondaryButton from '../buttons/SecondaryButton.vue'
import {useToast} from "vue-toastification";

const showDialog = ref(false)
const newQuestionnaire = ref('')
const toast = useToast()

const singleChoice = ref(false)

const answerOptions = ref([{ answer: '', checked: false }, { answer: '', checked: false }])

const addAnswerOption = () => {
  answerOptions.value.push({ answer: '', checked: false })
}
const removeAnswerOption = (index: number) => {
  if(answerOptions.value.length > 2) {
    answerOptions.value.splice(index, 1)
  } else {
    toast.error("You need at least two possible answers per question.")
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
          v-model="newQuestionnaire"
          label="Question"
        ></v-text-field>
        <v-btn-toggle
          v-model="singleChoice"
          density="compact"
          color="primary"
          group
        >
          <v-btn :value="true">
            Single choice
          </v-btn>

          <v-btn :value="false">
            Multiple Choice
          </v-btn>
        </v-btn-toggle><br><br>
        <v-divider></v-divider><br>
        <v-row no-gutters class="text-caption mb-2">
          <v-col cols="1">Correct</v-col>
          <v-col cols="10">Answer</v-col>
          <v-col cols="1">Remove</v-col>
        </v-row>
        <v-row v-for="(option, index) in answerOptions" :key="index" no-gutters>
          <v-col cols="1"><v-checkbox v-model="option.checked" class="col-sm-1"></v-checkbox></v-col>
          <v-col cols="10">
            <v-text-field
              clearable
              variant="underlined"
              base-color="primary"
              color="primary"
              v-model="option.answer"
              label="Answer"
              class="col-sm-10"
            ></v-text-field>
          </v-col>
          <v-col cols="1">
            <v-btn
              icon="mdi-trash-can-outline"
              variant="text"
              @click="removeAnswerOption(index)"
              class="col-sm-1"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton @click="addAnswerOption" v-if="answerOptions.length < 10"><v-icon icon="mdi-plus-circle-outline"></v-icon>&nbsp;Add Answer</SecondaryButton><br><br>
            <v-divider></v-divider>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
            <PrimaryButton buttonName="Create"></PrimaryButton>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
