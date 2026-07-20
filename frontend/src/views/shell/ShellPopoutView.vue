<script setup lang="ts">
import Shell from '@/components/shell/ShellView.vue';
import { computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const extractString = (value: unknown): string | undefined => {
  if (typeof value === 'string') return value;
  if (Array.isArray(value) && typeof value[0] === 'string') return value[0];
  return undefined;
};

const taskId = computed<number | undefined>(() => {
  const raw = extractString(route.params.taskId) ?? extractString(route.query.taskId);

  const parsed = raw ? Number(raw) : Number.NaN;
  return Number.isFinite(parsed) ? parsed : undefined;
});
</script>

<template>
  <div class="popout-shell">
    <Shell
      v-if="taskId"
      :task-id="taskId"
      hide-popout-button
      :scale-viewport="true"
    />
    <div v-else class="popout-shell__error">
      Missing or invalid task id.
    </div>
  </div>
</template>

<style scoped>
.popout-shell {
  height: 95vh;
  width: 100vw;
  background-color: #000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.popout-shell__error {
  color: rgba(var(--v-theme-on-surface), 0.8);
  margin: auto;
}
</style>
