<script setup lang="ts">
import { ref } from 'vue'
</script>
<template>
  <v-card elevation="0">
    <v-footer>
      <v-row justify="center" no-gutters>
        <v-btn color="primary" variant="text" to="/privacypolicy"> Privacy Policy </v-btn>
        <v-btn color="primary" variant="text" to="/imprint"> Imprint </v-btn>
        <v-col class="text-center text-primary" cols="12">
          {{ new Date().getFullYear() }} - <strong>TURTL</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-card>
</template>
