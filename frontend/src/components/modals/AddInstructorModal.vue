<script setup lang="ts">
import TextButton from '@/components/buttons/TextButton.vue'
import type { User } from '@/stores/CatalogStore'
import { useCatalogStore } from '@/stores/CatalogStore'
import { useAxios } from '@vueuse/integrations/useAxios'
import { ref } from 'vue'
import {makeAxiosRequest} from "@/stores/AxiosInstance";
import {useToast} from "vue-toastification";

const catalogStore = useCatalogStore()
const response = await makeAxiosRequest("/users/instructors", 'GET', true, true)
const instructors: any[] = []
if(response.success) {
} else {
  useToast().error(response.message)
}
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
