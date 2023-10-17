<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { useField, useForm, useResetForm } from 'vee-validate'
import { ref } from 'vue'
import { useToast } from 'vue-toastification'
import * as yup from 'yup'

const showDialog = ref(false)
const toast = useToast()

const schema = yup.object({
  title: yup
    .string()
    .ensure()
    .trim()
    .required('This field is required')
    .min(3)
    .max(120)
    .matches(/.*[a-zA-Z].*/, { message: 'The title should contain at least one letter' }),
  description: yup.string().required('This field is required'),
  task_type: yup.string().required('This field is required'),
  difficulty: yup.string().required('This field is required')
})

const { handleSubmit } = useForm({ validationSchema: schema })

const { value: titleNewTask, errorMessage: titleError } = useField<string>(
  'title',
  {},
  { validateOnValueUpdate: false }
)
const { value: descriptionNewTask, errorMessage: descriptionError } = useField<string>(
  'description',
  {},
  { validateOnValueUpdate: false }
)
const { value: task_typeNewTask, errorMessage: task_typeError } = useField<string>(
  'task_type',
  {},
  { validateOnValueUpdate: false }
)
const { value: difficultyNewTask, errorMessage: difficultyError } = useField<string>(
  'difficulty',
  {},
  { validateOnValueUpdate: false }
)

const resetForm = useResetForm()

function resetAndHideModal() {
  showDialog.value = false
  resetForm()
}

const addTask = handleSubmit(async (values) => {
  const catalogStore = useCatalogStore()
  catalogStore
    .createTask(titleNewTask, descriptionNewTask, task_typeNewTask, difficultyNewTask)
    .then(() => {
      resetAndHideModal()
      toast.success('Task created successfully')
    })
    .catch((e) => {
      toast.error(e.message)
    })
})

const difficultyLevel = [
  {
    title: 'Beginner',
    value: 'beginner'
  },
  {
    title: 'Intermediate',
    value: 'intermediate'
  },
  {
    title: 'Advanced',
    value: 'advanced'
  }
]
const selectTaskType = [
  {
    title: 'Neutral',
    value: 'neutral'
  },
  {
    title: 'Attack',
    value: 'attack'
  },
  {
    title: 'Defense',
    value: 'defense'
  }
]
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Create Task</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            label="Edit Title"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
            v-model="titleNewTask"
            :error-messages="titleError"
          ></v-text-field>
          <v-textarea
            label="Task Description"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
            v-model="descriptionNewTask"
          ></v-textarea>
          <v-row>
            <v-col>
              <v-select
                label="Select Difficulty Level"
                :items="difficultyLevel"
                variant="underlined"
                base-color="primary"
                color="primary"
                v-model="difficultyNewTask"
              ></v-select>
            </v-col>
            <v-col>
              <v-select
                label="Select Task Type"
                :items="selectTaskType"
                variant="underlined"
                base-color="primary"
                color="primary"
                v-model="task_typeNewTask"
              ></v-select>
            </v-col>
          </v-row>
        </v-form>
        <TextButton buttonName="Close" @click="resetAndHideModal"></TextButton>
        <PrimaryButton buttonName="Create" @click="addTask"></PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
