<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import CreateClassroomModal from '@/components/modals/CreateClassroomModal.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import dayjs from 'dayjs'
import { toRef } from 'vue'
import { useRouter } from 'vue-router'
import {useToast} from "vue-toastification";

const router = useRouter()

const catalogStore = useCatalogStore()
const toast = useToast()

let classroomList = toRef(catalogStore, 'classroomList')

catalogStore.getClassroomList().catch((e) => toast.error(e.message))

function handleRowClick(event: Event, item: { item: { raw: any } }) {
  // Allow text selection.
  // See https://stackoverflow.com/questions/31982407/prevent-onclick-event-when-selecting-text
  const selection = window.getSelection()
  if (selection?.toString().length === 0) {
    router.push(`classrooms/${item.item.raw.id}`)
  }
}
function formatReadableDate(date: string) {
  return dayjs(date).format('DD.MM.YYYY HH:mm')
}
</script>

<template>
  <DefaultLayout>
    <template #heading>Classrooms</template>
    <template #postHeadingButton>
      <PrimaryButton buttonName="Create Classroom">
        <CreateClassroomModal />
      </PrimaryButton>
    </template>
    <template #default>
      <v-data-table
        :headers="[
          {
            title: 'Title',
            align: 'start',
            sortable: true,
            key: 'title'
          },
          { title: 'Last edited', align: 'end', key: 'updated_at' },
          { title: 'Created at', align: 'end', key: 'created_at' },
          { title: 'Edit', align: 'end', key: 'link' }
        ]"
        :items="classroomList"
        @click:row="handleRowClick"
      >
        <template #[`item.link`]="{ item }">
          <TextButton buttonName="Edit" :goTo="`classrooms/${item.raw.id}`"></TextButton>
        </template>
        <template v-slot:[`item.updated_at`]="{ item }">
          {{ formatReadableDate(item.raw.updated_at) }}
        </template>
        <template v-slot:[`item.created_at`]="{ item }">
          {{ formatReadableDate(item.raw.created_at) }}
        </template>
      </v-data-table>
    </template>
  </DefaultLayout>
</template>
