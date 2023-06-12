<script setup lang="ts">
import { ref } from 'vue'
import { useSortable } from '@vueuse/integrations/useSortable'

const emit = defineEmits<{
  (e: 'update:tasks', projectId: string, event: any): void
}>()

const props = defineProps<{
  projectId: string
  name: string
  tasks: { id: string; name: string }[]
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
    <v-container fluid>
      <v-row>
        <v-col md="6">
          <div><v-icon icon="mdi-drag" />{{ name }}</div>
          <v-btn
            v-if="!showInformation"
            append-icon="mdi-chevron-down"
            @click="showInformation = true"
            variant="tonal" color="primary" class="elevation-2"
          >
            Show information
          </v-btn>
          <v-btn
            v-if="showInformation"
            variant="tonal" color="primary" class="elevation-2"
            append-icon="mdi-chevron-down"
            @click="showInformation = false"
          >
            Hide Information
          </v-btn>
        </v-col>
      </v-row>
      <v-row v-show="showInformation">
        <v-col>
          <div>Tasks</div>
          <div :id="`taskWrapper${props.projectId}`">
            <div v-for="task in props.tasks" :key="task.id" style="cursor: grab">
              <v-icon icon="mdi-drag" />{{ task.name }}
            </div>
          </div>
          <v-btn prepend-icon="mdi-plus" variant="tonal" color="primary" class="elevation-2">Add Task</v-btn>
        </v-col>
        <v-col md="6">
          <div class="ml-auto" style="width: fit-content">
            <v-btn variant="tonal" color="error" class="elevation-2">Delete</v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>
