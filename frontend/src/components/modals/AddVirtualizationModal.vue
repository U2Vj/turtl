<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { useField, useForm, useResetForm } from 'vee-validate'
import { ref, toRef } from 'vue'
import * as yup from 'yup'

const showDialog = ref(false)
const catalogStore = useCatalogStore()

const props = defineProps<{
  classroomId: number
  taskId: number
}>()

let classroom = toRef(catalogStore, 'classroom')

const schema = yup.object({
  name: yup.string().required('This field is required'),
  role: yup.string().required('This field is required'),
  dockerfile: yup.string().required('This field is required')
})
const { handleSubmit } = useForm({ validationSchema: schema })

const { value: nameNewVirtualization, errorMessage: nameError } = useField<string>(
  'name',
  {},
  { validateOnValueUpdate: false }
)

const { value: roleNewVirtualization, errorMessage: roleError } = useField<string>(
  'role',
  {},
  { validateOnValueUpdate: false }
)

const { value: dockerfileNewVirtualization, errorMessage: dockerfileError } = useField<string>(
  'dockerfile',
  {},
  { validateOnValueUpdate: false }
)

const resetForm = useResetForm()

function resetDialog() {
  resetForm()
  showDialog.value = false
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Add Virtualization</v-card-title>
      <v-card-subtitle>Virtualizations for the challenges.</v-card-subtitle>
      <v-card-text>
        <v-text-field
          label="Name of Virtualization"
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="nameNewVirtualization"
        ></v-text-field>
        <v-select
          label="Role"
          :items="['UserShell', 'IP']"
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="roleNewVirtualization"
        ></v-select>
        <v-text-field
          label="Dockerfile Content"
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="dockerfileNewVirtualization"
        ></v-text-field>
        <TextButton buttonName="Close" @click="resetDialog"></TextButton>
        <PrimaryButton buttonName="Create"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
