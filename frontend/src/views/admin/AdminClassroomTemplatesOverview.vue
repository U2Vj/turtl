<script setup lang="ts">
import FooterTurtl from '@/components/FooterTurtl.vue'
import HeaderTurtl from '@/components/HeaderTurtl.vue'
import CreateClassroomTemplateModal from '@/components/modals/CreateClassroomTemplateModal.vue'
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
  <HeaderTurtl />
  <v-main class="d-flex justify-center">
    <div class="main-container mt-5 ml-3 mr-3">
      <v-container fluid>
        <div class="d-flex flex-row mb-2 align-center justify-space-between">
          <h1>Classroom Templates</h1>
          <v-btn variant="elevated" color="primary" class="ml-10 elevation-2"
            >Create Template
            <CreateClassroomTemplateModal></CreateClassroomTemplateModal>
          </v-btn>
        </div>
        <v-data-table
          :headers="[
            {
              title: 'Name',
              align: 'start',
              sortable: true,
              key: 'name'
            },
            { title: 'Last Edited', align: 'end', key: 'lastedited' },
            { title: 'Created At', align: 'end', key: 'createdat' },
            { title: 'Use', align: 'end', key: 'link' }
          ]"
          :items="values"
          @click:row="handleRowClick"
        >
          <template #[`item.link`]="{ item }">
            <v-btn variant="text" color="primary" :to="`templates/${item.raw.id}`">Edit</v-btn>
          </template>
        </v-data-table>
      </v-container>
    </div>
  </v-main>
  <FooterTurtl />
</template>

<style scoped></style>
