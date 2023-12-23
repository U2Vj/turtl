<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import {useToast} from 'vue-toastification'
import type {Invitation} from "@/stores/InvitationStore"
import {TargetRole, useInvitationStore} from "@/stores/InvitationStore"
import {useUserStore} from "@/stores/UserStore"
import {useField, useForm} from "vee-validate"
import * as yup from 'yup'
import {toTypedSchema} from "@vee-validate/yup"
import { ref } from "vue"

const userStore = useUserStore()
const invitationStore = useInvitationStore()
const toast = useToast()

const isDisabled = ref(false)

const schema = toTypedSchema(yup.object({
  email: yup.string().required('This field is required.').email('Please provide a valid email address.'),
  targetRole: yup.string().test('requiredIfAdministrator', 'This field is required.', (value) => {
    if(value) {
      return true
    }
    return !userStore.isAdministrator()
  }).oneOf(['STUDENT', 'INSTRUCTOR'], 'Please select either Student or Instructor')
}))

const { handleSubmit, resetForm } = useForm({
  validationSchema: schema
})

const email = useField<string>('email')
const targetRole = useField<string>('targetRole')

const submit = handleSubmit( (values) => {
  isDisabled.value = true
  let invitation : Invitation
  if("targetRole" in values && values.targetRole != null) {
    invitation = {
      email: values.email,
      target_role: TargetRole[values.targetRole as keyof typeof TargetRole]
    }
  } else {
    invitation = {
      email: values.email,
      target_role: TargetRole.STUDENT
    }
  }
  invitationStore.inviteUser(invitation).then(() => {
        toast.success("Invitation sent")
        resetForm()
      })
      .catch((e) => toast.error(e.message))
      .finally(() => {
        isDisabled.value = false
      })
})

const roles = [
  {
    title: 'Student',
    value: 'STUDENT'
  },
  {
    title: 'Instructor',
    value: 'INSTRUCTOR'
  }
]

</script>

<template>
  <p>With this form, you can invite a <span v-if="userStore.isAdministrator()">user</span><span v-else>student</span> via email.</p><br>
  <v-form @submit="submit">
    <v-text-field
      type="email"
      label="Add Email address"
      variant="underlined"
      base-color="primary"
      color="primary"
      v-model="email.value.value"
      :error-messages="email.errorMessage.value"
    ></v-text-field>
    <v-select
      v-if="userStore.isAdministrator()"
      label="Select target role"
      :items="roles"
      variant="underlined"
      base-color="primary"
      color="primary"
      v-model="targetRole.value.value"
      :error-messages="targetRole.errorMessage.value"
    ></v-select><br>
    <PrimaryButton button-type="submit" :disabled="isDisabled">Invite</PrimaryButton>
  </v-form>
</template>

<style scoped></style>
