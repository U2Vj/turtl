<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import {TaskDifficulty, TaskType, useCatalogStore} from '@/stores/CatalogStore'
import {useField, useForm, useResetForm} from 'vee-validate'
import {ref} from 'vue'
import {useToast} from 'vue-toastification'
import * as yup from 'yup'

const showDialog = ref(false)
const toast = useToast()

const schema = yup.object({
  title: yup
    .string()
    .ensure()
    .trim()
    .required('This field is required')
    .min(2)
    .max(50)
    .matches(/.*[a-zA-Z].*/, { message: 'The title should contain at least one letter' }),
  description: yup.string().required('This field is required'),
  task_type: yup.string().required('This field is required'),
  difficulty: yup.string().required('This field is required')
})

const props = defineProps<{
  classroomId: number
  projectId: number
}>()

const { handleSubmit } = useForm({ validationSchema: schema })

const { value: title, errorMessage: titleError } = useField<string>(
  'title',
  {},
  { validateOnValueUpdate: false }
)
const { value: description, errorMessage: descriptionError } = useField<string>(
  'description',
  {},
  { validateOnValueUpdate: false }
)
const { value: taskType, errorMessage: taskTypeError } = useField<string>(
  'task_type',
  {},
  { validateOnValueUpdate: false }
)
const { value: difficulty, errorMessage: difficultyError } = useField<string>(
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
    .createTask(
      props.projectId,
      values.title,
      values.description,
      values.task_type,
      values.difficulty
    )
    .then(() => {
      resetAndHideModal()
      toast.success('Task created successfully')
    })
    .catch((e) => {
      toast.error(e.message)
    })
})

const selectDifficulty = [
  {
    title: 'Beginner',
    value: TaskDifficulty.Beginner
  },
  {
    title: 'Intermediate',
    value: TaskDifficulty.Intermediate
  },
  {
    title: 'Advanced',
    value: TaskDifficulty.Advanced
  }
]
const selectTaskType = [
  {
    title: 'Neutral',
    value: TaskType.Neutral
  },
  {
    title: 'Attack',
    value: TaskType.Attack
  },
  {
    title: 'Defense',
    value: TaskType.Defense
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
            v-model="title"
            :error-messages="titleError"
          ></v-text-field>
          <v-textarea
            label="Task Description"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
            v-model="description"
            :error-messages="descriptionError"
          ></v-textarea>
          <v-row>
            <v-col>
              <v-select
                label="Select Difficulty Level"
                :items="selectDifficulty"
                variant="underlined"
                base-color="primary"
                color="primary"
                v-model="difficulty"
                :error-messages="difficultyError"
              ></v-select>
            </v-col>
            <v-col>
              <v-select
                label="Select Task Type"
                :items="selectTaskType"
                variant="underlined"
                base-color="primary"
                color="primary"
                v-model="taskType"
                :error-messages="taskTypeError"
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
