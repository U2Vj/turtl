<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import Shell from '@/components/ShellView.vue'
import { ref } from 'vue'

const taskDescription = ref(
  'Text that explains the task. Get the code and enter it in the field below. Text that explains the task. Get the code and enter it in the field below.'
)
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col cols="12" sm="8" md="4">
          <div><h1>Task 1</h1></div>
          <div>
            <div class="mt-5">{{ taskDescription }}</div>
            <div class="mt-5">
              <v-textarea label="Enter Your Code here"></v-textarea>
            </div>
            <div>
              <v-btn class="mt-5">Verity Task</v-btn>
            </div>
          </div>
        </v-col>
        <v-col>
          <Shell />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>
