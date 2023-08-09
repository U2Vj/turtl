<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { useField, useForm } from 'vee-validate'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import * as yup from 'yup'

const showDialog = ref(false)
const router = useRouter()

const templateStore = useTemplateStore()

const isCreating = ref(false)

// let templateData = toRef(templateStore, 'basicTemplateData')
// templateStore.getBasicTemplateData()

const schema = yup.object({
  title: yup.string().required('This field is required')
})
const { handleSubmit } = useForm({ validationSchema: schema })

const { value: titleNewClassroom, errorMessage: titleError } = useField<string>(
  'title',
  {},
  { validateOnValueUpdate: false }
)

const create = handleSubmit(async (values) => {
  if (isCreating.value) {
    return
  }

  isCreating.value = true

  const result = await templateStore.createProjectTemplate(values.title)

  isCreating.value = false
  if (result.success) {
    console.log('Hier die ID:', result.id)
    console.log('Hier der success:', result.success)
    // router.push({ path: `admin/templates/${result.id}` })
    router.push('/profile')
  }
})
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
        ></v-text-field>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Create" @click="create" :disabled="isCreating"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
