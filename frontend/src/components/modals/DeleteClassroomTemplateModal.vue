<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { ref, toRef } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps<{ templateId: string }>()
const showDialog = ref(false)
const router = useRouter()

const templateStore = useTemplateStore()

let templateData = toRef(templateStore, 'classroomTemplate')
templateStore.fetchTemplate(props.templateId)

async function deleteTemplate() {
  const result = await templateStore.deleteClassroomTemplate(props.templateId)
  if (result) {
    router.push('/admin/templates')
  } else {
    console.error
  }
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title
        >Are you sure you want to permanently delete "{{ templateData?.title }}"</v-card-title
      >
      <v-card-text>
        <TextButton buttonName="Close" @click="showDialog = false"></TextButton>
        <PrimaryButton buttonName="Delete" @click="deleteTemplate()"> </PrimaryButton>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
