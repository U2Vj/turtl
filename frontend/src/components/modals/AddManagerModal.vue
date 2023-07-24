<script setup lang="ts">
import TextButton from '@/components/buttons/TextButton.vue'
import type { User } from '@/stores/TemplateStore'
import { useTemplateStore } from '@/stores/TemplateStore'
import { useAxios } from '@vueuse/integrations/useAxios'
import { ref } from 'vue'

const templateStore = useTemplateStore()
const { data: AllManagers } = useAxios<User[]>(`${import.meta.env.VITE_API_URL}/users/managers`)
const managers = AllManagers.value?.filter((element: User) => {
  return !templateStore.classroomTemplate?.managers.includes(element)
})
const showDialog = ref(false)
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Add Managers</v-card-title>
      <v-card-text>
        <v-data-table
          :headers="[
            { title: 'E-Mail', key: 'email' },
            { title: 'Add', key: 'add' }
          ]"
          :items="managers"
        >
          <template #[`item.add`]="{ item }">
            <v-btn
              icon="mdi-plus"
              variant="elevated"
              color="primary"
              @click="
                () => {
                  templateStore.addManager(item.raw.id, item.raw.email)
                }
              "
            />
          </template>
        </v-data-table>
        <TextButton buttonName="Close" @atClick="showDialog = false"></TextButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
