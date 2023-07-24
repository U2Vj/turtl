<script setup lang="ts">
import TextButton from '@/components/buttons/TextButton.vue'
</script>

<template>
  <v-card variant="flat" color="cardColor" class="elevation-4">
    <v-footer color="cardColor">
      <v-row justify="center" no-gutters>
        <TextButton buttonName="Privacy Policy" goTo="/privacypolicy"></TextButton>
        <TextButton buttonName="Imprint" goTo="/imprint"></TextButton>
        <v-col class="text-center text-primary" cols="12">
          {{ new Date().getFullYear() }} - <strong>TURTL</strong>
        </v-col>
      </v-row>
    </v-footer>
  </v-card>
</template>
