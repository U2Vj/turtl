<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { useField, useForm, useResetForm } from 'vee-validate'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import * as yup from 'yup'

const showDialog = ref(false)
const router = useRouter()
const createFunctionCalls = ref(0)
const templateStore = useTemplateStore()

// let templateData = toRef(templateStore, 'basicTemplateData')
// templateStore.getBasicTemplateData()

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

const createURL = handleSubmit(async (values) => {
  //   const result = await templateStore.createProjectTemplate(values.title)
  //   if (result.success) {
  //     router.push({ name: 'AdminTemplateClassroom', params: { templateId: result.id } })
  //   }
  //   createFunctionCalls.value++
})
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Add Helpful Resource</v-card-title>
      <v-card-text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="titleNewHelpfulResource"
          label="Title of helpful resource"
          :error-messages="titleError"
        ></v-text-field>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="urlNewHelpfulResource"
          label="URL of helpful resource"
          :error-messages="urlError"
        ></v-text-field>
        <TextButton buttonName="Close" @click="resetDialog"></TextButton>
        <PrimaryButton buttonName="Create" @click="createURL"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
