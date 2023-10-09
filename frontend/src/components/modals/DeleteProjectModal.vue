<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useCatalogStore } from '@/stores/CatalogStore'
import { ref } from 'vue'
import {useToast} from "vue-toastification";

const props = defineProps<{ projectId: number , projectTitle: string}>()
const showDialog = ref(false)
const toast = useToast()

const catalogStore = useCatalogStore()

async function deleteProject() {
  catalogStore.deleteProject(props.projectId).then(() => {
    toast.info("Project deleted")
    showDialog.value = false
  }).catch((e) => {
    toast.error(e.message)
  })
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>Delete Project</v-card-title>
      <v-card-text>
        <p>Are you sure you want to permanently delete "{{ projectTitle }}"</p>
      </v-card-text>
      <v-card-actions>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Delete" @click="deleteProject()"></PrimaryButton>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
