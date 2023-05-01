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
  <v-card max-width="1000" color="grey-lighten-4" style="cursor: grab">
    <v-container fluid>
      <v-row>
        <v-col md="6">
          <div><v-icon icon="mdi-drag" />{{ name }}</div>
          <v-btn
            v-if="!showInformation"
            color="primary"
            append-icon="mdi-chevron-down"
            @click="showInformation = true"
          >
            Show information
          </v-btn>
          <v-btn
            v-if="showInformation"
            color="primary"
            variant="outlined"
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
          <v-btn prepend-icon="mdi-plus" color="primary" variant="outlined">Add Task</v-btn>
        </v-col>
        <v-col md="6">
          <div>General Options</div>
          <v-switch label="Active" color="primary"></v-switch>
          <div>Description</div>
          <v-textarea placeholder="Description of this Project" rows="3"></v-textarea>
          <div class="ml-auto" style="width: fit-content">
            <v-btn color="error">Delete</v-btn>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>
