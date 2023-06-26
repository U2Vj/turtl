<script setup lang="ts">
import HeaderTurtl from '@/components/HeaderTurtl.vue'
import FooterTurtl from '@/components/FooterTurtl.vue'
import { ref } from 'vue'
import { useTemplateStore } from '@/stores/TemplateStore'
import { useRouter } from 'vue-router'
import AddQuestionModal from '@/components/modals/AddQuestionModal.vue'

const props = defineProps<{ templateId: string; taskId: string }>()

const router = useRouter()

const templateStore = useTemplateStore()
const task = ref(templateStore.getTask(props.taskId))
</script>

<template>
  <HeaderTurtl />
  <v-main v-if="task" class="d-flex justify-center">
    <div class="main-container mt-5 ml-3 mr-3">
      <v-container fluid>
        <v-row>
          <v-col>
            <h1>{{ task.title }}</h1>
          </v-col>
          <v-col>
            <v-btn variant="tonal" color="error" class="elevation-2"> Delete </v-btn>
          </v-col>
        </v-row>
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
                v-model="task.type"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <h2>Questions</h2>
            </v-col>
          </v-row>
          <v-row v-if="task.acceptance_criteria.acceptance_criteria_questionaire">
            <v-col
              cols="12"
              v-for="question in task.acceptance_criteria.acceptance_criteria_questionaire"
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
                      v-model="question.question"
                    ></v-text-field>
                    <v-row v-for="choice in question.question_choice" :key="choice.answer">
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
                        <v-select
                          label="Correctness"
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
              <v-btn variant="tonal" color="primary" class="elevation-2">
                Add Question <AddQuestionModal />
              </v-btn>
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
                <v-card
                  :key="task.virtualization.id"
                  variant="flat"
                  color="cardColor"
                  class="elevation-4"
                >
                  <v-card-text>
                    <v-text-field
                      label="Edit Name of Virtualization"
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
                      label="Change File"
                      variant="underlined"
                      base-color="primary"
                      color="primary"
                    ></v-file-input>
                  </v-card-text>
                </v-card>
              </v-form>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn
                variant="text"
                color="primary"
                @click="router.push(`/admin/templates/${props.templateId}`)"
              >
                Close
              </v-btn>
            </v-col>
            <v-col>
              <v-btn variant="elevated" color="primary" class="ml-10 elevation-2"> Safe </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-container>
    </div>
  </v-main>
  <FooterTurtl />
</template>
