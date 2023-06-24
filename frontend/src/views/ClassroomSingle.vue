<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import Footer from '@/components/Footer.vue'
import Shell from '@/components/ShellView.vue'
import { ref } from 'vue'

const taskDescription = ref(
  'Text that explains the task. Get the code and enter it in the field below. Text that explains the task. Get the code and enter it in the field below.'
)
</script>

<template>
  <turtl-header></turtl-header>
  <v-main class="d-flex justify-center">
    <div class="main-container mt-5 ml-3 mr-3">
      <v-container fluid>
        <h1>Task 1</h1>
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
      </v-container>
    </div>
  </v-main>
  <Footer></Footer>
</template>
