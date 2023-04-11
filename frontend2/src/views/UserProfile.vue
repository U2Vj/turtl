<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import TurtlHeader from '@/components/TurtlHeader.vue'
import { useField } from 'vee-validate'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/yup'
import * as yup from 'yup'

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

const { value: oldPasswordValue, errorMessage: oldPasswordError } = useField<string>(
  'oldPassword',
  {},
  { validateOnValueUpdate: false }
)
const { value: newPasswordValue, errorMessage: newPasswordError } = useField<string>(
  'newPassword',
  {},
  { validateOnValueUpdate: false }
)
const { value: newPasswordValidateValue, errorMessage: newPasswordValidateError } =
  useField<string>('newPasswordValidate', {}, { validateOnValueUpdate: false })

const submit = handleSubmit(async (values) => {
  // TODO: Add backend route change Password
})
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row no-gutters>
        <v-col cols="12" sm="8" md="4" offset="1" class="mt-8">
          <h1 class="title">Profil</h1>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12" offset="1">
          <h3 class="headlineTitle">E-Mail Adresse:</h3>
        </v-col>
        <v-col offset="1">
          <p>{{ userStore.user?.email }}</p>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12" offset="1">
          <h3 class="headlineTitle">Change your password:</h3>
        </v-col>
        <v-col cols="12" sm="8" md="4" offset="1">
          <v-sheet class="mr-auto">
            <v-form @submit="submit">
              <v-text-field
                v-model="oldPasswordValue"
                :error-messages="oldPasswordError"
                name="oldPassword"
                type="password"
                label="Enter current password"
              >
              </v-text-field>
              <v-text-field
                v-model="newPasswordValue"
                :error-messages="newPasswordError"
                name="newPassword"
                type="password"
                label="Enter new password"
              >
              </v-text-field>

              <v-text-field
                v-model="newPasswordValidateValue"
                :error-messages="newPasswordValidateError"
                name="newPasswordValidation"
                type="password"
                label="Confirm new password"
              >
              </v-text-field>

              <v-btn type="submit" variant="outlined">Change Password</v-btn>
            </v-form>
          </v-sheet>
        </v-col>
      </v-row>
      <v-row justify="end">
        <v-col cols="12" sm="6" md="3" offset="1">
          <v-btn variant="outlined">Permanently Delete Account</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<style>
.divMargins {
  text-align: left;
  margin: auto;
  margin-left: 5%;
  margin-top: 2%;
}
.title {
  font-weight: bolder;
  margin-bottom: 2%;
}
.headlineTitle {
  font-weight: bolder;
  margin-top: 1%;
  margin-bottom: 1%;
}
</style>
