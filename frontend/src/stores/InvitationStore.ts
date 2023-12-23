import { defineStore } from 'pinia'
import {ref} from 'vue'
import { makeAPIRequest } from '@/communication/APIRequests'

export enum TargetRole {
  STUDENT = "STUDENT",
  INSTRUCTOR = "INSTRUCTOR"
}

type User = {
  id: number,
  username: string | null,
  email: string,
  role: string
}

export type Invitation = {
  id?: number,
  email: string,
  target_role: TargetRole,
  target_role_display?: string,
  issuer?: User,
  expiration_date?: string
}



export const useInvitationStore = defineStore('invitation', () => {
  const allInvitations = ref<Invitation[]>()
  const myInvitations = ref<Invitation[]>()

  async function getAllInvitations() {
    const response = await makeAPIRequest('/users/invitations', 'GET', true, true)
    allInvitations.value = response.data
    return response.data
  }
  async function getMyInvitations() {
    const response = await makeAPIRequest('/users/invitations/my', 'GET', true, true)
    myInvitations.value = response.data
    return response.data
  }

  async function inviteUser(invitation: Invitation) {
    const response = await makeAPIRequest('/users/invitations', 'POST', true, true, invitation)
    return response.data
  }

  async function inviteMultipleStudents(emails: string[]) {
    const requestData = {
      emails: emails
    }
    await makeAPIRequest('/users/invitations/students/bulk', 'POST', true, true, requestData)
  }

  async function renewInvitation(id: number) {
    await makeAPIRequest(`/users/invitations/${id}/renew`, 'POST', true, true, null)
    await getAllInvitations()
    await getMyInvitations()
  }

  async function deleteInvitation(id: number) {
    await makeAPIRequest(`/users/invitations/${id}`, 'DELETE', true, true)
    await getAllInvitations()
    await getMyInvitations()
  }

  return {
    allInvitations,
    getAllInvitations,
    myInvitations,
    getMyInvitations,
    inviteUser,
    inviteMultipleStudents,
    renewInvitation,
    deleteInvitation,
  }
})