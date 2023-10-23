<script setup lang="ts">
import { useField, useForm, useResetForm } from 'vee-validate'
import { ref } from 'vue'
import * as yup from 'yup'
import PrimaryButton from '../buttons/PrimaryButton.vue'
import TextButton from '../buttons/TextButton.vue'

const showDialog = ref(false)

const schema = yup.object({
  promt: yup.string().required('This field is required').max(200),
  flag: yup.string().required('This field is required')
})
const { handleSubmit } = useForm({ validationSchema: schema })

const { value: newPromt, errorMessage: promtError } = useField<string>(
  'promt',
  {},
  { validateOnValueUpdate: false }
)

const { value: newFlag, errorMessage: flagError } = useField<string>(
  'flag',
  {},
  { validateOnValueUpdate: false }
)

const resetForm = useResetForm()

function resetDialog() {
  resetForm()
  showDialog.value = false
}
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>
        <p>Add Flag</p>
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
                v-model="newPromt"
                label="Promt"
                :rules="[(v) => (v || '').length <= 200 || 'Promt must be 200 characters or less']"
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
                v-model="newFlag"
                label="Flag"
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
              <PrimaryButton button-name="Add" button-type="submit"></PrimaryButton>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
