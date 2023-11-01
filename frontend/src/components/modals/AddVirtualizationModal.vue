<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import {useCatalogStore, VirtualizationRole} from '@/stores/CatalogStore'
import { useField, useForm, useResetForm } from 'vee-validate'
import { ref, toRef } from 'vue'
import * as yup from 'yup'
import type { Virtualization } from '@/stores/CatalogStore'

const showDialog = ref(false)

const props = defineProps<{ currentVirtualization?: Virtualization }>()
const emits = defineEmits<{ virtualizationEditingCompleted: [virtualization: Virtualization] }>()

const schema = yup.object({
  name: yup.string().required('This field is required').max(30),
  role: yup.string().required('This field is required'),
  dockerfile: yup.string().required('This field is required')
})
const { handleSubmit, resetForm } = useForm({ validationSchema: schema })

const { value: name, errorMessage: nameError } = useField<string>(
  'name',
  {},
  {
    validateOnValueUpdate: false,
    initialValue: (props.currentVirtualization) ? props.currentVirtualization.name : ''
  }
)

const { value: role, errorMessage: roleError } = useField<string>(
  'role',
  {},
  {
    validateOnValueUpdate: false,
    initialValue: (props.currentVirtualization) ? props.currentVirtualization.role : ''
  }
)

const { value: dockerfile, errorMessage: dockerfileError } = useField<string>(
  'dockerfile',
  {},
  {
    validateOnValueUpdate: false,
    initialValue: (props.currentVirtualization) ? props.currentVirtualization.dockerfile : ''
  }
)

const selectVirtualizationRole = [
  {
    title: 'User Shell',
    value: VirtualizationRole.UserShell
  },
  {
    title: 'User-accessible via IP',
    value: VirtualizationRole.UserAccessible
  }
]

function resetDialog() {
  resetForm()
  showDialog.value = false
}

const addVirtualization = handleSubmit((values) => {
  const virtualization = values as Virtualization
  if(props.currentVirtualization) {
    virtualization.id = props.currentVirtualization.id
  }
  emits('virtualizationEditingCompleted', virtualization)
  resetDialog()
})

</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title><slot name="title"></slot></v-card-title>
      <v-card-text>
        <v-form @submit.prevent="addVirtualization">
          <v-text-field
            label="Name of Virtualization"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
            v-model="name"
            :error-messages="nameError"
          ></v-text-field>
          <v-select
            label="Role"
            :items="selectVirtualizationRole"
            variant="underlined"
            base-color="primary"
            color="primary"
            v-model="role"
            :error-messages="roleError"
          ></v-select>
          <v-textarea
            label="Dockerfile Content"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
            v-model="dockerfile"
            :error-messages="dockerfileError"
          ></v-textarea>
          <TextButton button-name="Close" @click="resetDialog" button-type="button"></TextButton>
          <PrimaryButton button-type="submit"><slot name="submitButtonText"></slot></PrimaryButton>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
