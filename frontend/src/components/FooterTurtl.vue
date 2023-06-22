<script setup lang="ts">
import { ref } from 'vue'
</script>
<template>
  <v-card variant="flat" color="cardColor" class="elevation-4">
    <v-footer color="cardColor">
      <v-row justify="center" no-gutters>
        <v-btn size="small" color="primary" variant="text" to="/privacypolicy">
          Privacy Policy
        </v-btn>
        <v-btn size="small" color="primary" variant="text" to="/imprint"> Imprint </v-btn>
        <v-col class="text-center text-primary" cols="12">
          {{ new Date().getFullYear() }} - <strong>TURTL</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-card>
</template>
