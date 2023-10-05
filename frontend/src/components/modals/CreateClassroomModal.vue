<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { useField, useForm, useResetForm } from 'vee-validate'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import * as yup from 'yup'

const showDialog = ref(false)
const router = useRouter()
const catalogStore = useCatalogStore()

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

const { value: titleNewClassroom, errorMessage: titleError } = useField<string>(
  'title',
  {},
  { validateOnValueUpdate: false }
)

const create = handleSubmit(async (values) => {
  const result = await catalogStore.createClassroom(values.title)
  if (result.success) {
    await router.push({ name: 'InstructorClassroom', params: { classroomId: result.id } })
  }
})

const resetForm = useResetForm()
function resetDialog() {
  resetForm()
  showDialog.value = false
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Create Classroom</v-card-title>
      <v-card-text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="titleNewClassroom"
          label="Title"
          :error-messages="titleError"
        ></v-text-field>
        <TextButton buttonName="Close" @click="resetDialog"></TextButton>
        <PrimaryButton buttonName="Create" @click="create"></PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
