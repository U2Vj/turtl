<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { useField, useForm, useResetForm } from 'vee-validate'
import { ref, toRef } from 'vue'
import * as yup from 'yup'
import {useToast} from "vue-toastification";

const showDialog = ref(false)
const catalogStore = useCatalogStore()

const props = defineProps<{ classroomId: number }>()
const toast = useToast()

let classroom = toRef(catalogStore, 'classroom')

const schema = yup.object({
  title: yup.string().required('This field is required'),
  url: yup.string().url('Please provide a valid URL').required('This field is required')
})
const { handleSubmit } = useForm({ validationSchema: schema })

const { value: titleNewHelpfulResource, errorMessage: titleError } = useField<string>(
  'title',
  {},
  { validateOnValueUpdate: false }
)

const { value: urlNewHelpfulResource, errorMessage: urlError } = useField<string>(
  'url',
  {},
  { validateOnValueUpdate: false }
)
const resetForm = useResetForm()

function resetDialog() {
  resetForm()
  showDialog.value = false
}

const createHelpfulResource = handleSubmit(async (values) => {
  if (classroom.value) {
    const newResource = {
      title: values.title,
      url: values.url
    }
    classroom.value?.helpful_resources.push(newResource)
    catalogStore.updateClassroom(props.classroomId, classroom.value).then(resetDialog).catch((e) => {
      toast.error(e.message)
    })
  }
})
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Add Helpful Resource</v-card-title>
      <v-card-subtitle>Helpful resources are displayed to students in a classroom as a list of links.</v-card-subtitle>
      <v-card-text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="titleNewHelpfulResource"
          label="Title"
          :error-messages="titleError"
        ></v-text-field>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="urlNewHelpfulResource"
          label="URL"
          :error-messages="urlError"
        ></v-text-field>
        <TextButton buttonName="Close" @click="resetDialog"></TextButton>
        <PrimaryButton buttonName="Create" @click="createHelpfulResource"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
