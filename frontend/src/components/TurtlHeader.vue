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
        <v-btn to="/dashboard-prof">Classroom I??</v-btn>
        <v-btn to="/createclassroominstance">CreateClass I</v-btn>
        <v-btn to="/classrooms">Classrooms I</v-btn>
        <v-btn to="/studentclassrooms">MyClass S</v-btn>
        <v-btn to="/allclassrooms-stud">AllClass S</v-btn>
        <v-btn to="/dashboard">Dashboard S</v-btn>
        <v-btn to="/studentclassprojects">ClassProjects S</v-btn>
        <v-btn to="/edittasktemplate">EditTaskTemplate M</v-btn>
        <v-btn to="/templates">ClassTemplates M</v-btn>
        <v-btn to="/classrooms/:id">Task S</v-btn>
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
