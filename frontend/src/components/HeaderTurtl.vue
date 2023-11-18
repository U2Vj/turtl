<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

function handleLogout() {
  userStore.logout(router)
  toast.info('You have been signed out.')
}
</script>

<template>
  <div>
    <v-app-bar sticky color="cardColor" class="elevation-4">
      <div v-if="userStore.isAdministrator()" class="flex-grow-1">
        <v-btn to="/instructor/classrooms/my">My Classrooms</v-btn>
        <v-btn to="/student/enrollments">My Enrollments</v-btn>
        <v-btn to="/instructor/invitations">Invite Users</v-btn>
      </div>
      <div v-if="userStore.isInstructor()" class="flex-grow-1">
        <v-btn to="/instructor/classrooms/my">My Classrooms</v-btn>
        <v-btn to="/student/enrollments">My Enrollments</v-btn>
        <v-btn to="/instructor/invitations">Invite Users</v-btn>
      </div>
      <div v-if="userStore.isStudent()" class="flex-grow-1">
        <v-btn to="/student/enrollments">My Enrollments</v-btn>
        <v-btn to="/student/classrooms/all">All Classrooms</v-btn>
      </div>
      <template #prepend>
        <router-link to="/">
          <!-- TODO: change img to v-img for consistency.
          v-img did rerender the image on every page change tho.
          Giving it eager did not help.-->
          <img src="@/assets/logo.svg" width="75" />
        </router-link>
      </template>

      <template #append>
        <v-menu>
          <template #activator="{ props }">
            <v-btn icon="mdi-dots-vertical" v-bind="props"> </v-btn>
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
    </v-app-bar>
  </div>
</template>
