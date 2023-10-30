<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import type {Question} from '@/stores/CatalogStore'
import {QuestionType} from "@/stores/CatalogStore";
import type {Ref} from 'vue'
import {ref, toRaw} from 'vue'
import {useToast} from 'vue-toastification'
import SecondaryButton from '../buttons/SecondaryButton.vue'
import type {VForm} from "vuetify/components";

const showDialog = ref(false)
const toast = useToast()

const props = defineProps<{ currentQuestion?: Question }>()

const singleChoiceSelectedAnswerOption = ref<number>(0)

let question: Ref<Question>

const blankQuestion: Question = {
  question: "",
  question_type: QuestionType.SingleChoice,
  choices: [
    {
      answer: "",
      is_correct: false
    },
    {
      answer: "",
      is_correct: false
    }
  ]
}

if(props.currentQuestion) {
  question = ref(Object.assign({}, toRaw(props.currentQuestion)))
  if(props.currentQuestion.question_type == QuestionType.SingleChoice) {
    singleChoiceSelectedAnswerOption.value = toRaw(props.currentQuestion).choices.findIndex(choice => choice.is_correct)
  }
} else {
  question = ref(blankQuestion)
}

const addAnswer = () => {
  question.value.choices.push({ answer: "", is_correct: false })
}
const removeAnswer = (index: number) => {
  if (question.value.choices.length > 2) {
    question.value.choices.splice(index, 1)
  } else {
    toast.error('You need at least two possible answers per question.')
  }
}

const emits = defineEmits<{
  questionEditingCompleted: [question: Question]
}>()

// We perform validation manually because vee-validate does not do well with dynamically adding groups of elements to
// a form

const form: Ref<VForm | null> = ref(null)

function checkTextLength(input: string): boolean | string {
  if(!input || input.trim().length == 0) {
    return "This field is required."
  }
  if(input.length > 200) {
    return "This field must be 200 characters or less."
  }
  return true
}

const titleRules = [(input: string) => checkTextLength(input)]

function checkAnswerUnique(input: string): boolean | string {
  const filteredAnswers = question.value.choices.filter(choice => choice.answer === input)
  if(filteredAnswers.length <= 1) return true

  return "Answers must be unique."
}

const answerRules = [
  (input: string) => checkTextLength(input),
  (input: string) => checkAnswerUnique(input)
]

function checkNumberCorrect(input: boolean): boolean | string {
  if(question.value.question_type === QuestionType.SingleChoice) return true

  const filteredAnswers = question.value.choices.filter(choice => choice.is_correct)
  if(filteredAnswers.length < 1) {
    return "One or more answers must be correct."
  }
  if(filteredAnswers.length == question.value.choices.length) {
    return "Not all answers can be correct."
  }

  return true
}

const correctRules = [(input: boolean) => checkNumberCorrect(input)]

const resetAndHideDialog = () => {
  showDialog.value = false
  if(!props.currentQuestion) {
    // We only want to reset the form for newly created questions
    form.value?.reset()
    question.value.question_type = QuestionType.SingleChoice
    question.value.choices = [
      {
        answer: "",
        is_correct: false
      },
      {
        answer: "",
        is_correct: false
      }
    ]
    singleChoiceSelectedAnswerOption.value = 0
  }
}

// This function is called when submitting the form
const addQuestion = () => {
  if(question.value.question_type == QuestionType.SingleChoice) {
    question.value.choices.forEach((answer, index) => answer.is_correct = (index === singleChoiceSelectedAnswerOption.value))
  }
  form.value?.validate().then((result) => {
    if(result.valid) {
      emits('questionEditingCompleted', JSON.parse(JSON.stringify(question.value)))
      resetAndHideDialog()
    }
  })
}

</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title><slot name="title"></slot></v-card-title>
      <v-card-text>
        <v-form @submit.prevent="addQuestion" ref="form" validate-on="submit">
          <v-text-field
            variant="underlined"
            base-color="primary"
            color="primary"
            v-model="question.question"
            :rules="titleRules"
            label="Question"
          ></v-text-field>
          <v-btn-toggle v-model="question.question_type" density="compact" color="primary" group>
            <v-btn :value="QuestionType.SingleChoice" button-type="button">Single choice</v-btn>
            <v-btn :value="QuestionType.MultipleChoice" button-type="button">Multiple Choice</v-btn>
          </v-btn-toggle>
          <br /><br />
          <v-divider></v-divider>
          <br />
          <v-row no-gutters class="text-caption mb-2">
            <v-col cols="1">Correct</v-col>
            <v-col cols="10">Answer</v-col>
            <v-col cols="1">Remove</v-col>
          </v-row>
          <v-row v-for="(choice, index) in question.choices" :key="index" no-gutters>
            <v-col cols="1" align-self="end">
              <v-radio-group v-model="singleChoiceSelectedAnswerOption" v-if="question.question_type == QuestionType.SingleChoice">
                <v-radio :value="index" />
              </v-radio-group>
              <v-checkbox v-model="choice.is_correct" :rules="correctRules" v-else></v-checkbox>
            </v-col>
            <v-col cols="10">
              <v-text-field
                variant="underlined"
                base-color="primary"
                color="primary"
                v-model="choice.answer"
                :rules="answerRules"
                label="Answer"
                class="col-sm-10"
              ></v-text-field>
            </v-col>
            <v-col cols="1">
              <v-btn
                icon="mdi-trash-can-outline"
                variant="text"
                @click="removeAnswer(index)"
                class="col-sm-1"
                button-type="button"
              />
            </v-col>
          </v-row>
          <v-row v-if="question.choices.length < 10">
            <v-col>
              <SecondaryButton @click="addAnswer" button-type="button">
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
                @click="resetAndHideDialog"
                button-type="button"
              ></TextButton>
              <PrimaryButton button-type="submit">
                <slot name="submitButtonText"></slot>
              </PrimaryButton>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
