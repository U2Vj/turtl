<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'


const email = ref('')
const router = useRouter()
const userStore = useUserStore()

type snackbarOptionsType = {
  timeout: number
  text: string
  color: string
}

const snackbar = ref<snackbarOptionsType>({ timeout: 2000, text: 'Password reset email was send successful', color: 'success' })

const showSnackbar = ref(false)

function showSuccessMessage() {
  showSnackbar.value = true
}

async function handlePasswordResetRequest () {
  if (email) {
    showSuccessMessage()
    await userStore.resetPasswordRequest(email.value)
    router.push({ path: '/signin' })
  }
}


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
        <div class="text-h4 font-weight-bold text-center mb-4">Forgot Password</div>
        <v-text-field
          id="input-email"
          v-model="email"
          type="email"
          label="Email"
          :state="validEmail"
          placeholder="john.doe@example.com"
        ></v-text-field>
        <v-btn color="primary" block :disabled="!validInput" @click="handleLogin">Send password reset email</v-btn>
      </v-form>
      <router-link class="d-block mt-5" to="/recover">Back to sign in</router-link>
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