<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import CreateClassroomTemplateModal from '@/components/modals/CreateClassroomTemplateModal.vue'
import { makeAxiosRequest } from '@/stores/AxiosInstance'
import { useTemplateStore } from '@/stores/TemplateStore'
import { toRef } from 'vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const templateStore = useTemplateStore()

const props = defineProps<{ templateId: string }>()

let templateData = toRef(templateStore, 'classroomTemplate')
templateStore.fetchTemplate(props.templateId)

// TODO: find way to import DataTableItem from vuetify
function handleRowClick(event: Event, item: { item: { raw: any } }) {
  // Allow text selection.
  // See https://stackoverflow.com/questions/31982407/prevent-onclick-event-when-selecting-text
  const selection = window.getSelection()
  if (selection?.toString().length === 0) {
    router.push(`templates/${item.item.raw.id}`)
  }
}

const fetchedData = ref(null)

const fetchData = async () => {
  const response = await makeAxiosRequest('/templates/classrooms', 'GET', true, true)

  if (response.success) {
    fetchedData.value = response.data
  } else {
    console.error('An error occurred:', response.message)
  }
}
</script>

<template>
  <DefaultLayout v-if="templateData">
    <template #heading>Classroom Templates</template>
    <template #postHeadingButton>
      <PrimaryButton buttonName="Create Template">
        <CreateClassroomTemplateModal />
      </PrimaryButton>
    </template>
    <template #default>
      <p>{{ templateData.updated_at }}</p>
      <v-data-table
        :headers="[
          {
            title: 'Name',
            align: 'start',
            sortable: true,
            key: 'title'
          },
          { title: 'Last Edited', align: 'end', key: 'updated_at' },
          { title: 'Created At', align: 'end', key: 'created_at' },
          { title: 'Use', align: 'end', key: 'link' }
        ]"
        :items="[templateData]"
        @click:row="handleRowClick"
      >
        <template #[`item.link`]="{ item }">
          <TextButton buttonName="Edit" :goTo="`templates/${item.raw.id}`"></TextButton>
        </template>
      </v-data-table>
      <PrimaryButton buttonName="Fetch Data" @click="fetchData"></PrimaryButton>
      <div v-if="fetchedData">
        <p>{{ fetchedData }}</p>
      </div>
    </template>
  </DefaultLayout>
</template>
