<script setup lang="ts">
import TurtlHeader from '@/components/TurtlHeader.vue'
import Shell from '@/components/ShellView.vue'
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col>
          <Shell />
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>
