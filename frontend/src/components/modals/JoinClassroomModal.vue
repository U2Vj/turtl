<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useEnrollmentStore } from '@/stores/EnrollmentStore'
import { ref, toRef } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
const showDialog = ref(false)

function close() {
  showDialog.value = false
}

const props = defineProps<{
  id: number
  title: string
}>()

const router = useRouter()

const enrollmentStore = useEnrollmentStore()
const toast = useToast()

let myEnrollments = toRef(enrollmentStore, 'myEnrollments')

enrollmentStore.getMyEnrollments().catch((e: any) => toast.error(e.message))

async function join(id: number) {
  try {
    const response = await enrollmentStore.enroll(id)
    await router.push({ name: 'StudentMyClassrooms' })
    showDialog.value = false
  } catch (e: any) {
    toast.error(e.message)
  }
}
</script>
<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title> Join the classroom: {{ props.title }} </v-card-title>
      <v-card-actions>
        <v-spacer></v-spacer>
        <TextButton buttonName="Cancel" @click="close"></TextButton>
        <PrimaryButton buttonName="Join Classroom" @click="join(props.id)"> </PrimaryButton>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
