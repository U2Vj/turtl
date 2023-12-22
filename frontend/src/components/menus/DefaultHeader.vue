<script setup lang="ts">
import LogoutMenu from '@/components/menus/LogoutMenu.vue'
import { useUserStore } from '@/stores/UserStore'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

function handleLogout() {
  userStore.logout(router)
  toast.info('You have been signed out.')
}

const drawer = ref(false)
</script>

<template>
  <div>
    <v-app-bar sticky color="cardColor" class="elevation-4">
      <v-app-bar-nav-icon @click="drawer = true" class="d-flex d-sm-none"></v-app-bar-nav-icon>
      <div v-if="userStore.isAdministrator()" class="flex-grow-1 d-none d-sm-flex">
        <v-btn to="/instructor/classrooms/my">My Classrooms</v-btn>
        <v-btn to="/student/enrollments">My Enrollments</v-btn>
        <v-btn to="/instructor/invitations">Manage Invitations</v-btn>
      </div>
      <div v-if="userStore.isInstructor()" class="flex-grow-1 d-none d-sm-flex">
        <v-btn to="/instructor/classrooms/my">My Classrooms</v-btn>
        <v-btn to="/student/enrollments">My Enrollments</v-btn>
        <v-btn to="/instructor/invitations">Manage Invitations</v-btn>
      </div>
      <div v-if="userStore.isStudent()" class="flex-grow-1 d-none d-sm-flex">
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
        <LogoutMenu />
      </template>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" absolute temporary color="cardColor">
      <v-list nav dense>
        <v-list-item-group v-if="userStore.isAdministrator()">
          <v-list-item to="/instructor/classrooms/my">
            <v-list-item-title>My Classrooms</v-list-item-title>
          </v-list-item>
          <v-list-item to="/student/enrollments">
            <v-list-item-title>My Enrollments</v-list-item-title>
          </v-list-item>
          <v-list-item to="/instructor/invitations">
            <v-list-item-title>Invite Users</v-list-item-title>
          </v-list-item>
        </v-list-item-group>

        <v-list-item-group v-if="userStore.isInstructor()">
          <v-list-item to="/instructor/classrooms/my">
            <v-list-item-title>My Classrooms</v-list-item-title>
          </v-list-item>
          <v-list-item to="/student/enrollments">
            <v-list-item-title>My Enrollments</v-list-item-title>
          </v-list-item>
          <v-list-item to="/instructor/invitations">
            <v-list-item-title>Invite Users</v-list-item-title>
          </v-list-item>
        </v-list-item-group>

        <v-list-item-group v-if="userStore.isStudent()">
          <v-list-item to="/student/enrollments">
            <v-list-item-title>My Enrollments</v-list-item-title>
          </v-list-item>
          <v-list-item to="/student/classrooms/all">
            <v-list-item-title>All Classrooms</v-list-item-title>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>
