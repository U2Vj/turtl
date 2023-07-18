<script setup lang="ts">
defineProps<{
  appendIcon?: string
  buttonName?: string
  goTo?: string
  buttonType?: string
}>()
</script>

<template>
  <v-btn
    variant="text"
    color="primary"
    :append-icon="appendIcon"
    @click="$emit('atClick')"
    :to="goTo"
    :type="buttonType"
  >
    <slot></slot>
    {{ buttonName }}
  </v-btn>
</template>
