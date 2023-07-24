<script setup lang="ts">
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import SecundaryButton from '@/components/buttons/SecondaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useSortable } from '@vueuse/integrations/useSortable'
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'update:task_template', id: string, event: any): void
}>()

const props = defineProps<{
  templateId: string
  projectId: string
  title: string
  taskTemplates: { id: string; title: string }[]
}>()

const showInformation = ref(false)

useSortable(`#taskWrapper${props.projectId}`, props.taskTemplates, {
  animation: 150,
  onUpdate: (event: any) => {
    emit('update:task_template', props.projectId, event)
  }
})
</script>

<template>
  <v-card variant="flat" color="cardColor" class="elevation-4" style="cursor: grab">
    <v-card-title> <v-icon icon="mdi-drag" />{{ title }} </v-card-title>
    <v-card-actions>
      <TextButton
        v-if="!showInformation"
        buttonName="Show information"
        @click="showInformation = true"
        appendIcon="mdi-chevron-down"
      ></TextButton>
      <TextButton
        v-if="showInformation"
        buttonName="Hide information"
        @click="showInformation = false"
        appendIcon="mdi-chevron-up"
      ></TextButton>
    </v-card-actions>
    <v-card-text v-show="showInformation">
      Tasks
      <div :id="`taskWrapper${props.projectId}`">
        <div v-for="task in props.taskTemplates" :key="task.id" style="cursor: grab">
          <a :href="`/admin/templates/${props.templateId}/tasks/${task.id}`">
            <v-icon icon="mdi-drag" />{{ task.title }}
          </a>
        </div>
      </div>
      <v-card-actions>
        <SecundaryButton buttonName="Add Task" prependIcon="mdi-plus"> </SecundaryButton>
        <v-spacer></v-spacer>
        <ErrorButton buttonName="Delete Template"></ErrorButton>
      </v-card-actions>
    </v-card-text>
  </v-card>
</template>
