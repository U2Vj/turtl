<script setup lang="ts">
import { ref } from 'vue'
</script>
<template>
    <v-card>
  <v-footer
    color="primary"
  >
    <v-row
      justify="center"
      no-gutters
    >
      <v-btn
        color="white"
        variant="text"
        rounded="xl"
      >
        Privacy Policy
      </v-btn>
      <v-btn
        color="white"
        variant="text"
        rounded="xl"
      >
        Imprint
      </v-btn>
      <v-col
        class="primary lighten-2 text-center white--text"
        cols="12"
      >
        {{ new Date().getFullYear() }} - <strong>TURTL</strong>
      </v-col>
    </v-row>
  </v-footer>
  </v-card>
</template>