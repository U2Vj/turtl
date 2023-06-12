<script setup lang="ts">
import { ref } from 'vue'
import TurtlHeader from '@/components/TurtlHeader.vue'
import Footer from '@/components/Footer.vue'
import { watch } from 'vue'

const classroomName = ref('')
const selected = ref<any[]>([])

const search = ref('')

function createClassroom() {
  // TODO: Button Classroom. Selected Row Object in value: selected
}

const headers = [
  { title: 'Name', key: 'name' },
  { title: 'Created On', key: 'created_on' },
  { title: 'Created By', key: 'created_by' }
]
const classTemplates = [
  {
    name: 'Test Networks',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Test Networks',
    created_on: '01.03.2023',
    created_by: 'Franz Mustermann'
  },
  {
    name: 'Computer Versuch',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Safe',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Sicherheit',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Labor Networks',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Computer Programm',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Meister Teil',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Birnen Kompott',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Apfelmouse',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Advanced Software Engineering',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Data Science',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Digital Story',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Theo Inf',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Mathe',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Physik',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  },
  {
    name: 'Algorithmen',
    created_on: '01.03.2023',
    created_by: 'Max Mustermann'
  }
]

watch(selected, (newSelected) => {
  search.value = newSelected[0] ? newSelected[0].name : ''
})
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col>
          <h1>Create Classroom</h1>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="5">
          <v-text-field
            clearable
            label="Type in Classroom Name"
            v-model="classroomName"
            variant="underlined"
            base-color="primary"
            color="primary"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="5">
          <v-text-field
            clearable
            label="Search Classroom Template"
            v-model="search"
            append-inner-icon="mdi-magnify"
            variant="underlined"
            base-color="primary"
            color="primary"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="10">
          <v-data-table
            :headers="headers"
            :items="classTemplates"
            :search="search"
            v-model="selected"
            item-value="classTemplates"
            show-select
          ></v-data-table>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn variant="tonal" color="primary" class="elevation-2" @click="createClassroom">Create Classroom</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
  <Footer></Footer>
</template>

<style>
.v-icon {
  color: #333399 !important;
}
</style>
