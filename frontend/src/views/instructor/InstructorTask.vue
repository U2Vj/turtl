<script setup lang="ts">
import ErrorButton from '@/components/buttons/ErrorButton.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import SecondaryButton from '@/components/buttons/SecondaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import AddQuestionModal from '@/components/modals/AddQuestionModal.vue'
import type { Task } from '@/stores/CatalogStore'
import { useCatalogStore } from '@/stores/CatalogStore'
import type { Ref } from 'vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const props = defineProps<{ classroomId: number; taskId: number }>()

const router = useRouter()
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
      <ErrorButton buttonName="Delete"></ErrorButton>
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
            <h2>Questions</h2>
          </v-col>
        </v-row>
        <v-row v-if="task.acceptance_criteria.acceptance_criteria_questionnaire">
          <v-col
            cols="12"
            v-for="question in task.acceptance_criteria.acceptance_criteria_questionnaire"
            :key="question.id"
          >
            <v-form>
              <v-card variant="flat" color="cardColor" class="elevation-4">
                <v-card-text>
                  <v-text-field
                    label="Edit Question"
                    clearable
                    variant="underlined"
                    base-color="primary"
                    color="primary"
                    v-model="question.title"
                  ></v-text-field>
                  <v-row v-for="choice in question.choices" :key="choice.answer">
                    <v-col>
                      <v-text-field
                        label="Edit Answer"
                        clearable
                        variant="underlined"
                        base-color="primary"
                        color="primary"
                        v-model="choice.answer"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="3">
                      <!-- TODO: Make this a checkbox -->
                      <v-select
                        label="Correct"
                        :items="[
                          { title: 'True', value: true },
                          { title: 'False', value: false }
                        ]"
                        variant="underlined"
                        base-color="primary"
                        color="primary"
                        v-model="choice.is_correct"
                      ></v-select>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-form>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton buttonName="Add Question">
              <AddQuestionModal />
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
            <v-form>
              <!-- TODO: make this a loop because a task can contain multiple virtualizations -->
              <!--<v-card
                :key="task.virtualization.id"
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
                    v-model="task.virtualization.name"
                  ></v-text-field>
                  <v-select
                    label="Role"
                    :items="['UserShell', 'IP']"
                    variant="underlined"
                    base-color="primary"
                    color="primary"
                    v-model="task.virtualization.role"
                  ></v-select>
                  <v-file-input
                    clearable
                    label="Dockerfile"
                    variant="underlined"
                    base-color="primary"
                    color="primary"
                  ></v-file-input>
                </v-card-text>
              </v-card>-->
            </v-form>
          </v-col>
        </v-row>
        <div class="d-flex mt-5 mb-2 align-center justify-space-between">
          <TextButton
            buttonName="Close"
            :go-to="`/instructor/classrooms/${props.classroomId}`"
          ></TextButton>
          <PrimaryButton buttonName="Save"></PrimaryButton>
        </div>
      </v-form>
    </template>
  </DefaultLayout>
</template>
