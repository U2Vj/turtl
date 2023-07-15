<script setup lang="ts">
import FooterTurtl from '@/components/FooterTurtl.vue'
import HeaderTurtl from '@/components/HeaderTurtl.vue'
</script>
<template>
  <HeaderTurtl />
  <v-main>
    <v-container fluid class="w-75 mt-5">
      <div class="d-flex mb-2 align-center justify-space-between">
        <h1>
          <slot name="heading"></slot>
        </h1>
        <slot name="postHeadingButton"></slot>
      </div>

      <slot name="default"></slot>
    </v-container>
  </v-main>
  <FooterTurtl />
</template>
