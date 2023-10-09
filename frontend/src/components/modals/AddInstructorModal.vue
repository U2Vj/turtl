<script setup lang="ts">
import TextButton from '@/components/buttons/TextButton.vue'
import { ref } from 'vue'
import { makeAPIRequest } from "@/communication/APIRequests";
import {useToast} from "vue-toastification";
import type {User} from "@/stores/UserStore";

const toast = useToast()
const instructors = ref<User[]>()


makeAPIRequest("/users/instructors", 'GET', true, true).then((response) => {
  instructors.value = response.data
}).catch((e) => {
  toast.error(e.message)
})

const showDialog = ref(false)
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Add Instructors</v-card-title>
      <v-card-text>
        <v-data-table
          :headers="[
            { title: 'E-Mail', key: 'email' },
            { title: 'Add', key: 'add' }
          ]"
          :items="instructors"
        >
          <template #[`item.add`]="{ item }">
            <v-btn
              icon="mdi-plus"
              variant="elevated"
              color="primary"
              @click="
                () => {
                  //catalogStore.addInstructor(item.raw.id, item.raw.email)
                }
              "
            />
          </template>
        </v-data-table>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
