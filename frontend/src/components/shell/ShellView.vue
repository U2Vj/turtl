<script lang="ts" setup>
import { onMounted, onBeforeUnmount, ref, watch, nextTick } from 'vue';
import RFB from '@novnc/novnc/core/rfb.js';
import { useVMManagerStore } from '@/stores/VMManagerStore';
import { makeAPIRequest } from '@/communication/APIRequests';

const props = defineProps<{ taskId?: number }>();

const rfb = ref<RFB>();
const vncContainer = ref<HTMLElement>();
const vmStore = useVMManagerStore();
const environmentStatus = ref<string>('not_created');
const vmCount = ref<number>(0);
const connectionStatus = ref<string>('disconnected');
const isInitializing = ref<boolean>(false);
const hasConfig = ref<boolean | null>(null);

async function checkHasConfig() {
  if (!props.taskId) { hasConfig.value = null; return; }
  try {
    const resp = await makeAPIRequest(`/vm/has-config/${props.taskId}/`, 'GET', true, true);
    hasConfig.value = !!resp.data?.has_config;
  } catch (e) {
    console.error('Failed to check task config', e);
    hasConfig.value = false;
  }
}

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
    environmentStatus.value = 'provisioning';
    await vmStore.startEnvironment(props.taskId);
    await loadEnvironmentStatus();
  } catch (error){
    console.error('Failed to start environment', error);
    await loadEnvironmentStatus();
  }
}

async function stopEnvironment() {
  if(!props.taskId) return;
  try{
    environmentStatus.value = 'cleanup';
    await vmStore.stopEnvironment(props.taskId);
    await loadEnvironmentStatus();
  } catch (error){
    console.error('Failed to stop environment', error);
    await loadEnvironmentStatus();
  }
}

const getStatusColor = (status: string) =>{
  switch(status){
    case 'active': return 'success';
    case 'provisioning': return 'warning';
    case 'suspended': return 'info';
    case 'cleanup': return 'orange';
    case 'error': return 'error';
    default: return 'primary';
  }
};

const getStatusText = (status: string) =>{
  switch(status) {
    case 'active': return 'Active';
    case 'provisioning': return 'Provisioning';
    case 'suspended': return 'Suspended';
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
      let wsUrlBuilt: string | null = null;
      try {
        const resp = await makeAPIRequest(`/vm/vnc-ticket/${props.taskId}/`, 'GET', true, true);
        const ticket = resp.data?.ticket;
        const port = resp.data?.port;
        if (ticket) {
          rfbOptions.credentials = { username: 'proxmox', password: ticket };
        }
        // Backend consumer will forward to Proxmox using these values.
        const base = `${import.meta.env.VITE_WS_URL}/ws/vm-console/${props.taskId}/`;
        const qp = new URLSearchParams();
        if (ticket) qp.set('ticket', ticket);
        if (port) qp.set('port', String(port));
        const qpStr = qp.toString();
        wsUrlBuilt = qpStr ? `${base}?${qpStr}` : base;
      } catch (e) {
        console.error('Failed to fetch VNC ticket', e);
      } finally {
        // If no explicit wsUrl above (ticket fetch failed), fall back to base path
        const base = `${import.meta.env.VITE_WS_URL}/ws/vm-console/${props.taskId}/`;
        rfb.value = new RFB(vncContainerElement, wsUrlBuilt || base, rfbOptions);

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
          // Ensure credentials are resent if requested
          if (rfb.value && (rfbOptions.credentials?.password)) {
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

        // VNC settings
        rfb.value.scaleViewport = false;
        rfb.value.resizeSession = true;
      }
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
    if (environmentStatus.value === 'active') {
        setupVNC();
    }
  }
});

onBeforeUnmount(() => {
    cleanup();
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
        await loadEnvironmentStatus();
        if (environmentStatus.value === 'active') {
            // Wait for cleanup
            setTimeout(() => {
                setupVNC();
            }, 200);
        }
    }
});
function reloadVNC(){
  cleanup();
  setupVNC();
}
</script>

<template>
  <div v-if="hasConfig" class="shell-container">
    <div v-if="taskId" class="vm-controls">
        <div class="d-flex align-center justify-space-between">
          <div class="d-flex align-center">
            <v-chip 
              :color="getStatusColor(environmentStatus)" 
              size="small" 
              class="me-3"
            >
              {{ getStatusText(environmentStatus) }}
            </v-chip>
            <v-chip
              v-if="environmentStatus === 'active' && connectionStatus === 'connected'"
              color="success"
              size="small"
              class="me-3"
            >
            Shell: {{ connectionStatus }}
            </v-chip>
            <v-btn
              v-else-if="environmentStatus === 'active' && connectionStatus === 'disconnected'"
              @click="reloadVNC"
              :loading="isInitializing"
              color="primary"
              size="small"
              variant="outlined"
            >
              <v-icon size="small" class="me-1">mdi-refresh</v-icon>
              Reconnect Shell
            </v-btn>
          </div>
          <div class="d-flex gap-2">
            <v-btn
              v-if="environmentStatus === 'not_created' || environmentStatus === 'suspended' || environmentStatus === 'provisioning'"
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
              v-if="environmentStatus === 'active' || environmentStatus === 'suspended' || environmentStatus === 'cleanup'"
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
    
    <div v-show="environmentStatus === 'active'" class="vnc-container-wrapper">
      <div 
        ref="vncContainer"
        class="vnc-wrapper"
      ></div>
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
