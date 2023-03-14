<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const router = useRouter()
const userStore = useUserStore()

type snackbarOptionsType = {
  timeout: number
  text: string
  color: string
}

const snackbarOptions = {
  error: {
    timeout: 2000,
    text: 'E-Mail or Password incorrect!',
    color: 'error'
  },
  success: {
    timeout: 2000,
    text: 'Signin successful',
    color: 'success'
  }
}

const snackbar = ref<snackbarOptionsType>({ timeout: 0, text: '', color: '' })
const showSnackbar = ref(false)

async function handleLogin() {
  const success = await userStore.login({ user: { email: email.value, password: password.value } })
  if (success) {
    showLoginMessage()
    router.push({ path: '/home' })
  } else if (!success) {
    showErrorMessage()
  }
}

function showErrorMessage() {
  snackbar.value = snackbarOptions.error
  showSnackbar.value = true
}
function showLoginMessage() {
  snackbar.value = snackbarOptions.success
  showSnackbar.value = true
}

function validateEmail(email: string) {
  // eslint-disable-next-line no-useless-escape
  const re =
    /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  return re.test(String(email).toLowerCase())
}

const validEmail = computed(() => {
  return validateEmail(email.value)
})

const validPassword = computed(() => {
  return password.value.length >= 3
})
const validInput = computed(() => {
  return validEmail.value && validPassword.value
})
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
        <div class="text-h4 font-weight-bold text-center mb-4">Login</div>
        <v-text-field
          id="input-email"
          v-model="email"
          type="email"
          label="Email"
          :state="validEmail"
          placeholder="john.doe@example.com"
        ></v-text-field>
        <v-text-field
          id="input-name"
          v-model="password"
          type="password"
          label="Password"
          placeholder="Password"
        ></v-text-field>
        <v-btn color="primary" block :disabled="!validInput" @click="handleLogin">Sign In</v-btn>
      </v-form>
      <router-link class="d-block mt-5" to="/recover">Forgot your password?</router-link>
    </v-sheet>
  </div>
</template>

<style>
#container {
  height:fit-content;
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
