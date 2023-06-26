<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import HeaderTurtl from '@/components/HeaderTurtl.vue'
import FooterTurtl from '@/components/FooterTurtl.vue'
import { useField } from 'vee-validate'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/yup'
import * as yup from 'yup'
import { axiosInstance } from '@/stores/AxiosInstance'

const userStore = useUserStore()

const schema = toTypedSchema(
  yup.object({
    oldPassword: yup.string().required('This field is required'),
    newPassword: yup
      .string()
      .required('This field is required')
      .min(8, 'Password needs to be 8 characters long')
      .oneOf([yup.ref('newPasswordValidate')], 'Passwords need to be the same'),
    newPasswordValidate: yup
      .string()
      .required('This field is required')
      .min(8, 'Password needs to be 8 characters long')
      .oneOf([yup.ref('newPassword')], 'Passwords need to be the same')
  })
)

const { handleSubmit } = useForm({ validationSchema: schema })

const { value: oldPassword, errorMessage: oldPasswordError } = useField<string>(
  'oldPassword',
  {},
  { validateOnValueUpdate: false }
)
const { value: newPassword, errorMessage: newPasswordError } = useField<string>(
  'newPassword',
  {},
  { validateOnValueUpdate: false }
)
const { value: newPasswordValidateValue, errorMessage: newPasswordValidateError } =
  useField<string>('newPasswordValidate', {}, { validateOnValueUpdate: false })

const submit = handleSubmit(async (values) => {
  axiosInstance.post('/user/password/change', {
    oldPassword: values.oldPassword,
    newPassword: values.newPassword
  })
})
</script>

<template>
  <HeaderTurtl />
  <v-main class="d-flex justify-center">
    <div class="main-container mt-5 ml-3 mr-3">
      <v-container fluid>
        <h1>Profil</h1>
        <div class="mt-5"><h2>E-Mail Adresse:</h2></div>
        <div>{{ userStore.user?.email }}</div>
        <div class="mt-5"><h2>Change your password:</h2></div>
        <v-form @submit="submit">
          <v-text-field
            v-model="oldPassword"
            :error-messages="oldPasswordError"
            name="oldPassword"
            type="password"
            label="Enter current password"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
          >
          </v-text-field>
          <v-text-field
            v-model="newPassword"
            :error-messages="newPasswordError"
            name="newPassword"
            type="password"
            label="Enter new password"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
          >
          </v-text-field>

          <v-text-field
            v-model="newPasswordValidateValue"
            :error-messages="newPasswordValidateError"
            name="newPasswordValidation"
            type="password"
            label="Confirm new password"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
          >
          </v-text-field>

          <v-btn type="submit" variant="elevated" color="primary" class="elevation-2"
            >Change Password</v-btn
          >
        </v-form>
        <div class="d-flex flex-row mt-5 align-center justify-end">
          <v-btn variant="elevated" color="error" class="elevation-2"
            >Permanently Delete Account</v-btn
          >
        </div>
      </v-container>
    </div>
  </v-main>
  <FooterTurtl />
</template>

<style></style>
