<script setup lang="ts">
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import EnrollModal from '@/components/modals/EnrollModal.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import type { EnrollmentShort } from '@/stores/EnrollmentStore'
import { useEnrollmentStore } from '@/stores/EnrollmentStore'
import { useUserStore } from '@/stores/UserStore'
import type { Ref } from 'vue'
import { ref, toRef } from 'vue'
import { useToast } from 'vue-toastification'

const catalogStore = useCatalogStore()
const enrollmentStore = useEnrollmentStore()
const toast = useToast()
const breadcrumbItems: Ref<any[]> = ref([])
const userStore = useUserStore()
const search = ref('')

let classroomList = toRef(catalogStore, 'classroomList')

catalogStore.getClassroomList().catch((e) => toast.error(e.message))

const enrolledClassrooms: Ref<number[]> = ref([])
const myEnrollments: Ref<EnrollmentShort[]> = ref([])
enrollmentStore
  .getMyEnrollments()
  .then((enrollments) => {
    if (userStore.isStudent()) {
      breadcrumbItems.value = [
        {
          title: 'All Classrooms',
          disabled: true
        }
      ]
    } else {
      breadcrumbItems.value = [
        {
          title: 'My Enrollments',
          disabled: false,
          to: {
            name: 'StudentMyEnrollments'
          }
        },
        {
          title: 'All Classrooms',
          disabled: true
        }
      ]
    }
    enrollments.forEach((enrollment) => {
      enrolledClassrooms.value.push(enrollment.classroom.id)
    })
    myEnrollments.value = enrollments
  })
  .catch((e) => toast.error(e.message))

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
</script>
<template>
  <DefaultLayout v-if="classroomList">
    <template #heading>All Classrooms</template>
    <template #default>
      <v-row>
        <v-col>
          <v-breadcrumbs :items="breadcrumbItems" density="compact"></v-breadcrumbs>
        </v-col>
      </v-row>
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
          {
            title: 'Instructors',
            align: 'end',
            key: 'instructors',
            value: (item) => getInstructor(item.instructors)
          },
          { title: 'Enroll', align: 'end', key: 'link' }
        ]"
        :items="classroomList"
        :search="search"
      >
        <template #[`item.title`]="{ item }">
          {{ item.raw.title }}
          <small class="text-grey" v-if="enrolledClassrooms.includes(item.raw.id)">
            <em>(already enrolled)</em>
          </small>
        </template>
        <template #[`item.link`]="{ item }">
          <template v-if="enrolledClassrooms.includes(item.raw.id)">
            <TextButton
              :go-to="`/student/enrollments/${
                myEnrollments[enrolledClassrooms.indexOf(item.raw.id)].id
              }`"
            >
              Visit
            </TextButton>
          </template>
          <TextButton buttonName="Enroll" v-else>
            <EnrollModal :title="item.raw.title" :id="item.raw.id" />
          </TextButton>
        </template>
      </v-data-table>
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
