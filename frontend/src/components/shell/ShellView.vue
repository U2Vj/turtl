<script lang="ts" setup>
import { onMounted, onBeforeUnmount, ref, watch, nextTick } from 'vue';
import RFB from '@novnc/novnc/core/rfb.js';
import { useVMManagerStore } from '@/stores/VMManagerStore';
import { useRouter } from 'vue-router';

const props = withDefaults(
  defineProps<{ taskId?: number; hidePopoutButton?: boolean; scaleViewport?: boolean }>(),
  {
    scaleViewport: false
  }
);

const rfb = ref<RFB>();
const vncContainer = ref<HTMLElement>();
const vmStore = useVMManagerStore();
const router = useRouter();
const environmentStatus = ref<string>('not_created');
const vmCount = ref<number>(0);
const connectionStatus = ref<string>('disconnected');
const isInitializing = ref<boolean>(false);
const hasConfig = ref<boolean | null>(null);
let statusPollingInterval: ReturnType<typeof setInterval> | null = null;

// loading flags for start/stop/cleanup buttons
const isStarting = ref(false);
const isStopping = ref(false);
const isCleaning = ref(false);

async function checkHasConfig() {
  if (!props.taskId) { hasConfig.value = null; return; }
  try {
    hasConfig.value = await vmStore.hasConfig(props.taskId);
  } catch (e) {
    console.error('Failed to check task config', e);
    hasConfig.value = false;
  }
}

async function loadEnvironmentStatus() {
  if (!props.taskId) return;
  try {
    const status = await vmStore.getEnvironmentStatus(props.taskId);
    if (!status) return;
    environmentStatus.value = status.status;
    vmCount.value = status.vm_count || 0;
  } catch (error) {
    console.error('Failed to load environment status:', error);
  }
}

function startStatusPolling() {
  if (statusPollingInterval || !props.taskId) return;
  statusPollingInterval = setInterval(() => {
    if (!isStarting.value && !isStopping.value && !isCleaning.value){
      loadEnvironmentStatus();
    }
  }, 5000);
}

function stopStatusPolling() {
  if (!statusPollingInterval) return;
  clearInterval(statusPollingInterval);
  statusPollingInterval = null;
}

async function startEnvironment() {
  if (!props.taskId) return;
  try {
    isStarting.value = true;
    if(environmentStatus.value === 'not_created') {
      environmentStatus.value = 'provisioning';
    }else{
      environmentStatus.value = 'starting';
    }
    const res = await vmStore.startEnvironment(props.taskId);
    if (res.status === 'created' || res.status === 'started'){
      environmentStatus.value = 'active';
    }
  } catch (error) {
    console.error('Failed to start environment', error);
  } finally {
    isStarting.value = false;
  }
}

async function cleanupEnvironment() {
  if (!props.taskId) return;
  try {
    isCleaning.value = true;
    environmentStatus.value = 'cleanup';
    const res = await vmStore.cleanupEnvironment(props.taskId);
    if (res.status === 'deleted'){
      environmentStatus.value = 'not_created';
    }
  } catch (error) {
    console.error('Failed to cleanup environment', error);
  } finally {
    isCleaning.value = false;
  }
}

async function stopEnvironment() {
  if (!props.taskId) return;
  try {
    isStopping.value = true;
    environmentStatus.value = 'stopping';
    const res = await vmStore.stopEnvironment(props.taskId);
    if (res.status === 'stopped'){
      environmentStatus.value = 'stopped';
    }
  } catch (error) {
    console.error('Failed to stop environment', error);
  } finally {
    isStopping.value = false;
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'active': return 'success';
    case 'starting': return 'warning';
    case 'stopping': return 'warning';
    case 'provisioning': return 'warning';
    case 'stopped': return 'red';
    case 'cleanup': return 'warning';
    case 'error': return 'error';
    default: return 'primary';
  }
};

const getStatusText = (status: string) => {
  switch (status) {
    case 'active': return 'Active';
    case 'starting': return 'Starting';
    case 'stopping': return 'Stopping';
    case 'provisioning': return 'Provisioning';
    case 'stopped': return 'Stopped';
    case 'cleanup': return 'Cleanup';
    case 'not_created': return 'Not Created';
    default: return status;
  }
}

function setupVNC() {
  if (!props.taskId || isInitializing.value) return;

  cleanup();

  nextTick(() => {
    const vncContainerElement = vncContainer.value;
    if (!vncContainerElement) return;

    isInitializing.value = true;

    const accessToken = localStorage.getItem('accessToken');
    vncContainerElement.innerHTML = '';

    const rfbOptions: any = {
      shared: true,
      wsProtocols: accessToken ? ['binary', `jwt.${accessToken}`] : ['binary'],
    };

    // Fetch VNC ticket to be used as VNC password
    (async () => {
      const base = `${import.meta.env.VITE_WS_URL}/ws/vm-console/${props.taskId}/`;
      let wsUrl = base;

      try {
        const { ticket, port } = await vmStore.getVNCTicket(props.taskId!);
        
        if (ticket) {
          rfbOptions.credentials = { username: 'proxmox', password: ticket };
        }

        const params = new URLSearchParams();
        if (ticket) params.set('ticket', ticket);
        if (port) params.set('port', String(port));

        const qs = params.toString();
        if (qs) wsUrl = `${base}?${qs}`;
      } catch (e) {
        console.error('Failed to fetch VNC ticket', e);
      }

      rfb.value = new RFB(vncContainerElement, wsUrl, rfbOptions);
      rfb.value.showDotCursor = true;

      rfb.value.addEventListener('connect', () => {
        console.log('VNC connected');
        connectionStatus.value = 'connected';
        isInitializing.value = false;
      });

      rfb.value.addEventListener('disconnect', () => {
        console.log('VNC disconnected');
        connectionStatus.value = 'disconnected';
        isInitializing.value = false;
      });

      rfb.value.addEventListener('credentialsrequired', () => {
        console.log('VNC credentials required');
        if (rfb.value && rfbOptions.credentials?.password) {
          rfb.value.sendCredentials({
            username: 'proxmox',
            password: rfbOptions.credentials.password
          });
        }
      });

      rfb.value.addEventListener('securityfailure', () => {
        console.log('VNC security failure');
        connectionStatus.value = 'error';
        isInitializing.value = false;
      });

      rfb.value.scaleViewport = props.scaleViewport;
      rfb.value.resizeSession = false;
    })();
  });
}

function cleanup() {
  console.log('Cleaning up VNC connection...');

  // RFB disconnect und cleanup
  if (rfb.value) {
    try {
      rfb.value.disconnect();
    } catch (e) {
      console.warn('Error disconnecting RFB:', e);
    }
    rfb.value = undefined;
  }

  connectionStatus.value = 'disconnected';
  isInitializing.value = false;

  // Container cleanup
  if (vncContainer.value) {
    vncContainer.value.innerHTML = '';
  }
}

onMounted(async () => {
  await checkHasConfig();
  if (hasConfig.value === true) {
    await loadEnvironmentStatus();
    startStatusPolling();
    if (environmentStatus.value === 'active') {
      setupVNC();
    }
  }
});

onBeforeUnmount(() => {
  cleanup();
  stopStatusPolling();
});

watch(environmentStatus, (newStatus, oldStatus) => {
  console.log(`Environment status changed: ${oldStatus} -> ${newStatus}`);

  if (newStatus === 'active' && oldStatus !== 'active') {
    // Wait for cleanup
    setTimeout(() => {
      setupVNC();
    }, 200);
  } else if (newStatus !== 'active') {
    cleanup();
  }
});

watch(() => props.taskId, async (newTaskId, oldTaskId) => {
  console.log(`Task ID changed: ${oldTaskId} -> ${newTaskId}`);

  cleanup();
  if (newTaskId) {
    startStatusPolling();
    await loadEnvironmentStatus();
    if (environmentStatus.value === 'active') {
      // Wait for cleanup
      setTimeout(() => {
        setupVNC();
      }, 200);
    }
  } else {
    stopStatusPolling();
  }
});
function reloadVNC() {
  cleanup();
  setupVNC();
}

function openPopout() {
  if (!props.taskId || typeof window === 'undefined') return;

  const resolvedRoute = router.resolve({
    name: 'ShellPopout',
    params: { taskId: props.taskId }
  });
  const popoutUrl = new URL(resolvedRoute.href, window.location.origin).toString();
  const popout = window.open(popoutUrl, '_blank', 'noopener,noreferrer');
  if (popout) {
    popout.focus();
  } else {
    console.warn('Unable to open pop-out window. Please allow pop-ups for this site.');
  }
}
</script>

<template>
  <div v-if="hasConfig" class="shell-container">
    <div v-if="taskId" class="vm-controls">
      <div class="d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-chip :color="getStatusColor(environmentStatus)" size="small" class="me-3">
            {{ getStatusText(environmentStatus) }}
          </v-chip>
          <v-btn v-if="environmentStatus === 'active' && connectionStatus === 'disconnected'" @click="reloadVNC"
            :loading="isInitializing" color="primary" size="small" variant="outlined">
            <v-icon size="small" class="me-1">mdi-refresh</v-icon>
            Reconnect Shell
          </v-btn>
          <v-btn v-if="environmentStatus === 'active' && taskId && !hidePopoutButton" class="ms-2" size="small"
            color="primary" variant="tonal" @click="openPopout">
            <v-icon size="small" class="me-1">mdi-open-in-new</v-icon>
            Shell
          </v-btn>
        </div>
        <div class="d-flex gap-2">
          <v-btn
            v-if="environmentStatus === 'not_created' || environmentStatus === 'stopped' || environmentStatus === 'provisioning' || environmentStatus === 'starting'"
            @click="startEnvironment" :loading="isStarting" color="success" size="small" variant="outlined">
            <v-icon size="small" class="me-1">mdi-play</v-icon>
            Start Environment
          </v-btn>

          <v-btn v-if="environmentStatus === 'active' || environmentStatus === 'stopping'" @click="stopEnvironment" :loading="isStopping"
            color="warning" size="small" variant="outlined">
            <v-icon size="small" class="me-1">mdi-stop</v-icon>
            Stop Environment
          </v-btn>

          <v-btn
            v-if="environmentStatus === 'active' || environmentStatus === 'stopped' || environmentStatus === 'cleanup'"
            @click="cleanupEnvironment" :loading="isCleaning" color="error" size="small" variant="outlined">
            <v-icon size="small" class="me-1">mdi-delete</v-icon>
            Delete Environment
          </v-btn>
        </div>
      </div>
      <v-alert v-if="vmStore.error" type="error" variant="tonal" class="mt-2" closable
        @click:close="vmStore.error = null">
        {{ vmStore.error }}
      </v-alert>
    </div>

    <div v-show="environmentStatus === 'active'" class="vnc-container-wrapper">
      <div ref="vncContainer" class="vnc-wrapper"></div>
    </div>

    <div v-if="environmentStatus !== 'active' && taskId" class="placeholder-message">
      Start the environment to use the VNC console.
    </div>
  </div>
</template>

<style scoped>
.shell-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #000;
}

.vm-controls {
  flex-shrink: 0;
  padding: 12px;
  border-bottom: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  background-color: rgba(var(--v-theme-surface));
}

.vnc-container-wrapper {
  flex: 1;
  display: flex;
  min-height: 0;
  overflow: hidden;
}

.vnc-wrapper {
  flex: 1;
  display: grid;
  place-items: center;
}

.placeholder-message {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(var(--v-theme-on-surface), 0.6);
  font-size: 1.1rem;
}

.gap-2 {
  gap: 8px;
}
</style>
