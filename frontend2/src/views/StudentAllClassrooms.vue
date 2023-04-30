<script setup lang="ts">
import { ref } from 'vue'
import TurtlHeader from '@/components/TurtlHeader.vue'

const search = ref('')
const headers = [
  { title: 'Name of Classroom', key: 'name_classroom' },
  { title: 'Manager', key: 'manager_name' },
]

const classrooms = [
    {
        name_classroom: 'Test Networks',
        manager_name: 'John Doe'
    },
    {
        name_classroom: 'Computer Networks',
        manager_name: 'Tom Doe'
    },
    {
        name_classroom: 'Secure Networks',
        manager_name: 'Finn Doe'
    }
]

function joinClassroom(item:any) {
    console.log(item)
}
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
        <v-row>
            <v-col>
                <h1>All Classrooms</h1>
            </v-col>
        </v-row>
        <v-row>
        <v-col>
          <p>Search:</p>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="5">
          <v-text-field
          clearable
          label="Search Name of Classroom"
          v-model="search"
          append-inner-icon="mdi-magnify"
          variant="solo"
        ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
            <v-data-table
                :headers="headers"
                :items="classrooms"
                :search="search"
                item-value="classTemplates"
            >
            <template v-slot:item.actions="{ item }">
                <v-btn
                    size="small"
                    @click="joinClassroom(item.raw)"
                >Join classroom</v-btn>
                </template>
                <template v-slot:no-data>
                <p>No data</p>
                </template>
            </v-data-table>
        </v-col>
      </v-row>
    </v-container>
    </v-main>
</template>

<style>
</style>