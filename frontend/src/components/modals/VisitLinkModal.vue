<script setup lang="ts">
import { ref } from 'vue'
import PrimaryButton from '../buttons/PrimaryButton.vue'
import TextButton from '../buttons/TextButton.vue'

const showDialog = ref(false)

const props = defineProps<{ url: string }>()
</script>

<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title>
        <slot name="title"></slot>
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col>
            <p><slot name="content"></slot></p>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <TextButton
              button-name="Close"
              @click="showDialog = false"
              button-type="button"
            ></TextButton>
            <PrimaryButton button-type="button" :href="props.url">
              <slot name="visitButtonText"></slot>
            </PrimaryButton>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>