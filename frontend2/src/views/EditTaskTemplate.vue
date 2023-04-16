<script setup lang="ts">
import { ref } from 'vue'
import TurtlHeader from '@/components/TurtlHeader.vue'
import { boolean } from 'yup';
const taskName = ref('What are IP Adresses?')
const onlyRead = ref(true)
const editLabel = ref('Edit')
const taskDescription = ref('Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.  Stet clita kasd gubergren, no sea takimata sanctus est.')

function toggleEdit() {
    if (onlyRead.value === true) {
        onlyRead.value = false
        editLabel.value = 'Exit'
    }
    else if (onlyRead.value === false) {
        onlyRead.value = true
        editLabel.value = 'Edit'
    }
}

</script>

<template>
    <turtl-header></turtl-header>
    <v-main>
        <v-container fluid>
            <v-row>
                <v-col>
                    <v-row no-gutters>
                        <v-col cols="3">
                            <h1>{{ taskName }}</h1>
                            <v-text-field v-if="onlyRead===false" prepend-inner-icon="mdi-pencil" type="edit" v-model="taskName">
                            </v-text-field>
                        </v-col>
                        <v-col cols="3">
                            <v-btn @click="toggleEdit">{{ editLabel }}</v-btn>
                        </v-col>
                    </v-row>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <h2>Task Description</h2>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="5">
                <v-textarea clearable label="Write here the description" v-model="taskDescription"></v-textarea>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <h2>Acceptance Criteria</h2>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <h2>Virtualizations</h2>
                </v-col>
            </v-row>
        </v-container>
    </v-main>
</template>

<style>
</style>