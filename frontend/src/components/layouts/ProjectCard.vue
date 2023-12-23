<script setup lang="ts">
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import AddTaskModal from '@/components/modals/AddTaskModal.vue'
import DeleteProjectModal from '@/components/modals/DeleteProjectModal.vue'
import type { Task } from '@/stores/CatalogStore'
import { useCatalogStore } from '@/stores/CatalogStore'
import { ref, toRef } from 'vue'
import { useToast } from 'vue-toastification'

const catalogStore = useCatalogStore()
const toast = useToast()
let classroom = toRef(catalogStore, 'classroom')

const props = defineProps<{
  classroomId: number
  projectId: number
  projectTitle: string
  tasks: Task[]
}>()

const showDetails = ref(false)
const projectTitle = ref(props.projectTitle)

const hasProjectTitleChanged = ref(false)
const projectTitleJustSaved = ref(false)

function onProjectTitleInputChange() {
  hasProjectTitleChanged.value = projectTitle.value !== props.projectTitle
  if (hasProjectTitleChanged.value) {
    projectTitleJustSaved.value = false
  }
}

function editProjectTitle(newTitle: string, projectId: number) {
  if (!classroom.value) {
    return
  }

  const updatedClassroom = { ...classroom.value }

  const project = updatedClassroom.projects.find((p) => p.id === projectId)

  if (project) {
    project.title = newTitle

    catalogStore
      .updateClassroom(classroom.value.id, updatedClassroom)
      .then(() => {
        toast.success('Project title changed')
        projectTitleJustSaved.value = true
      })
      .catch((e) => {
        toast.error(e.message)
      })
  }
}
</script>

<template>
  <v-card variant="flat" color="cardColor" class="elevation-4">
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
      <v-text-field
        label="Edit Title"
        clearable
        variant="underlined"
        base-color="primary"
        color="primary"
        v-model="projectTitle"
        @input="onProjectTitleInputChange"
      ></v-text-field>
      <PrimaryButton
        button-name="Save Title"
        :disabled="!hasProjectTitleChanged || projectTitleJustSaved"
        @click="editProjectTitle(projectTitle, projectId)"
      ></PrimaryButton>
      <br /><br />
      <v-divider></v-divider>
      <br />
      Tasks
      <div>
        <div v-for="task in props.tasks" :key="task.id">
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
      <br />
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
