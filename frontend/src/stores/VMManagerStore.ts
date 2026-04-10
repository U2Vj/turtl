import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeAPIRequest } from '@/communication/APIRequests'

type EnvironmentStatusValue =
    | 'not_created'
    | 'provisioning'
    | 'starting'
    | 'active'
    | 'degraded'
    | 'stopping'
    | 'stopped'
    | 'cleanup'

type StartEnvironmentResponseStatus = 'created' | 'started' | 'error'
type StopEnvironmentResponseStatus = 'stopped' | 'error'
type CleanupEnvironmentResponseStatus = 'deleted' | 'error'

interface EnvironmentStatusResponse {
    status: EnvironmentStatusValue
    environment_id?: number
    created_at?: string
    vm_count?: number
}

interface StartEnvironmentResponse {
    status: StartEnvironmentResponseStatus
    message?: string
    environment_id?: number
}

interface StopEnvironmentResponse {
    status: StopEnvironmentResponseStatus
    message?: string
    detail?: string
}

interface CleanupEnvironmentResponse {
    status: CleanupEnvironmentResponseStatus
    message?: string
    detail?: string
    error_code?: string
}

interface VNCTicket {
    ticket?: string
    port?: number
}

export const useVMManagerStore = defineStore('vmManager', () => {
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function startEnvironment(taskId: number): Promise<StartEnvironmentResponse> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/start/${taskId}/`,
                'POST',
                true,
                true
            )

            return response.data as StartEnvironmentResponse
        } catch (err: any) {
            error.value = err.message || 'Failed to start environment'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function stopEnvironment(taskId: number): Promise<StopEnvironmentResponse> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/stop/${taskId}/`,
                'POST',
                true,
                true
            )

            return response.data as StopEnvironmentResponse
        } catch (err: any) {
            error.value = err.message || 'Failed to stop environment'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function cleanupEnvironment(taskId: number): Promise<CleanupEnvironmentResponse> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/cleanup/${taskId}/`,
                'POST',
                true,
                true
            )

            return response.data as CleanupEnvironmentResponse
        } catch (err: any) {
            error.value = err.message || 'Failed to cleanup environment'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function getEnvironmentStatus(taskId: number): Promise<EnvironmentStatusResponse> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/status/${taskId}/`,
                'GET',
                true,
                true
            )

            return response.data as EnvironmentStatusResponse
        } catch (err: any) {
            error.value = err.message || 'Failed to get environment status'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function hasConfig(taskId: number): Promise<boolean> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/has-config/${taskId}/`,
                'GET',
                true,
                true
            )

            return !!response.data?.has_config
        } catch (err: any) {
            error.value = err.message || 'Failed to check config'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function getVNCTicket(taskId: number): Promise<VNCTicket> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/vnc-ticket/${taskId}/`,
                'GET',
                true,
                true
            )

            return response.data as VNCTicket
        } catch (err: any) {
            error.value = err.message || 'Failed to fetch VNC ticket'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        loading,
        error,
        startEnvironment,
        stopEnvironment,
        cleanupEnvironment,
        getEnvironmentStatus,
        hasConfig,
        getVNCTicket,
    }
})
