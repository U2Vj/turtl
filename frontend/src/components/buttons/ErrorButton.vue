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
    variant="tonal"
    :icon="singleIcon"
    color="error"
    class="elevation-2"
    :append-icon="appendIcon"
    @click="$emit('click')"
    :to="goTo"
    :type="buttonType"
  >
    <slot></slot>
    {{ buttonName }}
  </v-btn>
</template>
