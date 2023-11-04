<script setup lang="ts">
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import JoinClassroomModal from '@/components/modals/JoinClassroomModal.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { ref, toRef } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const router = useRouter()

const catalogStore = useCatalogStore()
const toast = useToast()

const search = ref('')

let classroomList = toRef(catalogStore, 'classroomList')

catalogStore.getClassroomList().catch((e) => toast.error(e.message))
</script>

<template>
  <DefaultLayout>
    <template #heading>All Classrooms</template>
    <template #default>
      <v-row>
        <v-col cols="8">
          <v-text-field
            clearable
            label="Search title of Classroom"
            v-model="search"
            append-inner-icon="mdi-magnify"
            variant="underlined"
            base-color="primary"
            color="primary"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-data-table
        :headers="[
          {
            title: 'Title',
            align: 'start',
            sortable: true,
            key: 'title'
          },
          { title: 'Join', align: 'end', key: 'link' }
        ]"
        :items="classroomList"
        :search="search"
      >
        <template #[`item.link`]="{ item }">
          <TextButton buttonName="Join">
            <JoinClassroomModal :title="item.raw.title" />
          </TextButton>
        </template>
      </v-data-table>
    </template>
  </DefaultLayout>
</template>
