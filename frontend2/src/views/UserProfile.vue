<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { ref } from 'vue'
import TurtlHeader from '@/components/TurtlHeader.vue'

const userStore = useUserStore()
const user = ref(userStore.user || null)

type snackbarOptionsType = {
  timeout: number
  text: string
  color: string
}

const snackbarOptions = {
  error: {
    timeout: 2000,
    text: 'E-Mail or currenrt password incorrect!',
    color: 'error'
  },
  success: {
    timeout: 2000,
    text: 'Password successfully changed!',
    color: 'success'
  },
  fillAll: {
    timeout: 2000,
    text: 'Type in all passwords!',
    color: 'error'
  },
  notTheSame: {
    timeout: 2000,
    text: 'New passwords are not the same!',
    color: 'error'
  },
  noUserLogedIn: {
    timeout: 2000,
    text: 'No user is currently logged in!',
    color: 'error'
  },
  errorAtReset: {
    timeout: 2000,
    text: 'An error occured! The password cound not be reset! Try Again!',
    color: 'error'
  }
}

const snackbar = ref<snackbarOptionsType>({ timeout: 0, text: '', color: '' })
const showSnackbar = ref(false)

function showErrorMessage() {
  snackbar.value = snackbarOptions.error
  showSnackbar.value = true
}
function showChangesPasswordMessage() {
  snackbar.value = snackbarOptions.success
  showSnackbar.value = true
}
function showFillAllMessage() {
  snackbar.value = snackbarOptions.fillAll
  showSnackbar.value = true
}
function showNotAllTheSame() {
  snackbar.value = snackbarOptions.notTheSame
  showSnackbar.value = true
}
function showNoUserMessage() {
  snackbar.value = snackbarOptions.noUserLogedIn
  showSnackbar.value = true
}
function showErrorReset() {
  snackbar.value = snackbarOptions.errorAtReset
  showSnackbar.value = true
}

const inputs = ref([
  {
    id: '1',
    label: 'Enter your current password',
    password: ''
  },
  {
    id: '2',
    label: 'Enter your new password',
    password: ''
  },
  {
    id: '3',
    label: 'Confirm your new password',
    password: ''
  }
])

async function resetPassword() {
  if (user.value) {
    for (const input of inputs.value) {
      if (!input.password) {
        showFillAllMessage()
        return
      }
    }
    if (inputs.value[1].password !== inputs.value[2].password) {
      showNotAllTheSame()
      return
    }
    const isCurrentPasswordValid = await userStore.login({
      user: { email: user.value.email, password: inputs.value[0].password }
    })
    if (isCurrentPasswordValid) {
      const successReset = await userStore.resetPassword(user.value.email, inputs.value[1].password)
      if (successReset) {
        alert('Password sucesfully changed!')
        showChangesPasswordMessage()
      } else if (!successReset) {
        showErrorReset()
      }
    } else if (!isCurrentPasswordValid) {
      showErrorMessage()
    }
  } else {
    showNoUserMessage()
  }
}
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-snackbar v-model="showSnackbar" :timeout="snackbar.timeout" :color="snackbar.color">
        {{ snackbar.text }}
      </v-snackbar>
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
          <p v-if="user">{{ user.email }}</p>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12" offset="1">
          <h3 class="headlineTitle">Change your password:</h3>
        </v-col>
        <v-col cols="12" sm="8" md="4" offset="1">
          <v-sheet class="mr-auto">
            <v-form @submit.prevent>
              <v-text-field
                type="password"
                v-for="input in inputs"
                :key="input.id"
                :label="input.label"
                v-model="input.password"
                variant="solo"
              ></v-text-field>
              <v-btn type="submit" variant="outlined" @click="resetPassword">Change Password</v-btn>
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
