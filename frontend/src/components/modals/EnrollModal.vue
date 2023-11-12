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

async function enroll(id: number) {
  try {
    const enrollment = await enrollmentStore.enroll(id)
    toast.success(`You have enrolled in the classroom ‘${props.title}’.`)
    await router.push({ name: 'StudentClassroom', params: { enrollmentId: enrollment.id }})
    showDialog.value = false
  } catch (e: any) {
    toast.error(e.message)
  }
}
</script>
<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Enroll</v-card-title>
      <v-card-text>
        <p>Do you want to enroll in the classroom &lsquo;{{ props.title }}&rsquo;?</p>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <TextButton buttonName="Cancel" @click="close"></TextButton>
        <PrimaryButton @click="enroll(props.id)">Enroll</PrimaryButton>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
