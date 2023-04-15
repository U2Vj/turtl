<script setup lang="ts">
import { ref } from 'vue'

const classroomName = ref('')
const selected = ref()
const selectedItemName = ref('')
const search = ref(selectedItemName)

function rowSelected() {
    //selectedItemName.value = selected.value[0].name
    if (selected.value.length === 1) {
        selectedItemName.value = selected.value[0].name
    }
    else {
        selectedItemName.value = ''
    }
}

function createClassroom() {
    //Selected Row Object in value: selected
}

const headers = [
          { title: 'Name', key: 'name' },
          { title: 'Created On', key: 'created_on' },
          { title: 'Created By', key: 'created_by' },
        ]
const classTemplates = [
    {
        name: 'Test Networks',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
        {
        name: 'Test Networks',
        created_on: '01.03.2023',
        created_by: 'Franz Mustermann',
    },
    {
        name: 'Computer Versuch',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Safe',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Sicherheit',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Labor Networks',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Computer Programm',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Meister Teil',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Birnen Kompott',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Apfelmouse',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Advanced Software Engineering',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Data Science',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Digital Story',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Theo Inf',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Mathe',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Physik',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
    {
        name: 'Algorithmen',
        created_on: '01.03.2023',
        created_by: 'Max Mustermann',
    },
]

</script>

<template>
    <div class="classroomInstanceDiv">
        <div class="inputMargins">
            <h1 class="title">Create Classroom</h1>
            <p class="namesTitle">Classroom Name</p>
            <v-text-field
                clearable
                label="Type in Classroom Name"
                v-model="classroomName"
                variant="solo"
                class="textFieldMargins"
            ></v-text-field>
            <p class="namesTitle">Classroom Template</p>
            <v-text-field
                clearable
                label="Search Classroom Template"
                v-model="selectedItemName"
                append-icon="mdi-magnify"
                variant="solo"
                class="textFieldMargins"
            ></v-text-field>
            </div>
            <div>
            <v-data-table
                @click="rowSelected()"
                :headers="headers"
                :items="classTemplates"
                :search="search"
                v-model="selected"
                item-value="classTemplates"
                show-select
            ></v-data-table>
            </div>
                <v-btn @click="createClassroom">Create Classroom</v-btn>
                <!-- <p>Selected2: {{ selected }}</p> -->
    </div>
</template>

<style>

.namesTitle {
    font-weight: bold;
    margin-bottom: 2%;
}
.title {
    font-weight: bolder;
    margin-bottom: 10%;
}
.classroomInstanceDiv {
    text-align: left;
    margin-left: 5%;
    margin-top: 2.5%;
    margin-right: 20%;
}
.inputMargins {
    margin-right: 60%;
}
.textFieldMargins {
    margin-bottom: 3%;
}
</style>