<script setup lang="ts">
import { useUserStore } from '@/stores/UserStore'
import { computed, ref } from 'vue'
import TurtlHeader from '@/components/TurtlHeader.vue'

const email = ref('')
email.value = "abc.def@hij.de"

const inputs = ref([
    {
        id: '1',
        label: 'Enter your current password',
        password: ''
    },
    {
        id: '2',
        label: 'Enter your new password',
        password: ''
    },
    {
        id: '2',
        label: 'Confirm your new password',
        password: ''
    }
])


</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
        <v-row>
            <v-col cols="12">
            </v-col>
            <v-col cols="12" sm="8" md="4" offset="1">
                <h1 class="title">Profil</h1>
            </v-col>
        </v-row>
        <v-row no-gutters>
            <v-col cols="12" offset="1">
                <h3 class="headlineTitle">E-Mail Adresse:</h3>
            </v-col>
            <v-col offset="1">
                <p>{{email}}</p>
            </v-col>
        </v-row>
        <v-row no-gutters>
            <v-col cols="12" offset="1">
                <h3 class="headlineTitle">Change your password</h3>
            </v-col>
            <v-col cols="12" sm="8" md="4" offset="1">
                <v-sheet class="mr-auto">
                <v-form @submit.prevent>
                    <v-text-field v-for="input in inputs"
                        :key="input.id"
                        :label="input.label"
                        v-model="input.password"
                        variant="solo"
                    ></v-text-field>
                    <v-btn type="submit" variant="outlined">Change Password</v-btn>
                </v-form>
            </v-sheet>
            </v-col>
        </v-row>
        <v-row justify="end">
            <v-col cols="12" sm="6" md="3" offset="1">
                <v-btn variant="outlined">Permanently Delete Account</v-btn>
            </v-col>
        </v-row>
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
