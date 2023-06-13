<script setup lang="ts">
import { ref } from 'vue'
import { useSortable } from '@vueuse/integrations/useSortable'

const emit = defineEmits<{
  (e: 'update:tasks', projectId: string, event: any): void
}>()

const props = defineProps<{
  projectId: string
  name: string
  tasks: { id: string; title: string }[]
}>()

const showInformation = ref(false)

useSortable(`#taskWrapper${props.projectId}`, props.tasks, {
  animation: 150,
  onUpdate: (event: any) => {
    emit('update:tasks', props.projectId, event)
  }
})
</script>

<template>
  <v-card max-width="1000" variant="flat" color="cardColor" class="elevation-4" style="cursor: grab">
      <v-card-title>
              <v-icon icon="mdi-drag" />{{ name }}
      </v-card-title>
      <v-card-actions>
          <v-btn
            v-if="!showInformation"
            append-icon="mdi-chevron-down"
            @click="showInformation = true"
            variant="text" color="primary"
          >
            Show information
          </v-btn>
          <v-btn
            v-if="showInformation"
            variant="text" color="primary"
            append-icon="mdi-chevron-down"
            @click="showInformation = false"
          >
            Hide Information
          </v-btn>
          </v-card-actions>
      <v-card-text v-show="showInformation">
          Tasks
          <div :id="`taskWrapper${props.projectId}`">
            <div v-for="task in props.tasks" :key="task.id" style="cursor: grab">
              <v-icon icon="mdi-drag" />{{ task.title }}
            </div>
          </div>
      <v-card-actions>
          <v-btn prepend-icon="mdi-plus" variant="tonal" color="primary" class="elevation-2">Add Task</v-btn>
          <v-spacer></v-spacer>
            <v-btn variant="tonal" color="error" class="elevation-2">Delete Template</v-btn>
      </v-card-actions>
      </v-card-text>

  </v-card>
</template>
