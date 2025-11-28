import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeAPIRequest } from '@/communication/APIRequests'

interface EnvironmentStatus {
    status: string
    environment_id?: number
    created_at?: string
    vm_count?: number
}

interface VNCTicket {
    ticket?: string
    port?: number
}

export const useVMManagerStore = defineStore('vmManager', () => {
    const loading = ref(false)
    const error = ref<string | null>(null)

    async function startEnvironment(taskId: number): Promise<EnvironmentStatus> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/start/${taskId}/`,
                'POST',
                true,
                true
            )

            return response.data as EnvironmentStatus
        } catch (err: any) {
            error.value = err.message || 'Failed to start environment'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function stopEnvironment(taskId: number): Promise<EnvironmentStatus> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/stop/${taskId}/`,
                'POST',
                true,
                true
            )

            return response.data as EnvironmentStatus
        } catch (err: any) {
            error.value = err.message || 'Failed to stop environment'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function cleanupEnvironment(taskId: number): Promise<EnvironmentStatus> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/cleanup/${taskId}/`,
                'POST',
                true,
                true
            )

            return response.data as EnvironmentStatus
        } catch (err: any) {
            error.value = err.message || 'Failed to cleanup environment'
            throw err
        } finally {
            loading.value = false
        }
    }

    async function getEnvironmentStatus(taskId: number): Promise<EnvironmentStatus> {
        loading.value = true
        error.value = null

        try {
            const response = await makeAPIRequest(
                `/vm/status/${taskId}/`,
                'GET',
                true,
                true
            )

            return response.data
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
