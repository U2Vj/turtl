<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { ref } from 'vue'
import ErrorButton from '../buttons/ErrorButton.vue'
import SecondaryButton from '../buttons/SecondaryButton.vue'

const showDialog = ref(false)
const newQuestionnaire = ref('')

const singleChoice = ref(false)

const answerOptions = ref([{ answer: '', checked: false }])

const addAnswerOption = () => {
  answerOptions.value.push({ answer: '', checked: false })
}
const removeAnswerOption = (index: number) => {
  answerOptions.value.splice(index, 1)
}
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
        <v-row>
          <v-col>
            <div
              v-for="(option, index) in answerOptions"
              :key="index"
              style="display: flex; justify-content: start"
            >
              <div>
                <v-checkbox v-model="option.checked"></v-checkbox>
              </div>
              <div style="flex-grow: 1">
                <v-text-field
                  clearable
                  variant="underlined"
                  base-color="primary"
                  color="primary"
                  v-model="option.answer"
                  label="Answer"
                ></v-text-field>
                <div>
                  <ErrorButton
                    button-name="Delete"
                    @click="removeAnswerOption(index)"
                  ></ErrorButton>
                </div>
              </div>
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton
              button-name="Add Answer Option"
              @click="addAnswerOption"
            ></SecondaryButton>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
            <PrimaryButton buttonName="Create"> </PrimaryButton>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
