<script setup lang="ts">
import Shell from '@/components/ShellView.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import type {TaskStudent} from '@/stores/EnrollmentStore'
import type {Ref} from 'vue'
import {ref} from 'vue'
import {useEnrollmentStore} from '@/stores/EnrollmentStore'
import {useToast} from 'vue-toastification'

const props = defineProps<{ enrollmentId: number, taskId: number }>()

const task: Ref<TaskStudent | undefined> = ref()
const enrollmentStore = useEnrollmentStore()
const toast = useToast()

enrollmentStore.getEnrollment(props.enrollmentId).then(() => {
  task.value = enrollmentStore.getTask(props.taskId)
}).catch((e) => toast.error(e.message))

</script>

<template>
  <DefaultLayout v-if="task">
    <template #heading>{{ task.title }}</template>
    <template #default>
      <v-row>
        <v-col cols="12">
          {{ task.description }}
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-textarea
            label="Enter Your Code here"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
          ></v-textarea>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <Shell />
        </v-col>
      </v-row>
      <v-row class="mt-5">
        <v-col>
          <PrimaryButton buttonName="Verify Task" />
        </v-col>
      </v-row>
    </template>
  </DefaultLayout>
</template>
