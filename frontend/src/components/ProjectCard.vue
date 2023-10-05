<script setup lang="ts">
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useSortable } from '@vueuse/integrations/useSortable'
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'update:task', id: number, event: any): void
}>()

// TODO: change tasks type

const props = defineProps<{
  classroomId: number
  projectId: number
  title: string
  tasks: { id: number; title: string }[]
}>()

const showTasks = ref(false)

useSortable(`#taskWrapper${props.projectId}`, props.tasks, {
  animation: 150,
  onUpdate: (event: any) => {
    emit('update:task', props.projectId, event)
  }
})
</script>

<template>
  <v-card variant="flat" color="cardColor" class="elevation-4" style="cursor: grab">
    <v-card-title> <v-icon icon="mdi-drag" />{{ title }} </v-card-title>
    <v-card-actions>
      <TextButton
        v-if="!showTasks"
        buttonName="Show tasks"
        @click="showTasks = true"
        appendIcon="mdi-chevron-down"
      ></TextButton>
      <TextButton
        v-if="showTasks"
        buttonName="Hide tasks"
        @click="showTasks = false"
        appendIcon="mdi-chevron-up"
      ></TextButton>
    </v-card-actions>
    <v-card-text v-show="showTasks">
      Tasks
      <div :id="`taskWrapper${props.projectId}`">
        <div v-for="task in props.tasks" :key="task.id" style="cursor: grab">
          <a :href="`/instructor/classrooms/${props.classroomId}/tasks/${task.id}`">
            <v-icon icon="mdi-drag" />{{ task.title }}
          </a>
        </div>
      </div>
      <v-card-actions>
        <SecondaryButton buttonName="Add Task" prependIcon="mdi-plus"> </SecondaryButton>
        <v-spacer></v-spacer>
        <ErrorButton buttonName="Delete Project"></ErrorButton>
      </v-card-actions>
    </v-card-text>
  </v-card>
</template>
