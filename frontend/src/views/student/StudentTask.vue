<script setup lang="ts">
import Shell from '@/components/ShellView.vue'
import PrimaryButton from '@/components/buttons/PrimaryButton.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import { ref } from 'vue'

const taskDescription = ref(
  'Text that explains the task. Get the code and enter it in the field below. Text that explains the task. Get the code and enter it in the field below.'
)
</script>

<template>
  <DefaultLayout v-if="taskDescription">
    <template #heading>Task 1</template>
    <template #default>
      <v-row>
        <v-col cols="12">
          {{ taskDescription }}
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-textarea
            label="Enter Your Code here"
            clearable
            variant="underlined"
            base-color="primary"
            color="primary"
          ></v-textarea>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <Shell />
        </v-col>
      </v-row>
      <v-row class="mt-5">
        <v-col>
          <PrimaryButton buttonName="Verify Task" />
        </v-col>
      </v-row>
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
