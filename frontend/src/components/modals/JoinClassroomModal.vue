<script setup lang="ts">
import { ref } from 'vue'
import PrimaryButton from '@/components/layouts/PrimaryButton.vue'
import TextButton from '@/components/layouts/TextButton.vue'

const showDialog = ref(false)

function close() {
  showDialog.value = false
}

function join() {
  showDialog.value = false
}
</script>
<template>
<v-dialog v-model="showDialog" activator="parent" persistent width="50%">
    <v-card>
        <v-card-title> <slot name="classroomName"></slot> </v-card-title>
        <v-card-text>
        <v-container>
            <v-row>
            <v-col>
                <p>Enter the code to join the classroom.</p>
            </v-col>
            </v-row>
            <v-row> </v-row>
            <v-row>
            <v-col cols="8">
                <v-text-field
                label="Enter Code"
                clearable
                variant="underlined"
                base-color="primary"
                color="primary"
                ></v-text-field>
            </v-col>
            </v-row>
        </v-container>
        </v-card-text>
        <v-card-actions>
        <v-spacer></v-spacer>
        <TextButton buttonName="Cancel" @atClick="close"></TextButton>
        <PrimaryButton buttonName="Join Classroom" @atClick="join"> </PrimaryButton>
        </v-card-actions>
    </v-card>
</v-dialog>
</template>