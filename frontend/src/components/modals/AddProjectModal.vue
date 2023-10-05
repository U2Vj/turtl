<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { ref } from 'vue'
import * as yup from "yup";
import { useField, useForm, useResetForm } from "vee-validate";

const showDialog = ref(false)

const schema = yup.object({
  title: yup.string()
      .ensure()
      .trim()
      .required('This field is required')
      .min(3)
      .max(120)
      .matches(/.*[a-zA-Z].*/, {message: "The title should contain at least one letter"})
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
  await catalogStore.createProject(values.title)
  resetAndHideModal()
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
