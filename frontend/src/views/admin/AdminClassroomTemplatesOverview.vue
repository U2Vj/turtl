<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import CreateClassroomTemplateModal from '@/components/modals/CreateClassroomTemplateModal.vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { useRouter } from 'vue-router'

const router = useRouter()

const values = [
  {
    name: 'Computer Networks',
    lastedited: '2022-12-12',
    createdat: '2021-01-02',
    id: 1
  },
  {
    name: 'Computer Networks',
    lastedited: '2022-12-12',
    createdat: '2021-01-02',
    id: 2
  }
]

const templateStore = useTemplateStore()

// TODO: find way to import DataTableItem from vuetify
function handleRowClick(event: Event, item: { item: { raw: any } }) {
  // Allow text selection.
  // See https://stackoverflow.com/questions/31982407/prevent-onclick-event-when-selecting-text
  const selection = window.getSelection()
  if (selection?.toString().length === 0) {
    router.push(`templates/${item.item.raw.id}`)
  }
}
</script>

<template>
  <DefaultLayout>
    <template #heading>Classroom Templates</template>
    <template #postHeadingButton>
      <PrimaryButton buttonName="Create Template">
        <CreateClassroomTemplateModal />
      </PrimaryButton>
    </template>
    <template #default>
      <v-data-table
        :headers="[
          {
            title: 'Name',
            align: 'start',
            sortable: true,
            key: 'name'
          },
          { title: 'Last Edited', align: 'end', key: 'updated_at' },
          { title: 'Created At', align: 'end', key: 'created_at' },
          { title: 'Use', align: 'end', key: 'link' }
        ]"
        :items="values"
        @click:row="handleRowClick"
      >
        <template #[`item.link`]="{ item }">
          <TextButton buttonName="Edit" :goTo="`templates/${item.raw.id}`"></TextButton>
        </template>
      </v-data-table>
    </template>
  </DefaultLayout>
</template>
