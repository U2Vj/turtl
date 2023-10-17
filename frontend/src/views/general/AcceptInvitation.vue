<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import { toTypedSchema } from '@vee-validate/yup'
import { useField, useForm } from 'vee-validate'
import { useRouter } from 'vue-router'
import * as yup from 'yup'
import {useToast} from "vue-toastification"
import {ref} from "vue"
import {makeAPIRequest} from "@/communication/APIRequests"

const router = useRouter()
const toast = useToast()

const submitButtonDisabled = ref(false)

const schema = toTypedSchema(
  yup.object({
    email: yup
      .string()
      .required('This field is required')
      .email('Please enter a valid email address'),
    password: yup
        .string()
        .required('This field is required')
        .min(8, 'Password needs to be 8 characters long'),
    passwordConfirm: yup
        .string()
        .required('This field is required')
        .oneOf([yup.ref('password')], 'Passwords do not match')
  })
)
const { handleSubmit } = useForm({ validationSchema: schema })

const { value: emailValue, errorMessage: emailError } = useField<string>(
  'email',
  {},
  { validateOnValueUpdate: false }
)
const { value: passwordValue, errorMessage: passwordError } = useField<string>(
  'password',
  {},
  { validateOnValueUpdate: false }
)
const { value: passwordConfirmValue, errorMessage: passwordConfirmError } = useField<string>(
  'passwordConfirm',
  {},
  { validateOnValueUpdate: false }
)

const submit = handleSubmit((values) => {
  submitButtonDisabled.value = true
  const requestBody = {
    email: values.email,
    password: values.password,
    token: router.currentRoute.value.query.token
  }
  makeAPIRequest('/users/invitations/accept', 'POST', false, false, requestBody)
      .then(() => {
        toast.success("You have registered successfully and you can now log in using your credentials.")
        router.push({ name: 'signin' })
      })
      .catch((e) => toast.error(e.message))
      .finally(() => {
        submitButtonDisabled.value = false
      })
})
</script>

<template>
  <div id="background">
    <div id="container" class="d-flex flex-column justify-center align-center">
      <div class="d-flex align-center">
        <v-img src="@/assets/logo.svg" width="150"></v-img>
        <h1 class="text-h3 ml-5 font-weight-bold">Virtual Network Security Lab</h1>
      </div>
      <v-sheet class="pa-10 elevation-24 mt-10" width="500" max-width="100%">
        <v-form @submit="submit">
          <div class="text-h4 font-weight-bold text-center mb-4">Register</div>
          <p class="text-center mb-2">You have been invited to join TURTL.</p>
          <p class="text-center">Please register using the email address your invitation was sent to.</p>
          <br>
          <v-text-field
            v-model="emailValue"
            :error-messages="emailError"
            name="email"
            type="email"
            label="Email"
            placeholder="john.doe@example.com"
          ></v-text-field>
          <v-text-field
            v-model="passwordValue"
            :error-messages="passwordError"
            type="password"
            label="Password"
            placeholder="Password"
          ></v-text-field>
          <v-text-field
            v-model="passwordConfirmValue"
            :error-messages="passwordConfirmError"
            type="password"
            label="Confirm Password"
            placeholder="Confirm Password"
          ></v-text-field><br>
          <PrimaryButton button-name="Register" button-type="submit" :disabled="submitButtonDisabled"></PrimaryButton>
        </v-form>
      </v-sheet>
    </div>
  </div>
</template>

<style scoped>
  #container {
    height: fit-content;
    min-height: 100vh;
    position: relative;
  }

  #background::before {
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
