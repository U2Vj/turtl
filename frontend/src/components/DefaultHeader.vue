<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router'
import {useToast} from "vue-toastification";
import LogoutMenu from '@/components/menus/LogoutMenu.vue'

const router = useRouter()
const userStore = useUserStore()
const toast = useToast()

function handleLogout() {
  userStore.logout(router)
  toast.info("You have been signed out.")
}

</script>

<template>
  <div>
    <v-app-bar sticky color="cardColor" class="elevation-4">
      <div class="flex-grow-1">
        <v-btn to="/student/dashboard">S Dashboard</v-btn>
        <v-btn to="/student/enrollments">S My Classrooms</v-btn>
        <v-btn to="/student/classrooms/all">S All Classrooms</v-btn>
        <v-btn to="/instructor/classrooms">I Classrooms</v-btn>
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
  </div>
</template>
