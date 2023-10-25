<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import type { Task } from '@/stores/CatalogStore'
import { ref } from 'vue'
import { useToast } from 'vue-toastification'
import SecondaryButton from '../buttons/SecondaryButton.vue'

const showDialog = ref(false)
const newQuestionnaire = ref('')
const toast = useToast()

const props = defineProps<{ task: Task }>()

const singleChoice = ref(true)

const answerOptions = ref([
  { answer: '', checked: false },
  { answer: '', checked: false }
])
const singleChoiceSelectedAnswerOption = ref<number>(0)

const addAnswerOption = () => {
  answerOptions.value.push({ answer: '', checked: false })
}
const removeAnswerOption = (index: number) => {
  if (answerOptions.value.length > 2) {
    answerOptions.value.splice(index, 1)
  } else {
    toast.error('You need at least two possible answers per question.')
  }
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title><slot name="title"></slot></v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
            v-model="newQuestionnaire"
            label="Question"
          ></v-text-field>
          <v-btn-toggle v-model="singleChoice" density="compact" color="primary" group>
            <v-btn :value="true" button-type="button"> Single choice </v-btn>
            <v-btn :value="false" button-type="button"> Multiple Choice </v-btn> </v-btn-toggle
          ><br /><br />
          <v-divider></v-divider><br />
          <v-row no-gutters class="text-caption mb-2">
            <v-col cols="1">Correct</v-col>
            <v-col cols="10">Answer</v-col>
            <v-col cols="1">Remove</v-col>
          </v-row>
          <v-row v-for="(option, index) in answerOptions" :key="index" no-gutters>
            <v-col cols="1" align-self="end">
              <v-radio-group v-model="singleChoiceSelectedAnswerOption" v-if="singleChoice">
                <v-radio :value="index" />
              </v-radio-group>
              <v-checkbox v-model="option.checked" v-else></v-checkbox>
            </v-col>
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
                button-type="button"
              />
            </v-col>
          </v-row>
          <v-row v-if="answerOptions.length < 10">
            <v-col>
              <SecondaryButton @click="addAnswerOption" button-type="button">
                <v-icon icon="mdi-plus-circle-outline"></v-icon>&nbsp;Add Answer
              </SecondaryButton>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-divider></v-divider>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <TextButton
                button-name="Close"
                @click="showDialog = false"
                button-type="button"
              ></TextButton>
              <PrimaryButton button-name="Add" button-type="submit"></PrimaryButton>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
