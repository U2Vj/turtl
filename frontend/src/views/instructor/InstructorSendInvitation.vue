<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import InviteMultipleUsers from '@/components/tabs/InviteMultipleUsers.vue'
import InviteSingleUser from '@/components/tabs/InviteSingleUser.vue'
import type { Ref } from 'vue'
import { ref } from 'vue'

const tab = ref('single')
const breadcrumbItems: Ref<any[]> = ref([])
breadcrumbItems.value = [
  {
    title: 'Manage Invitations',
    disabled: false,
    to: {
      name: 'InstructorInvitationList'
    }
  },
  {
    title: 'Invite Users',
    disabled: true
  }
]
</script>

<template>
  <DefaultLayout>
    <template #heading>Invite Users</template>
    <template #default>
      <v-row>
        <v-col>
          <v-breadcrumbs :items="breadcrumbItems" density="compact"></v-breadcrumbs>
        </v-col>
      </v-row>
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
