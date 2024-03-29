<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import { useUserStore } from '@/stores/UserStore'
import { toTypedSchema } from '@vee-validate/yup'
import { useField, useForm } from 'vee-validate'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import * as yup from 'yup'

const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

const schema = toTypedSchema(
  yup.object({
    email: yup
      .string()
      .required('This field is required')
      .email('Please enter a valid email address'),
    password: yup.string().required('This field is required')
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

const submit = handleSubmit((values) => {
  userStore
    .login({
      email: values.email,
      password: values.password
    })
    .then(() => {
      if (userStore.isAdministrator()) {
        router.push({ name: 'InstructorMyClassrooms' })
      } else if (userStore.isInstructor()) {
        router.push({ name: 'InstructorMyClassrooms' })
      } else if (userStore.isStudent()) {
        router.push({ name: 'StudentMyEnrollments' })
      } else {
        router.push({ name: 'UserProfile' })
      }
      toast.info('Welcome back!')
    })
    .catch((e) => {
      toast.error(e.message)
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
          <div class="text-h4 font-weight-bold text-center mb-4">Login</div>
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
            name="password"
            type="password"
            label="Password"
            placeholder="Password"
          ></v-text-field>
          <PrimaryButton buttonName="Sign In" buttonType="submit"></PrimaryButton>
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
