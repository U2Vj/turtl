<script lang="ts" setup>
import { onMounted, onBeforeUnmount, ref, watch, nextTick } from 'vue';
import RFB from '@novnc/novnc/core/rfb.js';
import { useVMManagerStore } from '@/stores/VMManagerStore';
import { useRouter } from 'vue-router';
import {
  KEYBOARD_LAYOUT_DE,
  SHIFT_KEYSYM,
  ALTGR_KEYSYM,
  SPACE_KEYSYM,
} from './keyboardLayouts';

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

const showClipboard = ref(false);
const clipboardText = ref('');
const isTyping = ref(false);
const typingProgress = ref(0);
let cancelTyping = false;

const SUB_EVENT_DELAY = 5;
const PER_CHAR_DELAY = 35;
const sleep = (ms: number) => new Promise(res => setTimeout(res, ms));

async function pressKey(r: any, ks: number, code: string | undefined, down: boolean) {
  r.sendKey(ks, code, down);
  await sleep(SUB_EVENT_DELAY);
}

async function tapKey(r: any, ks: number, code: string | undefined) {
  await pressKey(r, ks, code, true);
  await pressKey(r, ks, code, false);
}

async function sendChar(r: any, ch: string) {
  const spec = KEYBOARD_LAYOUT_DE[ch];
  if (!spec) {
    await tapKey(r, ch.charCodeAt(0), undefined);
    return;
  }
  const ks = spec.keysym ?? ch.charCodeAt(0);
  if (spec.shift) await pressKey(r, SHIFT_KEYSYM, 'ShiftLeft', true);
  if (spec.altgr) await pressKey(r, ALTGR_KEYSYM, 'AltRight', true);
  await tapKey(r, ks, spec.code);
  if (spec.altgr) await pressKey(r, ALTGR_KEYSYM, 'AltRight', false);
  if (spec.shift) await pressKey(r, SHIFT_KEYSYM, 'ShiftLeft', false);
  if (spec.dead) await tapKey(r, SPACE_KEYSYM, 'Space');
}

async function toggleTyping() {
  if (isTyping.value) {
    cancelTyping = true;
    return;
  }
  if (!rfb.value || connectionStatus.value !== 'connected' || !clipboardText.value) return;

  isTyping.value = true;
  cancelTyping = false;
  typingProgress.value = 0;

  const text = clipboardText.value;
  const r = rfb.value as any;

  try {
    for (let i = 0; i < text.length; i++) {
      if (cancelTyping) break;
      if (text[i] !== '\r') {
        await sendChar(r, text[i]);
        await sleep(PER_CHAR_DELAY);
      }
      typingProgress.value = i + 1;
    }
  } catch (e) {
    console.warn('typing aborted', e);
  } finally {
    try {
      r.sendKey(ALTGR_KEYSYM, 'AltRight', false);
      r.sendKey(SHIFT_KEYSYM, 'ShiftLeft', false);
    } catch {}
    isTyping.value = false;
    cancelTyping = false;
  }
}

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
    case 'degraded': return 'warning';
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
    case 'degraded': return 'Degraded';
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
      if (import.meta.env.DEV && !import.meta.env.VITE_WS_URL) {
        throw new Error('VITE_WS_URL is required in dev. Set it in frontend/.env.development.')
      }
      const wsProto = globalThis.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsBase = import.meta.env.DEV
        ? import.meta.env.VITE_WS_URL
        : `${wsProto}//${globalThis.location.host}/shell`;
      const wsUrl = `${wsBase}/ws/vm-console/${props.taskId}/`;

      try {
        const { ticket, port } = await vmStore.getVNCTicket(props.taskId!);
        
        if (ticket) {
          rfbOptions.credentials = { username: 'proxmox', password: ticket };
          const encodedTicket = btoa(ticket).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/g, '');
          rfbOptions.wsProtocols.push(`vnc.${encodedTicket}`);
        }

        if (port) {
          rfbOptions.wsProtocols.push(`vncport.${String(port)}`);
        }
      } catch (e) {
        console.error('Failed to fetch VNC ticket', e);
      }

      // Capture the close code from the WebSocket to display ws rate limit.
      const OriginalWebSocket = globalThis.WebSocket;
      globalThis.WebSocket = new Proxy(OriginalWebSocket, {
        construct(target, args) {
          const ws = new (target as any)(...args);
          ws.addEventListener('close', (event: CloseEvent) => {
            if (event.code === 4429) {
              vmStore.error = 'Too many active shell sessions. Close another tab and try again.';
            }
          });
          return ws;
        }
      });
      try {
        rfb.value = new RFB(vncContainerElement, wsUrl, rfbOptions);
      } finally {
        globalThis.WebSocket = OriginalWebSocket;
      }
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

  if (isTyping.value) {
    cancelTyping = true;
  }

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
  if (!props.taskId || !globalThis.location || typeof globalThis.open !== 'function') return;

  const resolvedRoute = router.resolve({
    name: 'ShellPopout',
    params: { taskId: props.taskId }
  });
  const popoutUrl = new URL(resolvedRoute.href, globalThis.location.origin).toString();
  const popout = globalThis.open(popoutUrl, '_blank', 'noopener,noreferrer');
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
          <v-btn v-if="environmentStatus === 'active' && connectionStatus === 'connected'" class="ms-2" size="small"
            color="primary" variant="tonal" @click="showClipboard = !showClipboard">
            <v-icon size="small" class="me-1">mdi-clipboard-text</v-icon>
            Clipboard
          </v-btn>
          <v-btn
            v-if="environmentStatus === 'not_created' || environmentStatus === 'stopped' || environmentStatus === 'provisioning' || environmentStatus === 'starting' || environmentStatus === 'degraded'"
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
            v-if="environmentStatus === 'active' || environmentStatus === 'degraded' || environmentStatus === 'stopped' || environmentStatus === 'cleanup'"
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
      <div v-if="showClipboard" class="clipboard-panel">
        <div class="clipboard-header">
          <span class="clipboard-title">Clipboard</span>
          <v-btn icon="mdi-close" size="x-small" variant="text" @click="showClipboard = false" />
        </div>
        <v-textarea
          v-model="clipboardText"
          class="clipboard-textarea"
          placeholder="Enter text to copy to the machine"
          hide-details
          variant="outlined"
          :readonly="isTyping"
          no-resize
        />
        <div class="clipboard-actions">
          <v-btn
            :color="isTyping ? 'error' : 'primary'"
            :disabled="!isTyping && !clipboardText"
            size="small"
            variant="tonal"
            @click="toggleTyping"
          >
            <v-icon size="small" class="me-1">{{ isTyping ? 'mdi-stop' : 'mdi-keyboard' }}</v-icon>
            {{ isTyping ? `Stop (${typingProgress}/${clipboardText.length})` : 'PASTE' }}
          </v-btn>
        </div>
      </div>
    </div>

    <div v-if="environmentStatus !== 'active' && taskId" class="placeholder-message">
      {{ environmentStatus === 'degraded'
        ? 'The environment is degraded. Start it to recover the missing VMs, or stop/delete it.'
        : 'Start the environment to use the VNC console.' }}
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

.clipboard-panel {
  flex-shrink: 0;
  width: 320px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background-color: rgba(var(--v-theme-surface));
  border-left: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
}

.clipboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.clipboard-title {
  font-weight: 500;
}

.clipboard-textarea {
  flex: 1;
}

.clipboard-textarea :deep(.v-field),
.clipboard-textarea :deep(.v-field__field),
.clipboard-textarea :deep(textarea) {
  height: 100%;
}

.clipboard-actions {
  display: flex;
  justify-content: flex-end;
}
</style>
