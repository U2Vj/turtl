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
  title: yup.string().required('This 1 field is required')
})
const { handleSubmit } = useForm({ validationSchema: schema })

const { value: titleNewClassroom, errorMessage: titleError } = useField<string>(
  'title',
  {},
  { validateOnValueUpdate: false }
)

const create = handleSubmit(async (values) => {
  const result = await templateStore.createProjectTemplate(values.title)
  if (result.success) {
    router.push({ name: 'AdminTemplateClassroom', params: { templateId: result.id } })
  }
  createFunctionCalls.value++
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
      <v-card-title>Create Classroom Template</v-card-title>
      <v-card-text>
        <v-text-field
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="titleNewClassroom"
          label="Name of new classroom template"
          :error-messages="titleError"
        ></v-text-field>
        <TextButton buttonName="Close" @click="resetDialog"></TextButton>
        <PrimaryButton buttonName="Create" @click="create"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
