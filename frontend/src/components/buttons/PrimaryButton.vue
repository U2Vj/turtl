<script setup lang="ts">
defineProps<{
  appendIcon?: string
  buttonName?: string
  goTo?: string
  buttonType?: string
  href?: string
}>()
</script>

<template>
  <v-btn
    class="elevation-2"
    variant="elevated"
    color="primary"
    :append-icon="appendIcon"
    :to="goTo"
    :type="buttonType"
    :href="href"
  >
    <slot></slot>
    {{ buttonName }}
  </v-btn>
</template>
