<script setup lang="ts">
import DefaultFooter from '@/components/DefaultFooter.vue'
import DefaultHeader from '@/components/DefaultHeader.vue'
import { defineProps } from 'vue'

const props = defineProps({
  breadcrumbItems: Array
})
</script>
<template>
  <DefaultHeader />
  <v-main class="d-flex justify-center">
    <div>
      <v-breadcrumbs :items="breadcrumbItems" density="compact"></v-breadcrumbs>
    </div>
    <div class="main-container mt-5 ml-3 mr-3">
      <v-container fluid>
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
  <DefaultFooter />
</template>

<style>
.main-container {
  min-width: 75%;
  max-width: 960px;
}
</style>
