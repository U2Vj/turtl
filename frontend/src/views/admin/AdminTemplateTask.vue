<script setup lang="ts">
import HeaderTurtl from '@/components/HeaderTurtl.vue'
import FooterTurtl from '@/components/FooterTurtl.vue'
import { ref, toRef } from 'vue'
import { useTemplateStore } from '@/stores/TemplateStore'

const props = defineProps<{ id: string }>()

const tab = ref(0)
const showCreateModal = ref(false)

const templateStore = useTemplateStore()

let templateData = toRef(templateStore, 'classroomTemplate')
templateStore.fetchTemplate(props.id)

// templateData.project_templates.task_template.acceptance_criteria.acceptance_criteria_questionaire.questions.question_choice.answer
</script>

<template>
  <HeaderTurtl />
  <v-main v-if="templateData" class="d-flex justify-center">
    <div class="main-container mt-5 ml-3 mr-3">
      <v-container fluid>
        <v-form>
          <v-text-field
            label="Edit Title"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
          ></v-text-field>
          <v-textarea
            label="Task Description"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
          >
          </v-textarea>
          <v-row>
            <v-col>
              <!-- <h2>Difficulty</h2> -->
              <v-select
                label="Select Difficulty Level"
                :items="['Beginner', 'Intermediate', 'Advanced']"
                variant="underlined"
                base-color="primary"
                color="primary"
              ></v-select>
            </v-col>
            <v-col>
              <!-- <h2>Task Type</h2> -->
              <v-select
                label="Select Difficulty Level"
                :items="['Neural', 'Attack', 'Defense']"
                variant="underlined"
                base-color="primary"
                color="primary"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" v-for="project in templateData.project_templates">
              <v-form>
                <v-card :key="project.id" variant="flat" color="cardColor" class="elevation-4">
                  <v-card-text>
                    <v-text-field
                      label="Edit Question"
                      clearable
                      variant="underlined"
                      base-color="primary"
                      color="primary"
                    ></v-text-field>
                    <v-row v-for="criteria in project.task_template">
                      <v-col>
                        <v-textarea
                          label="Edit Answer"
                          clearable
                          variant="underlined"
                          base-color="primary"
                          color="primary"
                        ></v-textarea>
                      </v-col>
                      <v-col>
                        <v-select
                          label="Correctness"
                          :items="['True', 'False']"
                          variant="underlined"
                          base-color="primary"
                          color="primary"
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
              <v-btn variant="tonal" color="primary" class="elevation-2"> Add Question </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="6" v-for="project in templateData.project_templates">
              <v-form>
                <v-card :key="project.id" variant="flat" color="cardColor" class="elevation-4">
                  <v-card-text>
                    <v-text-field
                      label="Edit Name of Virtualization"
                      clearable
                      variant="underlined"
                      base-color="primary"
                      color="primary"
                    ></v-text-field>
                    <v-select
                      label="Role"
                      :items="['UserShell', 'IP']"
                      variant="underlined"
                      base-color="primary"
                      color="primary"
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
                <v-btn variant="tonal" color="error" class="elevation-2"> Delete </v-btn>
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
