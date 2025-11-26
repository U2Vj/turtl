import { defineStore } from 'pinia'
import { ref } from 'vue'
import { makeAPIRequest } from '@/communication/APIRequests'

interface EnvironmentStatus {
  status: string
  environment_id?: number
  created_at?: string
  vm_count?: number
}

export const useVMManagerStore = defineStore('vmManager', () =>{
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

            if (response.statusCode >=400){
                throw new Error(response.data.message || 'Failed to start environment')
            }
            return response.data as EnvironmentStatus
        } catch (err: any){
            error.value = err.message || 'Failed to start environment'
            throw err
        } finally{
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

            if (response.statusCode >= 400){
                throw new Error(response.data.message || 'Failed to stop environment')
            }
            return response.data as EnvironmentStatus
        }catch (err: any){
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
            
            if (response.statusCode >= 400) {
                throw new Error(response.data.message || 'Failed to cleanup environment')
            }
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
            
            if (response.statusCode >= 400) {
                throw new Error(response.data.message || 'Failed to get environment status')
            }
            
            return response.data
        } catch (err: any) {
            error.value = err.message || 'Failed to get environment status'
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
        getEnvironmentStatus
    }
})
