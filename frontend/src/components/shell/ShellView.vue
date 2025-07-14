<script lang="ts" setup>
import { onMounted, ref, watch } from 'vue';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import { useVMManagerStore } from '@/stores/VMManagerStore';

const props = defineProps<{ taskId?: number }>();

const term = ref<Terminal>();
const socket = ref<WebSocket>();
const vmStore = useVMManagerStore();
const environmentStatus = ref<string>('not_created')
const vmCount = ref<number>(0);

async function loadEnvironmentStatus() {
  if (!props.taskId) return;

  try {
    const status = await vmStore.getEnvironmentStatus(props.taskId);
    environmentStatus.value = status.status;
    vmCount.value = status.vm_count || 0;
  } catch (error) {
    console.error('Failed to load environment status:', error);
  }
}

async function startEnvironment() {
  if(!props.taskId) return;

  try{
    await vmStore.startEnvironment(props.taskId);
    await loadEnvironmentStatus();
  } catch (error){
    console.error('Failed to start environment', error);
  }
}

async function stopEnvironment() {
  if(!props.taskId) return;
  try{
    await vmStore.stopEnvironment(props.taskId);
    environmentStatus.value = 'not_created';
  } catch (error){
    console.error('Failed to start environment', error);
    await loadEnvironmentStatus();
  }
}

const getStatusColor = (status: string) =>{
  switch(status){
    case 'active':
      return 'success';
    case 'stopped':
      return 'info';
    case 'cleanup':
      return 'orange';
    case 'error':
      return 'error';
    default:
      return 'primary';
  }
};

const getStatusText = (status: string) =>{
  switch(status) {
    case 'active':
      return 'Active';
    case 'cleanup':
      return 'Cleanup';
    case 'not_created':
      return 'Not Created';
    default:
      return status;
  }
}

onMounted(async () => {
  await loadEnvironmentStatus();

  term.value = new Terminal({
    cursorBlink: true,
    convertEol: true,
  });

  socket.value = new WebSocket(import.meta.env.VITE_WS_URL);

  const fitAddon = new FitAddon();
  term.value.loadAddon(fitAddon);

  const terminalContainer = document.getElementById('terminal-container');
  if (terminalContainer) {
    term.value.open(terminalContainer);
  }

  fitAddon.fit();

  let commandBuffer = '';

  term.value.onKey(({ key, domEvent }) => {
    if (domEvent.key === 'Enter') {
      // Only send the command when Enter is pressed
      socket.value?.send(JSON.stringify({ message: commandBuffer }));
      commandBuffer = '';
    } else if (domEvent.key === 'Backspace') {
      // Handle backspace
      if (commandBuffer.length > 0) {
        commandBuffer = commandBuffer.slice(0, -1);
        term.value?.write('\b \b');
      }
    } else {
      // Accumulate other keys into commandBuffer
      commandBuffer += key;
      term.value?.write(key);
    }
  });

  // Handle incoming messages from the WebSocket
  socket.value.onmessage = (event) => {
    term.value?.write(event.data);
  };
});
watch(() => props.taskId, loadEnvironmentStatus);
</script>

<template>
  <div class="shell-container">
    <div v-if="taskId" class="vm-controls mb-4">
       <div class="d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-chip 
            :color="getStatusColor(environmentStatus)" 
            size="small" 
            class="me-3"
          >
            {{ getStatusText(environmentStatus) }}
          </v-chip>
        </div>
        <div class="d-flex gap-2">
          <v-btn
            v-if="environmentStatus === 'not_created'"
            @click="startEnvironment"
            :loading="vmStore.loading"
            color="success"
            size="small"
            variant="outlined"
          >
            <v-icon size="small" class="me-1">mdi-play</v-icon>
            Start Environment
          </v-btn>
          
          <v-btn
            v-if="environmentStatus === 'active'"
            @click="stopEnvironment"
            :loading="vmStore.loading"
            color="error"
            size="small"
            variant="outlined"
          >
            <v-icon size="small" class="me-1">mdi-delete</v-icon>
            Delete Environment
          </v-btn>
        </div>
       </div>
       <v-alert
           v-if="vmStore.error"
           type="error"
           variant="tonal"
           class="mt-2"
           closable
           @click:close="vmStore.error = null"
         >
           {{ vmStore.error }}
       </v-alert>
    </div>
    <div>
      <div :id="'terminal-container'" class="terminal-wrapper"></div>
    </div>
  </div>
</template>

<style src="xterm/css/xterm.css"></style>
<style scoped>
  .shell-container {
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .vm-controls {
    flex-shrink: 0;
    padding: 12px;
    border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
    border-radius: 4px;
    background-color: rgba(var(--v-theme-surface));
  }

  .terminal-wrapper {
    flex: 1;
    min-height: 400px;
  }

  .gap-2 {
    gap: 8px;
  }
</style>