<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { ref, toRef } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps<{ classroomId: number }>()
const showDialog = ref(false)
const router = useRouter()

const catalogStore = useCatalogStore()

let classroom = toRef(catalogStore, 'classroom')
catalogStore.getClassroom(props.classroomId)

async function deleteClassroom() {
  const result = await catalogStore.deleteClassroom(props.classroomId)
  if (result) {
    await router.push({ name: 'InstructorClassroomList' })
  } else {
    console.error
  }
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Delete Classroom</v-card-title>
      <v-card-text>
        <p>Are you sure you want to permanently delete "{{ classroom?.title }}"</p>
      </v-card-text>
      <v-card-actions>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Delete" @click="deleteClassroom()"></PrimaryButton>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
