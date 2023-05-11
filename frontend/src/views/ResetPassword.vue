<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { toTypedSchema } from '@vee-validate/yup'
import * as yup from 'yup'
import { useField, useForm } from 'vee-validate'

const password = ref('')
const repeatPassword = ref('')
const router = useRouter()
const userStore = useUserStore()

const schema = toTypedSchema(
  yup.object({
    newPassword: yup
      .string()
      .required('This field is required')
      .min(8, 'Password needs to be 8 characters long')
      .oneOf([yup.ref('newPasswordConfirm')], 'Passwords need to be the same'),
    newPasswordValidate: yup
      .string()
      .required('This field is required')
      .min(8, 'Password needs to be 8 characters long')
      .oneOf([yup.ref('newPassword')], 'Passwords need to be the same')
  })
)

const { handleSubmit } = useForm({ validationSchema: schema })
const { value: newPassword, errorMessage: newPasswordError } = useField<string>(
  'newPassword',
  {},
  { validateOnValueUpdate: false }
)
const { value: newPasswordConfirm, errorMessage: newPasswordConfirmError } = useField<string>(
  'newPasswordConfirm',
  {},
  { validateOnValueUpdate: false }
)

const submit = handleSubmit(async (values) => {
  //TODO:
})

/*
 async function handlePasswordReset () {
   if (password.value) {
     var errorStatus
     await axios.post('http://localhost:8000/api/password-reset-complete', {
       password: password.value,
       uidb64: $route.params.uidb64,
       token: $route.params.token,
       passwordConfirm: repeatPassword.value
     }).catch(function (error) {
       if (error.response) {
         errorStatus = error.response.status
       }
     })
     if (errorStatus === 401) {
       showErrorMessage()
     } else {
       showSuccessMessage()
       this.$router.push({path: '/signin'})
     }
   }
 }


})*/
</script>

<template>
  <div id="container" class="d-flex flex-column justify-center align-center">
    <v-snackbar v-model="showSnackbar" :timeout="snackbar.timeout" :color="snackbar.color">
      {{ snackbar.text }}
    </v-snackbar>
    <div class="d-flex align-center">
      <v-img src="@/assets/logo.svg" width="150"></v-img>
      <h1 class="text-h3 ml-5 font-weight-bold">Virtual Network Security Lab</h1>
    </div>
    <v-sheet class="pa-10 elevation-24 mt-10" width="500" max-width="100%">
      <v-form>
        <div class="text-h4 font-weight-bold text-center mb-4">Reset Password</div>
        <v-text-field
          id="input-password"
          v-model="newPassword"
          :error-messages="newPasswordError"
          type="email"
          label="Password"
          placeholder="Enter your new password"
        ></v-text-field>
        <v-text-field
          id="repeat-password"
          v-model="newPasswordConfirm"
          :error-messages="newPasswordConfirmError"
          type="password"
          placeholder="Confirm your password"
        ></v-text-field>
        <v-btn type="submit" color="primary">Set new password</v-btn>
      </v-form>
      <router-link class="d-block mt-5" to="/">Back to sign in</router-link>
    </v-sheet>
  </div>
</template>

<style scoped>
#container {
  height: fit-content;
  min-height: 100vh;
}

#container::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  background-image: url(@/assets/logo.svg);
  background-size: contain;
  background-repeat: space;
  opacity: 0.2;
}
</style>
