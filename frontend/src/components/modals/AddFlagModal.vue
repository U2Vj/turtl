<script setup lang="ts">
import { useField, useForm } from 'vee-validate'
import { ref } from 'vue'
import * as yup from 'yup'
import PrimaryButton from '../buttons/PrimaryButton.vue'
import TextButton from '../buttons/TextButton.vue'
import type { Flag } from '@/stores/CatalogStore'

const showDialog = ref(false)

const props = defineProps<{currentFlag?: Flag}>()

const schema = yup.object({
  prompt: yup.string().required('This field is required').max(200),
  flag: yup.string().required('This field is required').max(200)
})
const { handleSubmit, resetForm } = useForm({ validationSchema: schema })

const { value: newPrompt, errorMessage: promptError } = useField<string>(
  'prompt',
  {},
  {
    validateOnValueUpdate: false,
    initialValue: (props.currentFlag) ? props.currentFlag.prompt : ''
  }
)

const { value: newFlag, errorMessage: flagError } = useField<string>(
  'flag',
  {},
  {
    validateOnValueUpdate: false,
    initialValue: (props.currentFlag) ? props.currentFlag.value : ''
  }
)

function resetDialog() {
  resetForm()
  showDialog.value = false
}

const emits = defineEmits<{ flagEditingCompleted: [flag: Flag]}>()

const addFlag = handleSubmit(() => {
  const flag: Flag = { prompt: newPrompt.value, value: newFlag.value }
  if(props.currentFlag) {
    flag.id = props.currentFlag.id
  }
  emits('flagEditingCompleted', { prompt: newPrompt.value, value: newFlag.value })
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
                :error-messages="promptError"
              >
              </v-textarea>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-textarea
                clearable
                variant="underlined"
                base-color="primary"
                color="primary"
                v-model="newFlag"
                label="Flag"
                :error-messages="flagError"
              >
              </v-textarea>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <TextButton
                button-name="Close"
                @click="resetDialog"
                button-type="button"
              ></TextButton>
              <PrimaryButton button-type="button" @click="addFlag"><slot name="submitButtonText"></slot></PrimaryButton>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
