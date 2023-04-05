<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { computed, ref } from 'vue'
import TurtlHeader from '@/components/TurtlHeader.vue'

const email = ref('')
email.value = "abc.def@hij.de"

const inputs = ref([
    {
        id: '1',
        label: 'Enter your current password'
    },
    {
        id: '2',
        label: 'Enter your new password'
    },
    {
        id: '2',
        label: 'Confirm your new password'
    }
])

const currentPassword = ref('')

</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
        <div class="divMargins">
            <h1 class="title">Profil</h1>
            <div>
                <h3 class="headlineTitle">E-Mail Adresse:</h3>
                <p>{{email}}</p>
            </div>
            <div>
                <h3 class="headlineTitle">Change your password</h3>
                <v-sheet width="30%" class="mr-auto">
                    <v-form @submit.prevent>
                        <v-text-field v-for="input in inputs"
                            :key="input.id"
                            :label="input.label"
                            v-model="currentPassword"
                            variant="solo"
                        ></v-text-field>
                        <v-btn type="submit" variant="outlined">Change Password</v-btn>
                    </v-form>
                </v-sheet>
            </div>
            <v-btn variant="outlined">Permanently Delete Account</v-btn>
        </div>
    </v-container>
  </v-main>
</template>

<style>
.divMargins {
    text-align: left;
    margin: auto;
    margin-left: 5%;
    margin-top: 2%;
}
.title {
    font-weight: bolder;
    margin-bottom: 2%;
}
.headlineTitle {
    font-weight: bolder;
    margin-top: 1%;
    margin-bottom: 1%;

}
</style>
