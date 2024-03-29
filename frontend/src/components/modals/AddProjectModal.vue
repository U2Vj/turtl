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
    .matches(/.*[a-zA-Z].*/, { message: 'The title should contain at least one letter' })
})

const { handleSubmit } = useForm({ validationSchema: schema })

const { value: titleNewProject, errorMessage: titleError } = useField<string>(
  'title',
  {},
  { validateOnValueUpdate: false }
)

const resetForm = useResetForm()

function resetAndHideModal() {
  showDialog.value = false
  resetForm()
}

const addProject = handleSubmit(async (values) => {
  const catalogStore = useCatalogStore()
  catalogStore
    .createProject(values.title)
    .then(() => {
      resetAndHideModal()
      toast.success('Project created successfully')
    })
    .catch((e) => {
      toast.error(e.message)
    })
})
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Create Project</v-card-title>
      <v-card-text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="titleNewProject"
          label="Title"
          :error-messages="titleError"
        ></v-text-field>
        <TextButton buttonName="Close" @click="resetAndHideModal"></TextButton>
        <PrimaryButton buttonName="Create" @click="addProject"></PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
