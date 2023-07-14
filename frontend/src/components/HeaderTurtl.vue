<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()
</script>

<template>
  <div>
    <v-app-bar sticky color="cardColor" class="elevation-4">
      <div class="flex-grow-1">
        <v-btn to="/student/dashboard">S Dashboard</v-btn>
        <v-btn to="/student/classrooms">S Classroom Enroled</v-btn>
        <v-btn to="/student/classrooms/all">S Classrooms All</v-btn>
        <v-btn to="/admin/templates">A Templates</v-btn>
        <v-btn to="/manager/classrooms">M Classrooms</v-btn>
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
            <v-list-item @click="userStore.signOut(router)">
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
