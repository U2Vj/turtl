<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { ref } from 'vue'
import {useToast} from "vue-toastification";
import type {Task} from "@/stores/CatalogStore";
import {useRouter} from "vue-router";

const props = defineProps<{ classroomId: number; task: Task }>()
const showDialog = ref(false)
const toast = useToast()
const router = useRouter()

const catalogStore = useCatalogStore()

async function deleteTask() {
  if(!props.task.id) return
  catalogStore.deleteTask(props.task.id).then(() => {
    toast.info("Task deleted")
    showDialog.value = false
    router.push({name: "InstructorClassroom", params: { classroomId: props.classroomId }})
  }).catch((e) => {
    toast.error(e.message)
  })
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Delete Task</v-card-title>
      <v-card-text>
        <p>Are you sure you want to permanently delete "{{ task.title }}"?</p>
      </v-card-text>
      <v-card-actions>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Delete" @click="deleteTask()"></PrimaryButton>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
