<script setup lang="ts">
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import AddTaskModal from '@/components/modals/AddTaskModal.vue'
import DeleteProjectModal from '@/components/modals/DeleteProjectModal.vue'
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'update:task', id: number, event: any): void
}>()

// TODO: change tasks type

const props = defineProps<{
  classroomId: number
  projectId: number
  projectTitle: string
  tasks: { id: number; title: string }[]
}>()

const showDetails = ref(false)
</script>

<template>
  <v-card variant="flat" color="cardColor" class="elevation-4" style="cursor: grab">
    <v-card-title>{{ projectTitle }} </v-card-title>
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
      <div>
        <div v-for="task in props.tasks" :key="task.id" style="cursor: grab">
          <router-link
            :to="{
              name: 'InstructorTask',
              params: { classroomId: props.classroomId, taskId: task.id }
            }"
          >
            {{ task.title }}
          </router-link>
        </div>
      </div>
      <small v-if="!props.tasks.length">This project does not contain any tasks yet.</small>
      <v-card-actions>
        <SecondaryButton buttonName="Add Task" prependIcon="mdi-plus">
          <AddTaskModal
            :classroom-id="props.classroomId"
            :project-id="props.projectId"
          ></AddTaskModal>
        </SecondaryButton>
        <v-spacer></v-spacer>
        <ErrorButton buttonName="Delete Project">
          <delete-project-modal
            :project-id="props.projectId"
            :project-title="props.projectTitle"
          ></delete-project-modal>
        </ErrorButton>
      </v-card-actions>
    </v-card-text>
  </v-card>
</template>
