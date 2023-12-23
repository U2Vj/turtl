<script setup lang="ts">
import { useField, useForm } from 'vee-validate'
import { ref } from 'vue'
import * as yup from 'yup'
import PrimaryButton from '../buttons/PrimaryButton.vue'
import TextButton from '../buttons/TextButton.vue'
import type {RegEx} from "@/stores/CatalogStore"

const showDialog = ref(false)

const props = defineProps<{ currentRegex?: RegEx }>()

const schema = yup.object({
  prompt: yup.string().required('This field is required').max(200),
  regex: yup.string().required('This field is required').max(200)
})
const { handleSubmit, resetForm } = useForm({ validationSchema: schema })

const { value: newPrompt, errorMessage: promptError } = useField<string>(
  'prompt',
  {},
  {
    validateOnValueUpdate: false,
    initialValue: (props.currentRegex) ? props.currentRegex.prompt : ''
  }
)

const { value: newRegex, errorMessage: regexError } = useField<string>(
  'regex',
  {},
  {
    validateOnValueUpdate: false,
    initialValue: (props.currentRegex) ? props.currentRegex.pattern : ''
  }
)


function resetDialog() {
  resetForm()
  showDialog.value = false
}

const emits = defineEmits<{regExEditingCompleted: [regex: RegEx]}>()

const addRegex = handleSubmit((values) => {
  const regex: RegEx = { prompt: values.prompt, pattern: values.regex }
  if(props.currentRegex) {
    regex.id = props.currentRegex.id
  }
  emits('regExEditingCompleted', regex)
  resetDialog()
})
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>
        <p><slot name="title"></slot></p>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="addRegex">
          <v-row>
            <v-col>
              <v-textarea
                clearable
                variant="underlined"
                base-color="primary"
                color="primary"
                v-model="newPrompt"
                label="Prompt"
                :error-messages="promptError"
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
                label="RegEx"
                :error-messages="regexError"
              >
              </v-text-field>
              <small>You do not need the opening or closing forward slashes, just the expression itself.</small>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <TextButton
                button-name="Close"
                @click="resetDialog"
                button-type="button"
              ></TextButton>
              <PrimaryButton button-type="submit">
                <slot name="submitButtonText"></slot>
              </PrimaryButton>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
