<script setup lang="ts">
import type { DefineStoreOptionsInPlugin } from 'pinia';

defineProps<{
  appendIcon?: string,
  buttonName?: string,
  goTo?: string,
  buttonType?: string
}>()
</script>

<template>
    <v-btn class="elevation-2" variant="elevated" color="primary" :append-icon=appendIcon @click="$emit('atClick')" :to=goTo :type=buttonType>
      <slot></slot>
     {{ buttonName }}
    </v-btn>
</template>
