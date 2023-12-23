<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import Shell from '@/components/shell/ShellView.vue'
import {AcceptanceCriteriaType, QuestionType} from '@/stores/CatalogStore'
import type {TaskStudent} from '@/stores/EnrollmentStore'
import {AcceptanceCriteriaSolutionResult, useEnrollmentStore} from '@/stores/EnrollmentStore'
import type {Ref} from 'vue'
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {useToast} from 'vue-toastification'
import {VCheckbox, VForm, VRow} from 'vuetify/components'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'

const props = defineProps<{ enrollmentId: number; taskId: number }>()

const task: Ref<TaskStudent | undefined> = ref()
const enrollmentStore = useEnrollmentStore()
const toast = useToast()
const router = useRouter()
const breadcrumbItems: Ref<any[]> = ref([])

enrollmentStore
  .getEnrollment(props.enrollmentId)
  .then((enrollment) => {
    task.value = enrollmentStore.getTask(props.taskId)
    const project = enrollment?.classroom.projects.filter((project) => {
      if (!task.value) return false
      return project.tasks.includes(task.value)
    })[0]
    breadcrumbItems.value = [
      {
        title: enrollment?.classroom.title,
        disabled: false,
        to: {
          name: 'StudentClassroom',
          params: {
            enrollmentId: props.enrollmentId
          }
        }
      },
      {
        title: project.title,
        disabled: false,
        to: {
          name: 'StudentClassroom',
          params: {
            enrollmentId: props.enrollmentId
          }
        }
      },
      {
        title: task.value?.title,
        disabled: true
      }
    ]
  })
  .catch((e) => toast.error(e.message))

type AcceptanceCriteriaError = {
  id: number
  error: string
}
type AcceptanceCriteriaErrors = {
  flagErrors: AcceptanceCriteriaError[]
  regExErrors: AcceptanceCriteriaError[]
  questionErrors: AcceptanceCriteriaError[]
}

function getSingleChoiceSelectedAnswerOption(questionId: number) {
  return task.value?.acceptance_criteria.questions
    ?.find((question) => question.id === questionId)
    ?.choices.find((choice) => choice.checked)?.id
}
function setSingleChoiceSelectedAnswerOption(questionId: number, choiceId: number) {
  task.value?.acceptance_criteria.questions
    ?.find((question) => question.id === questionId)
    ?.choices.forEach((choice) => (choice.checked = choice.id === choiceId))
}

const errorMessages: Ref<AcceptanceCriteriaErrors> = ref({
  flagErrors: [],
  regExErrors: [],
  questionErrors: []
})
const showCheckmarks = ref(false)

function getErrorMessages(errorList: AcceptanceCriteriaError[], id: number): string[] {
  return errorList.filter((error) => error.id === id).map((error) => error.error)
}

function getFlagErrors(id: number) {
  return getErrorMessages(errorMessages.value.flagErrors, id)
}

function getRegExErrors(id: number) {
  return getErrorMessages(errorMessages.value.regExErrors, id)
}

function getQuestionErrors(id: number) {
  return getErrorMessages(errorMessages.value.questionErrors, id)
}

function submitSolution() {
  if (!task.value) return

  // reset error lists
  errorMessages.value = {
    flagErrors: [],
    regExErrors: [],
    questionErrors: []
  }

  // check if some regex or flag inputs have no content
  task.value.acceptance_criteria.flags
    ?.filter((flag) => !flag.solution || flag.solution.trim().length === 0)
    .forEach((flag) =>
      errorMessages.value.flagErrors.push({
        id: flag.id,
        error: 'You must enter a solution.'
      })
    )
  task.value.acceptance_criteria.regexes
    ?.filter((regex) => !regex.solution || regex.solution.trim().length === 0)
    .forEach((regex) =>
      errorMessages.value.regExErrors.push({
        id: regex.id,
        error: 'You must enter a solution.'
      })
    )

  // check if some questions have no answers checked
  task.value.acceptance_criteria.questions
    ?.filter((question) => !question.choices.some((choice) => choice.checked))
    .forEach((question) =>
      errorMessages.value.questionErrors.push({
        id: question.id,
        error: 'Please select at least one answer.'
      })
    )

  // If there are error messages, i.e. if the frontend validation failed, abort the form submission
  if (Object.values(errorMessages.value).some((errors) => errors.length > 0)) {
    toast.error('Some answers were not correct')
    return
  }

  // Now we can send the data to the backend and submit the solution
  enrollmentStore
    .submitSolution(task.value)
    .then((response) => {
      showCheckmarks.value = true
      if (response.passed) {
        toast.success(`Congratulations! You have solved the task '${task.value?.title}'.`)
        router.push({ name: 'StudentClassroom', params: { enrollmentId: props.enrollmentId } })
        return
      }

      // Now we know that some answers were not correct
      toast.error('Some answers were not correct')
      // We go through everything and append error messages if applicable
      for (const id in response.flags) {
        let error: string = response.flags[id]
        if (response.flags[id] === AcceptanceCriteriaSolutionResult.Correct) continue
        else if (response.flags[id] === AcceptanceCriteriaSolutionResult.Incorrect) {
          error = 'Incorrect answer'
        }
        errorMessages.value.flagErrors.push({
          id: Number(id),
          error: error
        })
      }
      for (const id in response.regexes) {
        let error: string = response.regexes[id]
        if (response.regexes[id] === AcceptanceCriteriaSolutionResult.Correct) continue
        else if (response.regexes[id] === AcceptanceCriteriaSolutionResult.Incorrect) {
          error = 'Incorrect answer'
        }
        errorMessages.value.regExErrors.push({
          id: Number(id),
          error: error
        })
      }
      for (const id in response.questions) {
        let error: string = response.questions[id]
        if (response.questions[id] === AcceptanceCriteriaSolutionResult.Correct) continue
        else if (response.questions[id] === AcceptanceCriteriaSolutionResult.Incorrect) {
          error = 'Incorrect answer'
        }
        errorMessages.value.questionErrors.push({
          id: Number(id),
          error: error
        })
      }
    })
    .catch((e) => toast.error(e.message))
}
</script>

<template>
  <DefaultLayout v-if="task" :breadcrumb-items="breadcrumbItems">
    <template #heading>{{ task.title }}</template>
    <template #default>
      <v-container fluid>
        <v-row>
          <v-col cols="6">
            <p style="white-space: pre-wrap">{{ task.description }}</p>
            <br />
          </v-col>
          <v-col cols="6">
            <Shell />
          </v-col>
        </v-row>
        <v-divider class="mt-4 mb-4"></v-divider>
      </v-container>
      <v-container>
        <v-form @submit.prevent="submitSolution">
          <v-row v-for="flag in task.acceptance_criteria.flags">
            <v-col>
              <v-card color="cardColor">
                <v-card-title>{{ flag.prompt }}</v-card-title>
                <v-card-subtitle>Enter your solution below</v-card-subtitle>
                <v-card-text>
                  <v-text-field
                    v-model="flag.solution"
                    :error-messages="getFlagErrors(flag.id)"
                  ></v-text-field>
                  <v-icon
                    v-if="showCheckmarks && getFlagErrors(flag.id).length === 0"
                    icon="mdi-check-circle-outline"
                    color="success"
                  ></v-icon>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <v-divider
            class="mt-4 mb-4"
            v-if="task.acceptance_criteria.flags && task.acceptance_criteria.flags.length > 0"
          />
          <v-row v-for="regex in task.acceptance_criteria.regexes">
            <v-col>
              <v-card color="cardColor">
                <v-card-title>{{ regex.prompt }}</v-card-title>
                <v-card-subtitle>Enter your solution below</v-card-subtitle>
                <v-card-text>
                  <v-text-field
                    v-model="regex.solution"
                    :error-messages="getRegExErrors(regex.id)"
                  ></v-text-field>
                  <v-icon
                    v-if="showCheckmarks && getRegExErrors(regex.id).length === 0"
                    icon="mdi-check-circle-outline"
                    color="success"
                  ></v-icon>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <v-divider
            v-if="task.acceptance_criteria.regexes && task.acceptance_criteria.regexes.length > 0"
            class="mt-4 mb-4"
          />
          <v-row v-for="question in task.acceptance_criteria.questions" ref="questions">
            <v-col>
              <v-card color="cardColor">
                <v-card-title>{{ question.question }}</v-card-title>
                <v-card-subtitle v-if="question.question_type === QuestionType.SingleChoice">
                  Select the correct answer
                </v-card-subtitle>
                <v-card-subtitle v-else> Select the correct answers </v-card-subtitle>
                <v-card-text>
                  <div v-for="choice in question.choices">
                    <v-radio-group
                      v-if="question.question_type == QuestionType.SingleChoice"
                      :model-value="getSingleChoiceSelectedAnswerOption(question.id)"
                      @update:model-value="
                        (choiceId) => setSingleChoiceSelectedAnswerOption(question.id, choiceId)
                      "
                    >
                      <v-radio :label="choice.answer" :value="choice.id" />
                    </v-radio-group>
                    <v-checkbox :label="choice.answer" v-model="choice.checked" v-else></v-checkbox>
                  </div>
                  <v-alert
                    icon="false"
                    type="error"
                    density="compact"
                    v-for="error in getQuestionErrors(question.id)"
                  >
                    {{ error }}
                  </v-alert>
                  <v-icon
                    v-if="showCheckmarks && getQuestionErrors(question.id).length === 0"
                    icon="mdi-check-circle-outline"
                    color="success"
                  ></v-icon>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
          <v-divider
            v-if="
              task.acceptance_criteria.questions && task.acceptance_criteria.questions.length > 0
            "
            class="mt-4 mb-4"
          />
          <v-row v-if="task.done && task.acceptance_criteria.criteria_type !== AcceptanceCriteriaType.Disabled">
            <v-col>
              <v-sheet color="cardColor" class="pa-4">
                <p>
                  <strong>Please note:</strong> You have already solved this task. You can try again
                  and check if the values you entered are correct, but your initial solution will
                  remain and will not be lost or changed.
                </p>
              </v-sheet>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <PrimaryButton button-type="submit">
                <template v-if="task.acceptance_criteria.criteria_type == AcceptanceCriteriaType.Disabled">
                  Mark as done
                </template>
                <template v-else>
                  Submit solution
                </template>
              </PrimaryButton>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </template>
  </DefaultLayout>
</template>

<style scoped>
.center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.v-breadcrumbs {
  padding: 0;
}
</style>
