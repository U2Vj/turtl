<script setup lang="ts">
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import TextButton from '@/components/buttons/TextButton.vue'
import { ref } from 'vue'

const showDialog = ref(false)

function close() {
  showDialog.value = false
}

function join() {
  showDialog.value = false
}

const props = defineProps<{
  title: string
}>()
</script>
<template>
  <v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
      <v-card-title> Join the classroom: {{ props.title }} </v-card-title>
      <v-card-actions>
        <v-spacer></v-spacer>
        <TextButton buttonName="Cancel" @click="close"></TextButton>
        <PrimaryButton buttonName="Join Classroom" @click="join"> </PrimaryButton>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
