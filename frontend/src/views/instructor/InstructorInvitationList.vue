<script setup lang="ts">
import DefaultLayout from '@/components/layouts/DefaultLayout.vue'
import dayjs from 'dayjs'
import {ref, toRef} from 'vue'
import {useToast} from "vue-toastification"
import { useInvitationStore } from "@/stores/InvitationStore"
import {useUserStore} from "@/stores/UserStore"
import PrimaryButton from "@/components/buttons/PrimaryButton.vue"

const currentTab = ref("myInvitations")

const renewInvitationButtonDisabled = ref(false)
const deleteInvitationButtonDisabled = ref(false)
const searchMyInvitations = ref("")
const searchAllInvitations = ref("")

const userStore = useUserStore()
const invitationStore = useInvitationStore()
const toast = useToast()

const myInvitations = toRef(invitationStore, 'myInvitations')
const allInvitations = toRef(invitationStore, 'allInvitations')

invitationStore.getMyInvitations().catch((e) => toast.error(e.message))

function deleteInvitation(id: number) {
  deleteInvitationButtonDisabled.value = true
  invitationStore.deleteInvitation(id)
      .then(() => toast.info("Invitation deleted"))
      .catch((e) => toast.error(e.message))
      .finally(() => {
        deleteInvitationButtonDisabled.value = false
      })
}
function renewInvitation(id: number) {
  renewInvitationButtonDisabled.value = true
  invitationStore.renewInvitation(id)
      .then(() => toast.success("Invitation renewed"))
      .catch((e) => toast.error(e.message))
      .finally(() => {
        renewInvitationButtonDisabled.value = false
      })
}

function formatReadableDate(date: string) {
  return dayjs(date).format('DD.MM.YYYY HH:mm')
}

function isExpired(expiration_date: string): boolean {
  return dayjs().isAfter(dayjs(expiration_date))
}

</script>

<template>
  <DefaultLayout>
    <template #heading>Manage Invitations</template>
    <template #postHeadingButton>
      <PrimaryButton buttonName="Invite Users" go-to="/instructor/invitations/send"></PrimaryButton>
    </template>
    <template #default>
      <v-tabs v-model="currentTab" color="primary">
        <v-tab value="myInvitations" @click="invitationStore.getMyInvitations()">My open Invitations</v-tab>
        <v-tab value="allInvitations" @click="invitationStore.getAllInvitations()">All open Invitations</v-tab>
      </v-tabs>
      <v-window v-model="currentTab" class="mt-5">
        <v-window-item value="myInvitations">
          <v-text-field
            v-model="searchMyInvitations"
            append-icon="mdi-magnify"
            label="Search my invitations"
          ></v-text-field>
          <v-data-table
            :headers="[
              {
                title: 'Email',
                align: 'start',
                key: 'email'
              },
              {
                title: 'Target role',
                align: 'start',
                key: 'target_role_display'
              },
              {
                title: 'Expires at',
                align: 'start',
                key: 'expiration_date'
              },
              {
                title: 'Renew / Delete',
                key: 'id',
                sortable: false
              }
            ]"
            :items="myInvitations"
            :search="searchMyInvitations"
            no-data-text="Could not find any open invitations that you sent."
          >
            <template #[`item.expiration_date`]="{ item }">
              <span v-if="isExpired(item.raw.expiration_date)" style="color:red;font-weight:bold">{{ formatReadableDate(item.raw.expiration_date) }}</span>
              <span v-else>{{ formatReadableDate(item.raw.expiration_date) }}</span>
            </template>
            <template #[`item.id`]="{ item }">
              <v-btn
                icon="mdi-refresh"
                variant="text"
                @click="renewInvitation(item.columns.id)"
                :disabled="renewInvitationButtonDisabled"
              />&nbsp;
              <v-btn
                icon="mdi-trash-can-outline"
                variant="text"
                @click="deleteInvitation(item.columns.id)"
                :disabled="deleteInvitationButtonDisabled"
              />
            </template>
          </v-data-table>
        </v-window-item>
        <v-window-item value="allInvitations">
          <v-text-field
            v-model="searchAllInvitations"
            append-icon="mdi-magnify"
            label="Search all invitations"
          ></v-text-field>
          <v-data-table
            :headers="[
              {
                title: 'Email',
                align: 'start',
                key: 'email'
              },
              {
                title: 'Target role',
                align: 'start',
                key: 'target_role_display'
              },
              {
                title: 'Issued by',
                align: 'start',
                key: 'issuer.email'
              },
              {
                title: 'Expires at',
                align: 'start',
                key: 'expiration_date'
              },
              {
                title: 'Renew / Delete',
                key: 'id',
                sortable: false
              }
            ]"
            :items="allInvitations"
            :search="searchAllInvitations"
            no-data-text="Could not find any open invitations."
          >
            <template #[`item.expiration_date`]="{ item }">
              <span v-if="isExpired(item.raw.expiration_date)" style="color:red;font-weight:bold">{{ formatReadableDate(item.raw.expiration_date) }}</span>
              <span v-else>{{ formatReadableDate(item.raw.expiration_date) }}</span>
            </template>
            <template #[`item.id`]="{ item }">
              <span v-if="item.raw.issuer.id == userStore.user?.id || userStore.isAdministrator()">
                <v-btn
                  icon="mdi-refresh"
                  variant="text"
                  @click="renewInvitation(item.columns.id)"
                  :disabled="renewInvitationButtonDisabled"
                />&nbsp;
                <v-btn
                  icon="mdi-trash-can-outline"
                  variant="text"
                  @click="deleteInvitation(item.columns.id)"
                  :disabled="deleteInvitationButtonDisabled"
                />
              </span>
            </template>
          </v-data-table>
        </v-window-item>
      </v-window>
    </template>
  </DefaultLayout>
</template>
