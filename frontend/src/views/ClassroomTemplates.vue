<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import Footer from '@/components/Footer.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// TODO: change mock data with api call
const headers = [
  {
    title: 'Name',
    align: 'start',
    sortable: true,
    key: 'name'
  },
  { title: 'Last Edited', align: 'end', key: 'lastedited' },
  { title: 'Created At', align: 'end', key: 'createdat' },
  { title: 'Use', align: 'end', key: 'link' }
]

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
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col>
          <div class="d-flex align-center">
            <h1>Classroom Templates</h1>
            <v-btn color="primary ml-10" prepend-icon="mdi-plus">Create Template</v-btn>
          </div>
          <v-data-table :headers="headers" :items="values" @click:row="handleRowClick">
            <template v-slot:[`item.link`]="{ item }">
              <router-link :to="`templates/${item.raw.id}`">edit</router-link>
            </template>
          </v-data-table>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
  <Footer></Footer>
</template>
