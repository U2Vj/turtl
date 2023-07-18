<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { toTypedSchema } from '@vee-validate/yup'
import { useField, useForm } from 'vee-validate'
import { useRouter } from 'vue-router'
import PrimaryButton from '@/components/layouts/PrimaryButton.vue';
import * as yup from 'yup'

const router = useRouter()
const userStore = useUserStore()

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

// validateOnValueUpdate cant be set on form level. See https://github.com/logaretm/vee-validate/issues/3771
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

const submit = handleSubmit(async (values) => {
  const success = await userStore.login({
    user: { email: values.email, password: values.password }
  })
  if (success) {
    router.push({ path: '/profile' })
  }
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
          <PrimaryButton buttonName="Sign In" buttonType="submit">
          </PrimaryButton>
        </v-form>
        <router-link class="d-block mt-5" to="/forgot-password">Forgot your password?</router-link>
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
