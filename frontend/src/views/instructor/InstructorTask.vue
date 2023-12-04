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
import type { Flag, Question, RegEx, Task, Virtualization } from '@/stores/CatalogStore'
import {
  AcceptanceCriteriaType,
  QuestionType,
  TaskDifficulty,
  TaskType,
  VirtualizationRole,
  useCatalogStore
} from '@/stores/CatalogStore'
import { useField, useForm } from 'vee-validate'
import type { Ref } from 'vue'
import { ref, toRef } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import * as yup from 'yup'

const props = defineProps<{
  classroomId: number
  taskId: number
}>()

const toast = useToast()
const catalogStore = useCatalogStore()
const breadcrumbItems: Ref<any[]> = ref([])
const router = useRouter()

let task: Ref<Task | undefined> = ref(undefined)
let classroom = toRef(catalogStore, 'classroom')

const addRegEx = (regex: RegEx) => {
  if (!task.value) return

  if (task.value.acceptance_criteria?.regexes) {
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
    task.value?.acceptance_criteria.regexes?.splice(index, 0, regex)
  }, 2)
}

const deleteRegEx = (index: number) => {
  task.value?.acceptance_criteria.regexes?.splice(index, 1)
}

const addFlag = (flag: Flag) => {
  if (!task.value) return

  if (task.value.acceptance_criteria?.flags) {
    task.value.acceptance_criteria.flags.push(flag)
  } else {
    task.value.acceptance_criteria.flags = [flag]
  }
}

const updateFlag = (flag: Flag, index: number) => {
  deleteFlag(index)
  setTimeout(() => {
    task.value?.acceptance_criteria.flags?.splice(index, 0, flag)
  }, 2)
}

const deleteFlag = (index: number) => {
  task.value?.acceptance_criteria.flags?.splice(index, 1)
}

const addQuestion = (question: Question) => {
  if (!task.value) return

  if (task.value.acceptance_criteria?.questions) {
    task.value.acceptance_criteria.questions.push(question)
  } else {
    task.value.acceptance_criteria.questions = [question]
  }
}

const updateQuestion = (question: Question, index: number) => {
  deleteQuestion(index)
  setTimeout(() => {
    task.value?.acceptance_criteria.questions?.splice(index, 0, question)
  }, 2)
}

const deleteQuestion = (index: number) => {
  task.value?.acceptance_criteria.questions?.splice(index, 1)
}

const addVirtualization = (virtualization: Virtualization) => {
  task.value?.virtualizations.push(virtualization)
}

const updateVirtualization = (virtualization: Virtualization, index: number) => {
  deleteVirtualization(index)
  setTimeout(() => {
    task.value?.virtualizations.splice(index, 0, virtualization)
  }, 2)
}

const deleteVirtualization = (index: number) => {
  task.value?.virtualizations.splice(index, 1)
}

// Form validation for the Task title, description, type and difficulty
const schema = yup.object({
  title: yup.string().required('This field is required').max(50),
  description: yup.string().required('This field is required'),
  task_type: yup.string().required('This field is required'),
  difficulty: yup.string().required('This field is required')
})
const { handleSubmit } = useForm({ validationSchema: schema })

const { value: title, errorMessage: titleError } = useField<string>(
  'title',
  {},
  {
    validateOnValueUpdate: false
  }
)

const { value: description, errorMessage: descriptionError } = useField<string>(
  'description',
  {},
  {
    validateOnValueUpdate: false
  }
)

const { value: taskType, errorMessage: taskTypeError } = useField<string>(
  'task_type',
  {},
  {
    validateOnValueUpdate: false
  }
)

const { value: difficulty, errorMessage: difficultyError } = useField<string>(
  'difficulty',
  {},
  {
    validateOnValueUpdate: false
  }
)

const selectDifficulty = [
  {
    title: 'Beginner',
    value: TaskDifficulty.Beginner
  },
  {
    title: 'Intermediate',
    value: TaskDifficulty.Intermediate
  },
  {
    title: 'Advanced',
    value: TaskDifficulty.Advanced
  }
]
const selectTaskType = [
  {
    title: 'Neutral',
    value: TaskType.Neutral
  },
  {
    title: 'Attack',
    value: TaskType.Attack
  },
  {
    title: 'Defense',
    value: TaskType.Defense
  }
]

const saveTask = handleSubmit(async (values) => {
  if (!task.value) return
  task.value.title = values.title
  task.value.description = values.description
  task.value.difficulty = values.difficulty
  task.value.task_type = values.task_type

  // Determine AcceptanceCriteria type
  let differentCriteriaTypes = 0
  if (
    task.value.acceptance_criteria.questions &&
    task.value.acceptance_criteria.questions.length > 0
  ) {
    task.value.acceptance_criteria.criteria_type = AcceptanceCriteriaType.Quiz
    differentCriteriaTypes++
  }
  if (task.value.acceptance_criteria.flags && task.value.acceptance_criteria.flags.length > 0) {
    task.value.acceptance_criteria.criteria_type = AcceptanceCriteriaType.Flag
    differentCriteriaTypes++
  }
  if (task.value.acceptance_criteria.regexes && task.value.acceptance_criteria.regexes.length > 0) {
    task.value.acceptance_criteria.criteria_type = AcceptanceCriteriaType.RegEx
    differentCriteriaTypes++
  }
  if (differentCriteriaTypes > 1) {
    task.value.acceptance_criteria.criteria_type = AcceptanceCriteriaType.Mixed
  } else if (differentCriteriaTypes === 0) {
    task.value.acceptance_criteria.criteria_type = AcceptanceCriteriaType.Disabled
  }

  catalogStore
    .updateTask(task.value)
    .then(() => {
      router.push({
        name: 'InstructorClassroom',
        params: {
          classroomId: props.classroomId
        }
      })
      toast.success('Changes saved.')
      task.value = catalogStore.getTask(props.taskId)
    })
    .catch((e) => toast.error(e.message))
})

// Retrieve the Task from the backend and set the form values
try {
  catalogStore
    .getClassroom(props.classroomId)
    .then(() => {
      task.value = catalogStore.getTask(props.taskId)
      breadcrumbItems.value = [
        {
          title: 'My Classrooms',
          disabled: false,
          to: {
            name: 'InstructorMyClassrooms'
          }
        },
        {
          title: classroom.value?.title,
          disabled: false,
          to: {
            name: 'InstructorClassroom',
            params: {
              classroomId: props.classroomId
            }
          }
        },
        {
          title: task.value?.title,
          disabled: true
        }
      ]
      if (!task.value) return
      title.value = task.value.title
      description.value = task.value.description
      difficulty.value = task.value.difficulty
      taskType.value = task.value.task_type
    })
    .catch((e) => {
      toast.error(e.message)
    })
} catch (e: any) {
  toast.error(e.message)
}
</script>
<template>
  <DefaultLayout v-if="task" :breadcrumb-items="breadcrumbItems">
    <template #heading>{{ task.title }}</template>
    <template #postHeadingButton>
      <ErrorButton button-name="Delete">
        <DeleteTaskModal :task="task" :classroom-id="classroomId"></DeleteTaskModal>
      </ErrorButton>
    </template>
    <template #default>
      <v-form @submit.prevent="saveTask">
        <v-text-field
          label="Edit Title"
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="title"
          :error-messages="titleError"
        ></v-text-field>
        <v-textarea
          label="Task Description"
          clearable
          variant="underlined"
          base-color="primary"
          color="primary"
          v-model="description"
          :error-messages="descriptionError"
        ></v-textarea>
        <v-row>
          <v-col>
            <v-select
              label="Select Difficulty Level"
              :items="selectDifficulty"
              variant="underlined"
              base-color="primary"
              color="primary"
              v-model="difficulty"
              :error-messages="difficultyError"
            ></v-select>
          </v-col>
          <v-col>
            <v-select
              label="Select Task Type"
              :items="selectTaskType"
              variant="underlined"
              base-color="primary"
              color="primary"
              v-model="taskType"
              :error-messages="taskTypeError"
            ></v-select>
          </v-col>
        </v-row>
        <v-row
          ><v-col><v-divider></v-divider></v-col
        ></v-row>
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
            <v-table
              v-if="
                task.acceptance_criteria?.regexes && task.acceptance_criteria.regexes.length > 0
              "
            >
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
                      <AddRegexModal
                        :current-regex="regEx"
                        @reg-ex-editing-completed="updateRegEx($event, index)"
                      >
                        <template v-slot:title>Edit RegEx</template>
                        <template v-slot:submitButtonText>Edit</template>
                      </AddRegexModal>
                    </TextButton>
                  </td>
                  <td>
                    <v-btn
                      icon="mdi-trash-can-outline"
                      variant="text"
                      @click="deleteRegEx(index)"
                    ></v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <p v-else>This Task does not contain any RegExes yet.</p>
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
            <v-table
              v-if="task.acceptance_criteria?.flags && task.acceptance_criteria.flags.length > 0"
            >
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
                      <AddFlagModal
                        :current-flag="flag"
                        @flag-editing-completed="updateFlag($event, index)"
                      >
                        <template v-slot:title>Edit Flag</template>
                        <template v-slot:submitButtonText>Edit</template>
                      </AddFlagModal>
                    </TextButton>
                  </td>
                  <td>
                    <v-btn
                      icon="mdi-trash-can-outline"
                      variant="text"
                      @click="deleteFlag(index)"
                    ></v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <p v-else>This Task does not contain any Flags yet.</p>
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
            <v-table
              v-if="
                task.acceptance_criteria?.questions && task.acceptance_criteria.questions.length > 0
              "
            >
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
                      <AddQuestionModal
                        :current-question="question"
                        @question-editing-completed="updateQuestion($event, index)"
                      >
                        <template v-slot:title>Edit Question</template>
                        <template v-slot:submitButtonText>Edit</template>
                      </AddQuestionModal>
                    </TextButton>
                  </td>
                  <td>
                    <v-btn
                      icon="mdi-trash-can-outline"
                      variant="text"
                      @click="deleteQuestion(index)"
                    ></v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <p v-else>This Task does not contain any Questions yet.</p>
            <br />
            <SecondaryButton button-name="Add Question" button-type="button">
              <AddQuestionModal @question-editing-completed="addQuestion">
                <template v-slot:title>Add Question</template>
                <template v-slot:submitButtonText>Add</template>
              </AddQuestionModal>
            </SecondaryButton>
          </v-col>
        </v-row>
        <v-row
          ><v-col><v-divider></v-divider></v-col
        ></v-row>
        <v-row>
          <v-col>
            <h2>Virtualization</h2>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-table v-if="task.virtualizations.length > 0">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Role</th>
                  <th>Edit</th>
                  <th>Delete</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(virtualization, index) in task.virtualizations" :key="index">
                  <td>{{ virtualization.name }}</td>
                  <td v-if="virtualization.virtualization_role === VirtualizationRole.UserShell">
                    User Shell
                  </td>
                  <td v-else>User-accessible via IP</td>
                  <td>
                    <TextButton button-type="button">
                      <v-icon icon="mdi-pencil"></v-icon>&nbsp;Edit
                      <AddVirtualizationModal
                        :current-virtualization="virtualization"
                        @virtualization-editing-completed="updateVirtualization($event, index)"
                      >
                        <template v-slot:title>Edit Virtualization</template>
                        <template v-slot:submitButtonText>Edit</template>
                      </AddVirtualizationModal>
                    </TextButton>
                  </td>
                  <td>
                    <v-btn
                      icon="mdi-trash-can-outline"
                      variant="text"
                      @click="deleteVirtualization(index)"
                    ></v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>
            <p v-else>This Task does not contain any virtualizations yet.</p>
            <br />
            <SecondaryButton button-name="Add Virtualization" button-type="button">
              <AddVirtualizationModal @virtualization-editing-completed="addVirtualization">
                <template v-slot:title>Add Virtualization</template>
                <template v-slot:submitButtonText>Add</template>
              </AddVirtualizationModal>
            </SecondaryButton>
          </v-col>
        </v-row>
        <v-row
          ><v-col><v-divider></v-divider></v-col
        ></v-row>
        <v-row>
          <v-col>
            <div class="d-flex mb-5 align-center justify-space-between">
              <TextButton
                button-name="Close"
                :go-to="`/instructor/classrooms/${props.classroomId}`"
                button-type="button"
              ></TextButton>
              <PrimaryButton button-name="Save" button-type="submit"></PrimaryButton>
            </div>
          </v-col>
        </v-row>
      </v-form>
    </template>
  </DefaultLayout>
  <div v-else class="center-screen">
    <v-progress-circular indeterminate color="primary" :size="50"></v-progress-circular>
  </div>
</template>

<style scoped>
.center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
