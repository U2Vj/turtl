<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import {useToast} from 'vue-toastification'
import {useInvitationStore} from "@/stores/InvitationStore"
import {useUserStore} from "@/stores/UserStore"
import {useField, useForm} from "vee-validate"
import * as yup from 'yup'
import {toTypedSchema} from "@vee-validate/yup"
import {ref} from "vue"

const userStore = useUserStore()

const invitationStore = useInvitationStore()
const toast = useToast()

const isDisabled = ref(false)

function splitEmailAddresses(inputString: string): string[] {
  return inputString.split(/[;,\s\t\n]+/)
      .filter((address) => address.trim() !== '')
      .map((address) => address.trim())
}

const schema = toTypedSchema(yup.object({
  emails: yup.string()
      .required('This field is required.')
      .test('noEmptyList', 'The list is empty.', (value) => {
        return splitEmailAddresses(value).length != 0
      }).test('noMoreThan30EmailsAtATime', 'You can only invite up to 30 Students at a time.', (value) => {
        return splitEmailAddresses(value).length <= 30
      }).test('noDuplicates', 'The list contains duplicates.', (value) => {
        const uniqueEmails = new Set<string>()
        for (const item of splitEmailAddresses(value)) {
          if (uniqueEmails.has(item)) {
            return false
          }
          uniqueEmails.add(item)
        }
        return true
      }).test('containsInvalidAddresses', 'The list contains invalid email addresses.', (value) => {
        const emailSchema = yup.string().email()
        for(const email of splitEmailAddresses(value)) {
          try {
            emailSchema.validateSync(email)
          } catch (error) {
            return false
          }
        }
        return true
      })
}))

const { handleSubmit, resetForm } = useForm({
  validationSchema: schema
})

const emails = useField<string>('emails')

const submit = handleSubmit( (values) => {
  const emails = splitEmailAddresses(values.emails)
  isDisabled.value = true
  invitationStore.inviteMultipleStudents(emails).then(() => {
    toast.success("Invitations sent")
    resetForm()
  }).catch((e) => toast.error(e.message)).finally(() => {
    isDisabled.value = false
  })
})

</script>

<template>
  <p>
    Here, you can invite multiple Students at once. In the text field below, you can enter a list of email addresses
    separated either by a space, a newline, a comma, a semicolon or any combination of these delimiters.
    <span v-if="userStore.isAdministrator()"> Please note: It is not possible to bulk-invite Instructors.</span>
  </p><br>
  <v-form @submit="submit">
    <v-textarea
      label="Email Addresses"
      variant="underlined"
      base-color="primary"
      color="primary"
      v-model="emails.value.value"
      :error-messages="emails.errorMessage.value"
    ></v-textarea><br>
    <PrimaryButton button-type="submit" :disabled="isDisabled">Invite Students</PrimaryButton>
  </v-form>
</template>

<style scoped></style>