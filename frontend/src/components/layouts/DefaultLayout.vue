<script setup lang="ts">
import FooterTurtl from '@/components/FooterTurtl.vue'
import HeaderTurtl from '@/components/HeaderTurtl.vue'
</script>
<template>
  <HeaderTurtl />
  <v-main class="d-flex justify-center">
    <div class="main-container mt-5 ml-3 mr-3">
      <v-container fluid class="mt-5">
        <div class="d-flex mb-2 align-center justify-space-between">
          <h1>
            <slot name="heading"></slot>
          </h1>
          <slot name="postHeadingButton"></slot>
        </div>

        <slot name="default"></slot>
      </v-container>
    </div>
  </v-main>
  <FooterTurtl />
</template>

<style>
.main-container {
  min-width: 75%;
  max-width: 960px;
}
</style>
