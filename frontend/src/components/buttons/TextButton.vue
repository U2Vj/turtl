<script setup lang="ts">
defineProps<{
  appendIcon?: string
  buttonName?: string
  goTo?: string
  buttonType?: string
  singleIcon?: string
}>()
</script>

<template>
  <v-btn
    variant="text"
    :icon="singleIcon"
    color="primary"
    :append-icon="appendIcon"
    :to="goTo"
    :type="buttonType"
  >
    <slot></slot>
    {{ buttonName }}
  </v-btn>
</template>
