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
import type {Question, Task} from '@/stores/CatalogStore'
import {QuestionType, useCatalogStore} from '@/stores/CatalogStore'
import type {Ref} from 'vue'
import {ref} from 'vue'
import {useToast} from 'vue-toastification'

const props = defineProps<{
  classroomId: number
  taskId: number
}>()

const toast = useToast()
const catalogStore = useCatalogStore()

let task: Ref<Task | undefined> = ref(undefined)

const regexList = ref<{ regexPrompt: string; regex: string }[]>([])

const handleAddRegex = (data: any) => {
  const { regexPrompt: newRegexPrompt, regex: newRegex } = data
  regexList.value.push({ regexPrompt: newRegexPrompt, regex: newRegex })
}

const deleteRegex = (index: number) => {
  regexList.value.splice(index, 1)
}

const flagList = ref<{ flagPrompt: string; flag: string }[]>([])

const handleAddFlag = (data: any) => {
  const { flagPrompt: newFlagPrompt, flag: newFlag } = data
  flagList.value.push({ flagPrompt: newFlagPrompt, flag: newFlag })
}

const deleteFlag = (index: number) => {
  flagList.value.splice(index, 1)
}

const addQuestion = (question: Question) => {
  console.log(question)
  if(!task.value) return

  if(task.value.acceptance_criteria?.questions) {
    task.value.acceptance_criteria.questions.push(question)
  } else {
    task.value.acceptance_criteria.questions = [question]
  }
}

const updateQuestion = (question: Question, index: number) => {
  if(!task.value?.acceptance_criteria?.questions) return

  task.value.acceptance_criteria.questions[index] = question
}

const deleteQuestion = (question: Question) => {
  if(!task.value?.acceptance_criteria?.questions) return

  // get the index of the question that should be deleted
  const index = task.value.acceptance_criteria.questions.indexOf(question)
  task.value.acceptance_criteria.questions.splice(index, 1)
}

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
            <div v-for="(regexItem, index) in regexList" :key="index">
              <v-row>
                <v-col>
                  <v-textarea
                    label="RegEx Prompt"
                    clearable
                    variant="underlined"
                    base-color="primary"
                    color="primary"
                    v-model="regexItem.regexPrompt"
                  ></v-textarea>
                </v-col>
                <v-col>
                  <v-text-field
                    label="RegEx"
                    clearable
                    variant="underlined"
                    base-color="primary"
                    color="primary"
                    v-model="regexItem.regex"
                  ></v-text-field>
                  <ErrorButton
                    button-name="Delete"
                    button-type="button"
                    @click="deleteRegex(index)"
                  ></ErrorButton>
                </v-col>
              </v-row>
              <v-divider></v-divider><br />
            </div>
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
            <div v-for="(flagItem, index) in flagList" :key="index">
              <v-row>
                <v-col>
                  <v-textarea
                    label="Flag Prompt"
                    clearable
                    variant="underlined"
                    base-color="primary"
                    color="primary"
                    v-model="flagItem.flagPrompt"
                  ></v-textarea>
                </v-col>
                <v-col>
                  <v-text-field
                    label="Flag"
                    clearable
                    variant="underlined"
                    base-color="primary"
                    color="primary"
                    v-model="flagItem.flag"
                  ></v-text-field>
                  <ErrorButton
                    button-name="Delete"
                    button-type="button"
                    @click="deleteFlag(index)"
                  ></ErrorButton>
                </v-col>
              </v-row>
              <v-divider></v-divider><br />
            </div>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton button-name="Add Flag" button-type="button">
              <AddFlagModal @addFlag="handleAddFlag" />
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
            <v-table v-if="task.acceptance_criteria?.questions">
              <thead>
                <tr>
                  <th>Question</th>
                  <th>Question Type</th>
                  <th>No. of choices</th>
                  <th>Edit</th>
                  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(question, index) in task.acceptance_criteria.questions" :key="index">
                  <td>{{ question.question }}</td>
                  <td v-if="question.question_type === QuestionType.SingleChoice">Single Choice</td>
                  <td v-else>Multiple Choice</td>
                  <td>{{ question.choices.length }}</td>
                  <td>
                    <TextButton button-type="button">
                      <v-icon icon="mdi-pencil"></v-icon>&nbsp;Edit
                      <AddQuestionModal :current-question="question" @question-editing-completed="updateQuestion($event, index)">
                        <template v-slot:title>Edit Question</template>
                        <template v-slot:submitButtonText>Edit</template>
                      </AddQuestionModal>
                    </TextButton>
                  </td>
                  <td>
                    <v-btn icon="mdi-trash-can-outline" variant="text" @click="deleteQuestion(question)"></v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <p v-else>This Task does not contain any questions yet.</p><br>
            <SecondaryButton button-name="Add Question" button-type="button">
              <AddQuestionModal @question-editing-completed="addQuestion">
                <template v-slot:title>Add Question</template>
                <template v-slot:submitButtonText>Add</template>
              </AddQuestionModal>
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
