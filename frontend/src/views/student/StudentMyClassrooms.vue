<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import SecundaryButton from '@/components/buttons/SecondaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import { useEnrollmentStore } from '@/stores/EnrollmentStore'
import dayjs from 'dayjs'
import { ref, toRef } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const progress = 33

const router = useRouter()

const enrollmentStore = useEnrollmentStore()
const toast = useToast()

const search = ref('')

let myEnrollments = toRef(enrollmentStore, 'myEnrollments')

enrollmentStore.getMyEnrollments().catch((e: any) => toast.error(e.message))

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
  <DefaultLayout>
    <template #heading>My Classrooms</template>
    <template #postHeadingButton>
      <PrimaryButton buttonName="Join Classroom" goTo="/student/classrooms/all"> </PrimaryButton>
    </template>
    <template #default>
      <v-row>
        <v-col v-for="item in myEnrollments" :key="item.id" cols="12" xs="12" sm="6" md="4">
          <v-card
            :key="item.id"
            :title="item.classroom.title"
            :subtitle="getInstructor(item.classroom.instructors)"
            variant="elevated"
            class="elevation-4"
            color="cardColor"
          >
            <v-card-text>
              Eingeschrieben am {{ formatReadableDate(item.date_enrolled) }}
            </v-card-text>
            <v-card-text>
              <v-progress-linear
                id="probar"
                color="progress"
                :height="25"
                :model-value="progress"
                rounded
                rounded-bar
                bg-color="#ffffff"
                bg-opacity="1"
              >
                <template #default>
                  <strong>{{ Math.ceil(progress) }}%</strong>
                </template>
              </v-progress-linear>
            </v-card-text>
            <v-card-actions>
              <SecundaryButton buttonName="Visit Classroom" class="d-flex flex-fill elevation-2">
              </SecundaryButton>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </DefaultLayout>
</template>

<style scoped></style>
