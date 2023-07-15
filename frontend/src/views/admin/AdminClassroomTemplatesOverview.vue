<script setup lang="ts">
import FooterTurtl from '@/components/FooterTurtl.vue'
import HeaderTurtl from '@/components/HeaderTurtl.vue'
import CreateClassroomTemplateModal from '@/components/modals/CreateClassroomTemplateModal.vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { useRouter } from 'vue-router'

const router = useRouter()
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
            { title: 'Last Edited', align: 'end', key: 'updated_at' },
            { title: 'Created At', align: 'end', key: 'created_at' },
            { title: 'Use', align: 'end', key: 'link' }
          ]"
          :items="templateStore.basicTemplateData"
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
