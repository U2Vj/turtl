<script setup lang="ts">
import Shell from '@/components/ShellView.vue'
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import { ref } from 'vue'

const taskDescription = ref(
  'Text that explains the task. Get the code and enter it in the field below. Text that explains the task. Get the code and enter it in the field below.'
)
</script>

<template>
  <DefaultLayout>
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
      <v-row>
        <v-col>
          <v-btn class="mt-5 elevation-2" variant="elevated" color="primary">Verify Task</v-btn>
        </v-col>
      </v-row>
    </template>
  </DefaultLayout>
</template>
