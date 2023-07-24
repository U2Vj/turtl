<script setup lang="ts">
defineProps<{
  prependIcon?: string
  buttonName?: string
  goTo?: string
  buttonType?: string
}>()
</script>

<template>
  <v-btn
    class="elevation-2"
    variant="tonal"
    color="primary"
    :prepend-icon="prependIcon"
    @click="$emit('atClick')"
    :to="goTo"
    :type="buttonType"
  >
    <slot></slot>
    {{ buttonName }}
  </v-btn>
</template>
