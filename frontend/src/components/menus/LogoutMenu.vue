<script setup lang="ts">
import {useRouter} from 'vue-router'
import {useUserStore} from '@/stores/UserStore'
import {useToast} from 'vue-toastification'

const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

function handleLogout() {
  userStore.logout(router)
  toast.info("You have been signed out.")
}
</script>

<template>
  <v-menu>
    <template #activator="{ props }">
      <v-btn icon="mdi-dots-vertical" v-bind="props"></v-btn>
    </template>
    <v-list>
      <v-list-item to="/profile">
        <template #prepend>
          <v-icon icon="mdi-account"></v-icon>
        </template>
        <v-list-item-title>Profile</v-list-item-title>
      </v-list-item>
      <v-list-item @click="handleLogout">
        <template #prepend>
          <v-icon icon="mdi-logout"></v-icon>
        </template>
        <v-list-item-title>Logout</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>
