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
import type {Flag, Question, RegEx, Task} from '@/stores/CatalogStore'
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

const addRegEx = (regex: RegEx) => {
  if(!task.value) return

  if(task.value.acceptance_criteria?.regexes) {
    task.value.acceptance_criteria.regexes.push(regex)
  } else {
    task.value.acceptance_criteria.regexes = [regex]
  }
}

// TODO: This is prone to errors and there is probably a way more elegant way to solve not having reactive props
const updateRegEx = (regex: RegEx, index: number) => {
  // To load the initial values in the modal correctly, we first have to remove the RegEx and then re-add it again
  deleteRegEx(index)
  // Re-add it after 2ms
  setTimeout(() => {
    if(!task.value?.acceptance_criteria?.regexes) return
    task.value.acceptance_criteria.regexes.splice(index, 0, regex)
  }, 2)

}

const deleteRegEx = (index: number) => {
  if(!task.value?.acceptance_criteria?.regexes) return

  task.value.acceptance_criteria.regexes.splice(index, 1)
}

const addFlag = (flag: Flag) => {
  if(!task.value) return

  if(task.value.acceptance_criteria?.flags) {
    task.value.acceptance_criteria.flags.push(flag)
  } else {
    task.value.acceptance_criteria.flags = [flag]
  }
}

const updateFlag = (flag: Flag, index: number) => {
  deleteFlag(index)
  setTimeout(() => {
    if(!task.value?.acceptance_criteria?.flags) return
    task.value.acceptance_criteria.flags.splice(index, 0, flag)
  }, 2)

}

const deleteFlag = (index: number) => {
  if(!task.value?.acceptance_criteria?.flags) return

  task.value.acceptance_criteria.flags.splice(index, 1)
}

const addQuestion = (question: Question) => {
  if(!task.value) return

  if(task.value.acceptance_criteria?.questions) {
    task.value.acceptance_criteria.questions.push(question)
  } else {
    task.value.acceptance_criteria.questions = [question]
  }
}

const updateQuestion = (question: Question, index: number) => {
  deleteQuestion(index)
  setTimeout(() => {
    if(!task.value?.acceptance_criteria?.questions) return
    task.value.acceptance_criteria.questions.splice(index, 0, question)
  }, 2)
}

const deleteQuestion = (index: number) => {
  if(!task.value?.acceptance_criteria?.questions) return

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
            <v-table v-if="task.acceptance_criteria?.regexes">
              <thead>
                <tr>
                  <th>Prompt</th>
                  <th>RegEx Pattern</th>
                  <th>Edit</th>
                  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(regEx, index) in task.acceptance_criteria.regexes" :key="index">
                  <td>{{ regEx.prompt }}</td>
                  <td>{{ regEx.pattern }}</td>
                  <td>
                    <TextButton button-type="button">
                      <v-icon icon="mdi-pencil"></v-icon>&nbsp;Edit
                      <AddRegexModal :current-regex="regEx" @reg-ex-editing-completed="updateRegEx($event, index)">
                        <template v-slot:title>Edit RegEx</template>
                        <template v-slot:submitButtonText>Edit</template>
                      </AddRegexModal>
                    </TextButton>
                  </td>
                  <td><v-btn icon="mdi-trash-can-outline" variant="text" @click="deleteRegEx(index)"></v-btn></td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton button-name="Add RegEx" button-type="button">
              <AddRegexModal @reg-ex-editing-completed="addRegEx">
                <template v-slot:title>Add RegEx</template>
                <template v-slot:submitButtonText>Add</template>
              </AddRegexModal>
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
            <v-table v-if="task.acceptance_criteria?.flags">
              <thead>
                <tr>
                  <th>Prompt</th>
                  <th>Flag Value</th>
                  <th>Edit</th>
                  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(flag, index) in task.acceptance_criteria.flags" :key="index">
                  <td>{{ flag.prompt }}</td>
                  <td>{{ flag.value }}</td>
                  <td>
                    <TextButton button-type="button">
                      <v-icon icon="mdi-pencil"></v-icon>&nbsp;Edit
                      <AddFlagModal :current-flag="flag" @flag-editing-completed="updateFlag($event, index)">
                        <template v-slot:title>Edit Flag</template>
                        <template v-slot:submitButtonText>Edit</template>
                      </AddFlagModal>
                    </TextButton>
                  </td>
                  <td><v-btn icon="mdi-trash-can-outline" variant="text" @click="deleteFlag(index)"></v-btn></td>
                </tr>
              </tbody>
            </v-table>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <SecondaryButton button-name="Add Flag" button-type="button">
              <AddFlagModal @flag-editing-completed="addFlag">
                <template v-slot:title>Add Flag</template>
                <template v-slot:submitButtonText>Add</template>
              </AddFlagModal>
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
                    <v-btn icon="mdi-trash-can-outline" variant="text" @click="deleteQuestion(index)"></v-btn>
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
