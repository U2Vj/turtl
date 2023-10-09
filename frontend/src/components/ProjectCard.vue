<script setup lang="ts">
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { useSortable } from '@vueuse/integrations/useSortable'
import { ref } from 'vue'
import DeleteProjectModal from "@/components/modals/DeleteProjectModal.vue";

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

const showDetails = ref(false)

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
        v-if="!showDetails"
        buttonName="Show more"
        @click="showDetails = true"
        appendIcon="mdi-chevron-down"
      ></TextButton>
      <TextButton
        v-if="showDetails"
        buttonName="Show less"
        @click="showDetails = false"
        appendIcon="mdi-chevron-up"
      ></TextButton>
    </v-card-actions>
    <v-card-text v-show="showDetails">
      Tasks
      <div :id="`taskWrapper${props.projectId}`">
        <div v-for="task in props.tasks" :key="task.id" style="cursor: grab">
          <router-link :to="{name: 'InstructorTask', params: { classroomId: props.classroomId, taskId: task.id }}">
            <v-icon icon="mdi-drag" />{{ task.title }}
          </router-link>
        </div>
      </div>
      <v-card-actions>
        <SecondaryButton buttonName="Add Task" prependIcon="mdi-plus"></SecondaryButton>
        <v-spacer></v-spacer>
        <ErrorButton buttonName="Delete Project">
          <delete-project-modal :project-id="props.projectId" :project-title="props.title"></delete-project-modal>
        </ErrorButton>
      </v-card-actions>
    </v-card-text>
  </v-card>
</template>
