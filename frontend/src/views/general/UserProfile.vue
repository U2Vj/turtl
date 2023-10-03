<script setup lang="ts">
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import { makeAxiosRequest } from '@/stores/AxiosInstance'
import { useUserStore } from '@/stores/UserStore'
import { toTypedSchema } from '@vee-validate/yup'
import { useField, useForm } from 'vee-validate'
import * as yup from 'yup'
import {useToast} from "vue-toastification";

const userStore = useUserStore()
const toast = useToast()

const schema = toTypedSchema(
  yup.object({
    username: yup.string().nullable().test('checkLengthOptional', 'Username needs to be between 2 and 255 characters long',
        (value) => {
          // If there is a value, we want to make sure it more than 2 and less than 255
          if(value) {
            return value.trim().length >= 2 && value.trim().length <= 255
          }
          return true;
        }),
    newPassword: yup.string().test('checkLengthOptional', 'Password needs to be 8 characters long',
        (value) => {
          // If there is a value, i.e. if the password should be updated, it has to be greater than 8
          if(value) {
            return value.length >= 8
          }
          return true;
        }).oneOf([yup.ref('newPasswordValidate')], 'Passwords need to be the same'),
    newPasswordValidate: yup.string().when('newPassword', (newPassword, field) => {
      // When a new password is provided, validate the field. Otherwise it can remain empty
      if(newPassword[0]) {
        return field
            .required('This field is required when updating your password')
            .min(8, 'Password needs to be 8 characters long')
            .oneOf([yup.ref('newPassword')], 'Passwords need to be the same')
      }
      return field
    }),
    oldPassword: yup.string().when( 'newPassword', (newPassword, field) =>
      newPassword[0] ? field.required('This field is required when updating your password') : field
    )
  }
))

const { handleSubmit } = useForm({ validationSchema: schema })

const { value: username, errorMessage: usernameError } = useField<string>(
  'username',
  {},
  {
    validateOnValueUpdate: false,
    initialValue: userStore.refreshTokenPayload?.username
  }
)

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

const submit = handleSubmit(async (values, { setFieldValue }) => {
  // We only want to provide the values that the user actually filled in
  let data = {}

  if('username' in values) {
    // If the username is empty, we have to send username: null to the API. Empty strings are not allowed.
    if(values.username === '') {
      data = Object.assign(data, {username: null})
    } else {
      data = Object.assign(data, {username: values.username?.trim() })
    }
  }
  // If these fields are present, the password should be updated
  if('oldPassword' in values && 'newPassword' in values && 'newPasswordValidate' in values && newPassword.value) {
    data = Object.assign(data, {
      current_password: values.oldPassword,
      new_password: values.newPassword,
      new_password_confirm: values.newPasswordValidate
    })
  }

  const res = await makeAxiosRequest('/users/profile', 'PUT', true, true, data)

  // If the request was successful, we need to refresh the login data to get the updated token claims (e.g. username)
  if(res.success) {
    await userStore.refreshLogin()
    toast.success("Your changes have been saved.")
  } else {
    toast.error(res.message)
  }
  // Reset the password form
  setFieldValue('oldPassword', undefined)
  setFieldValue('newPassword', undefined)
  setFieldValue('newPasswordValidate', undefined)
})
</script>

<template>
  <DefaultLayout>
    <template #heading>Your Profile</template>
    <template #default>
      <v-form @submit="submit">
        <div class="mt-5"><h2>Email address</h2></div>
        <div>{{ userStore.refreshTokenPayload?.email }}</div>
        <div class="mt-5"><h2>Role</h2></div>
        <div>{{ userStore.refreshTokenPayload?.role_display }}</div>
        <div class="mt-5"><h2>Username</h2></div>
        <v-text-field
          v-model="username"
          :error-messages="usernameError"
          name="username"
          type="text"
          label="Your username"
          variant="underlined"
          base-color="primary"
          color="primary"
        ></v-text-field>
        <small v-if="userStore.refreshTokenPayload?.username == null">
          You did not set a username yet.
        </small>
        <small v-if="userStore.refreshTokenPayload?.username != null">
          Usernames are optional. To remove your username, simply clear the text box.
        </small>
        <div class="mt-5"><h2>Change your password</h2></div>
        <v-text-field
          v-model="oldPassword"
          :error-messages="oldPasswordError"
          name="oldPassword"
          type="password"
          label="Enter current password"
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
          variant="underlined"
          base-color="primary"
          color="primary"
        >
        </v-text-field>
        <PrimaryButton buttonName="Save changes" buttonType="submit"> </PrimaryButton>
      </v-form>
      <div class="d-flex flex-row mt-5 align-center justify-end">
        <ErrorButton buttonName="Permanently Delete Account"></ErrorButton>
      </div>
    </template>
  </DefaultLayout>
</template>
