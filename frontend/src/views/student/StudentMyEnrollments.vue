<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import SecundaryButton from '@/components/buttons/SecondaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import type { EnrollmentShort } from '@/stores/EnrollmentStore'
import { useEnrollmentStore } from '@/stores/EnrollmentStore'
import dayjs from 'dayjs'
import type { Ref } from 'vue'
import { ref, toRef } from 'vue'
import { useToast } from 'vue-toastification'

const enrollmentStore = useEnrollmentStore()
const toast = useToast()
const breadcrumbItems: Ref<any[]> = ref([])

let myEnrollments: Ref<EnrollmentShort[] | undefined> = toRef(enrollmentStore, 'myEnrollments')

enrollmentStore
  .getMyEnrollments()
  .then(() => {
    breadcrumbItems.value = [
      {
        title: 'My Enrollments',
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
  <DefaultLayout v-if="myEnrollments">
    <template #heading>My Enrollments</template>
    <template #postHeadingButton>
      <PrimaryButton go-to="/student/classrooms/all">Enroll</PrimaryButton>
    </template>
    <template #default>
      <v-row>
        <v-col>
          <v-breadcrumbs :items="breadcrumbItems" density="compact"></v-breadcrumbs>
        </v-col>
      </v-row>
      <v-row class="mt-1">
        <v-col
          v-for="enrollment in myEnrollments"
          :key="enrollment.id"
          cols="12"
          xs="12"
          sm="6"
          md="4"
        >
          <v-card
            :key="enrollment.id"
            :title="enrollment.classroom.title"
            :subtitle="getInstructor(enrollment.classroom.instructors)"
            variant="elevated"
            class="elevation-4"
            color="cardColor"
          >
            <v-card-text>
              Enrolled on {{ formatReadableDate(enrollment.date_enrolled) }}
            </v-card-text>
            <v-card-text>
              <v-progress-linear
                id="probar"
                color="progress"
                :height="25"
                :model-value="enrollment.progress"
                rounded
                rounded-bar
                bg-color="#ffffff"
                bg-opacity="1"
              >
                <template #default>
                  <strong>{{ enrollment.progress }}&percnt;</strong>
                </template>
              </v-progress-linear>
            </v-card-text>
            <v-card-actions>
              <SecundaryButton
                buttonName="Visit Classroom"
                class="d-flex flex-fill elevation-2"
                :go-to="`/student/enrollments/${enrollment.id}`"
              >
              </SecundaryButton>
            </v-card-actions>
          </v-card>
        </v-col>
        <v-col v-if="myEnrollments?.length === 0">
          <p>You have not enrolled in any classrooms yet.</p>
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
