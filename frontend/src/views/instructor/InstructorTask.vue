<script setup lang="ts">
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import AddFlagModal from '@/components/modals/AddFlagModal.vue'
import AddQuestionModal from '@/components/modals/AddQuestionModal.vue'
import AddRegexModal from '@/components/modals/AddRegexModal.vue'
import AddVirtualizationModal from '@/components/modals/AddVirtualizationModal.vue'
import DeleteTaskModal from '@/components/modals/DeleteTaskModal.vue'
import type { Task } from '@/stores/CatalogStore'
import { useCatalogStore } from '@/stores/CatalogStore'
import type { Ref } from 'vue'
import { ref } from 'vue'
import { useToast } from 'vue-toastification'

const props = defineProps<{
  classroomId: number
  taskId: number
  regexPrompt: string
  regex: string
}>()

const regexPrompt = ref('')
const regex = ref('')

const handleAddRegex = (data: any) => {
  const { regexPrompt: newRegexPrompt, regex: newRegex } = data
  regexPrompt.value = newRegexPrompt
  regex.value = newRegex
}

const toast = useToast()
const catalogStore = useCatalogStore()

let task: Ref<Task | undefined> = ref(undefined)

try {
  catalogStore
    .getClassroom(props.classroomId)
    .then(() => {
      task.value = catalogStore.getTask(props.taskId)
    })
    .catch((e) => {
      toast.error(e.message)
    })
} catch (e: any) {
  toast.error(e.message)
}
</script>
<template>
  <DefaultLayout v-if="task">
    <template #heading>{{ task.title }}</template>
    <template #postHeadingButton>
      <ErrorButton button-name="Delete">
        <DeleteTaskModal :task="task" :classroom-id="classroomId"></DeleteTaskModal>
      </ErrorButton>
    </template>
    <template #default>
      <v-form>
        <v-text-field
          label="Edit Title"
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="task.title"
        ></v-text-field>
        <v-textarea
          label="Task Description"
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="task.description"
        ></v-textarea>
        <v-row>
          <v-col>
            <v-select
              label="Select Difficulty Level"
              :items="['Beginner', 'Intermediate', 'Advanced']"
              variant="underlined"
              base-color="primary"
              color="primary"
              v-model="task.difficulty"
            ></v-select>
          </v-col>
          <v-col>
            <v-select
              label="Select Task Type"
              :items="['Neural', 'Attack', 'Defense']"
              variant="underlined"
              base-color="primary"
              color="primary"
              v-model="task.task_type"
            ></v-select>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <h2>Acceptance Criteria</h2>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <h3>RegEx</h3>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <p>Prompt: {{ regexPrompt }}</p>
            <p>Regex: {{ regex }}</p>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton button-name="Add RegEx" button-type="button">
              <AddRegexModal @addRegex="handleAddRegex" />
            </SecondaryButton>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <h3>Flag</h3>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton button-name="Add Flag" button-type="button">
              <AddFlagModal :task="task" />
            </SecondaryButton>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <h3>Quiz</h3>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton button-name="Add Question" button-type="button">
              <AddQuestionModal :task="task" />
            </SecondaryButton>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <h2>Virtualization</h2>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton button-name="Add Virtualization" button-type="button">
              <AddVirtualizationModal :classroom-id="props.classroomId" :task-id="props.taskId">
              </AddVirtualizationModal>
            </SecondaryButton>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <!-- TODO: make this a loop because a task can contain multiple virtualizations -->
            <v-card
              v-for="virtualization in task.virtualizations"
              :key="virtualization.id"
              variant="flat"
              color="cardColor"
              class="elevation-4"
            >
              <v-card-text>
                <v-text-field
                  label="Name of Virtualization"
                  clearable
                  variant="underlined"
                  base-color="primary"
                  color="primary"
                  v-model="virtualization.name"
                ></v-text-field>
                <v-select
                  label="Role"
                  :items="['UserShell', 'IP']"
                  variant="underlined"
                  base-color="primary"
                  color="primary"
                  v-model="virtualization.role"
                ></v-select>
                <v-file-input
                  clearable
                  label="Dockerfile"
                  variant="underlined"
                  base-color="primary"
                  color="primary"
                ></v-file-input>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        <div class="d-flex mt-5 mb-2 align-center justify-space-between">
          <TextButton
            button-name="Close"
            :go-to="`/instructor/classrooms/${props.classroomId}`"
          ></TextButton>
          <PrimaryButton button-name="Save" button-type="submit"></PrimaryButton>
        </div>
      </v-form>
    </template>
  </DefaultLayout>
</template>
