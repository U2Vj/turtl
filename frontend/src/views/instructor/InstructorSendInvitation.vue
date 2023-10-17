<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import {ref} from 'vue'
import InviteSingleUser from "@/components/tabs/InviteSingleUser.vue";
import InviteMultipleUsers from "@/components/tabs/InviteMultipleUsers.vue";

const tab = ref("single")

</script>

<template>
  <DefaultLayout>
    <template #heading>Invite Users</template>
    <template #default>
      <v-tabs v-model="tab" color="primary">
        <v-tab value="single">Single User</v-tab>
        <v-tab value="multiple">Multiple Users</v-tab>
      </v-tabs>
      <v-window v-model="tab" class="mt-5">
        <v-window-item eager value="single">
          <InviteSingleUser />
        </v-window-item>
        <v-window-item eager value="multiple">
          <InviteMultipleUsers />
        </v-window-item>
      </v-window>
    </template>
  </DefaultLayout>
</template>

<style scoped></style>
