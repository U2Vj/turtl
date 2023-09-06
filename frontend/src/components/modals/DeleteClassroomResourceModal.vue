<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { ref } from 'vue'

const props = defineProps<{ resourceId: string }>()
const showDialog = ref(false)

const templateStore = useTemplateStore()

// let templateData = toRef(templateStore, 'classroomTemplate')
templateStore.fetchTemplate(props.resourceId)

async function deleteTemplate() {
  //   const result = await templateStore.deleteClassroomTemplate(props.resourceId)
  //
  // TODO: Delete Resource
  //   if (result) {
  //     showDialog.value = false
  //   } else {
  //     console.error
  //   }
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="60%">
    <v-card>
      <v-card-title>Delete Rsource </v-card-title>
      <v-card-text>
        <p>Are you sure you want to permanently delete the Resource "RESOURCE NAME EINFÜGEN"</p>
      </v-card-text>
      <v-card-actions>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Delete" @click="deleteTemplate()"> </PrimaryButton>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
