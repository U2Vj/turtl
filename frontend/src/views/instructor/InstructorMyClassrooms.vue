<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import CreateClassroomModal from '@/components/modals/CreateClassroomModal.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { useUserStore } from '@/stores/UserStore'
import dayjs from 'dayjs'
import type { Ref } from 'vue'
import { ref, toRef } from 'vue'
import { useToast } from 'vue-toastification'

const userStore = useUserStore()

const catalogStore = useCatalogStore()
const toast = useToast()

const breadcrumbItems: Ref<any[]> = ref([])

let classroomList = toRef(catalogStore, 'classroomList')

catalogStore
  .getMyClassroomList()
  .then(() => {
    breadcrumbItems.value = [
      {
        title: 'My Classrooms',
        disabled: true
      }
    ]
  })
  .catch((e: any) => toast.error(e.message))

function getInstructor(instructors: any[]) {
  return instructors
    .map((instructor: any) => {
      if (instructor.username !== null) {
        return instructor.username
      } else {
        return instructor.email
      }
    })
    .join(', ')
}

function formatReadableDate(date: string) {
  return dayjs(date).format('DD.MM.YYYY')
}
</script>

<template>
  <DefaultLayout v-if="classroomList" :breadcrumb-items="breadcrumbItems">
    <template #heading>My Classrooms</template>
    <template #postHeadingButton>
      <PrimaryButton button-name="Create"> <CreateClassroomModal /> </PrimaryButton>
    </template>
    <template #default>
      <v-row class="mt-1">
        <v-col
          v-for="classroom in classroomList"
          :key="classroom.id"
          cols="12"
          xs="12"
          sm="6"
          md="4"
        >
          <v-card
            :key="classroom.id"
            :title="classroom.title"
            :subtitle="getInstructor(classroom.instructors)"
            variant="elevated"
            class="elevation-4"
            color="cardColor"
          >
            <v-card-text> Created at {{ formatReadableDate(classroom.created_at) }} </v-card-text>
            <v-card-actions>
              <SecondaryButton
                buttonName="Edit Classroom"
                class="d-flex flex-fill elevation-2"
                :go-to="`/instructor/classrooms/${classroom.id}`"
              >
              </SecondaryButton>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col v-if="classroomList?.length === 0">
          <p>You do not manage any classrooms yet. Click above to create a new classroom.</p>
        </v-col>
      </v-row>
      <v-row v-if="userStore.isAdministrator()">
        <v-col>
          <p>
            As an administrator, you can also edit all classrooms, including classrooms you do not
            manage.
            <router-link to="/admin/classrooms/all">View All Classrooms</router-link>
          </p>
        </v-col>
      </v-row>
    </template>
  </DefaultLayout>
  <div v-else class="center-screen">
    <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
  </div>
</template>

<style scoped>
.center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
