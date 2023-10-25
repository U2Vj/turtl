<script setup lang="ts">
import { useField, useForm, useResetForm } from 'vee-validate'
import { ref } from 'vue'
import * as yup from 'yup'
import PrimaryButton from '../buttons/PrimaryButton.vue'
import TextButton from '../buttons/TextButton.vue'

const showDialog = ref(false)

const schema = yup.object({
  prompt: yup.string().required('This field is required').max(200),
  regex: yup.string().required('This field is required')
})
const { handleSubmit } = useForm({ validationSchema: schema })

const { value: newPrompt, errorMessage: promptError } = useField<string>(
  'prompt',
  {},
  { validateOnValueUpdate: false }
)

const { value: newRegex, errorMessage: regexError } = useField<string>(
  'regex',
  {},
  { validateOnValueUpdate: false }
)

const resetForm = useResetForm()

function resetDialog() {
  resetForm()
  showDialog.value = false
}

const emits = defineEmits()

const addRegex = () => {
  const regexPrompt = newPrompt.value
  const regex = newRegex.value
  emits('addRegex', { regexPrompt, regex })

  resetDialog()
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>
        <p>Add Regex</p>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-row>
            <v-col>
              <v-textarea
                clearable
                variant="underlined"
                base-color="primary"
                color="primary"
                v-model="newPrompt"
                label="Prompt"
                :rules="[(v) => (v || '').length <= 200 || 'Prompt must be 200 characters or less']"
              >
              </v-textarea>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                clearable
                variant="underlined"
                base-color="primary"
                color="primary"
                v-model="newRegex"
                label="Regex"
              >
              </v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <TextButton
                button-name="Close"
                @click="resetDialog"
                button-type="button"
              ></TextButton>
              <PrimaryButton
                button-name="Add"
                button-type="button"
                @click="addRegex"
              ></PrimaryButton>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
