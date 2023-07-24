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
    class="elevation-2"
    variant="elevated"
    color="primary"
    :append-icon="appendIcon"
    @click="$emit('click')"
    :to="goTo"
    :type="buttonType"
  >
    <slot></slot>
    {{ buttonName }}
  </v-btn>
</template>
