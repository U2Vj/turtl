<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
</script>

<template>
  <DefaultLayout>
    <template #default>
      <v-container class="fill-height" fluid>
        <v-row justify="center" align="center">
          <v-col cols="12" sm="8" md="6">
            <div class="text-center">
              <h1 class="display-1 font-weight-bold mb-4">404</h1>
              <h2 class="subtitle-1 font-weight-regular">Page Not Found</h2>
              <p class="caption">The page you requested could not be found.</p>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </template>
  </DefaultLayout>
</template>
