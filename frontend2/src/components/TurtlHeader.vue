<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()
</script>

<template>
  <div>
    <v-app-bar sticky>
      <div class="flex-grow-1">
        <v-btn to="/dashboard">Dashboard</v-btn>
        <v-btn to="/classrooms">Classrooms</v-btn>
      </div>
      <template v-slot:prepend>
        <router-link to="/">
          <v-img src="@/assets/logo.svg" width="75px"></v-img>
        </router-link>
      </template>

      <template v-slot:append>
        <v-menu>
          <template v-slot:activator="{ props }">
            <v-btn icon="mdi-dots-vertical" v-bind="props"> </v-btn>
          </template>
          <v-list>
            <v-list-item to="/profile">
              <template v-slot:prepend>
                <v-icon icon="mdi-account"></v-icon>
              </template>
              <v-list-item-title>Profile</v-list-item-title>
            </v-list-item>
            <v-list-item @click="userStore.logout(router)">
              <template v-slot:prepend>
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
