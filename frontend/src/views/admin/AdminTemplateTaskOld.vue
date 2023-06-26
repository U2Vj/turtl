<script setup lang="ts">
import { ref } from 'vue'
import HeaderTurtl from '@/components/HeaderTurtl.vue'
import FooterTurtl from '@/components/FooterTurtl.vue'
const taskName = ref('What are IP Adresses?')
const onlyRead = ref(true)
const editLabel = ref('Edit')
const taskDescription = ref(
  'Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.  Stet clita kasd gubergren, no sea takimata sanctus est.'
)
const createdOn = ref('2022.02.02')
const createdBy = ref('Max Muster')
const modifiedOn = ref('2022.02.02')
const modifiedBy = ref('Franz Muster')

const allCriteria = [
  { id: '1', type: 'Question', description: 'How many bytes does an IPv4 address consist of?' },
  { id: '2', type: 'Question', description: 'How ?' },
  { id: '3', type: 'Question', description: 'How many bytes does an IPv4 address consist of?' }
]

const allVirtual = [
  { id: '1', type: 'Docker Container', title: 'kalilinux/kali-rolling', accesable: 'User Shell' },
  { id: '2', type: 'Docker Container', title: 'ubuntu', accesable: 'User-accessible via IP' }
]

function toggleEdit() {
  if (onlyRead.value === true) {
    onlyRead.value = false
    editLabel.value = 'Safe'
  } else if (onlyRead.value === false) {
    onlyRead.value = true
    editLabel.value = 'Edit'
  }
}
</script>

<template>
  <HeaderTurtl />
  <v-main>
    <v-container fluid>
      <v-row justify="space-between">
        <v-col cols="12" sm="8" md="5">
          <div>
            <h1>{{ taskName }}</h1>
            <v-text-field
              v-if="onlyRead === false"
              prepend-inner-icon="mdi-pencil"
              type="edit"
              v-model="taskName"
              clearable
              variant="underlined"
              base-color="primary"
              color="primary"
            >
            </v-text-field>
            <v-btn variant="tonal" color="primary" @click="toggleEdit">{{ editLabel }}</v-btn>
          </div>
          <div class="mt-5">
            <h2>Task Description</h2>
          </div>
          <div>
            <v-textarea
              clearable
              label="Write here the description"
              v-model="taskDescription"
              variant="underlined"
              base-color="primary"
              color="primary"
            ></v-textarea>
          </div>
          <div>
            <h2>Acceptance Criteria</h2>
          </div>
          <div>
            <v-list>
              <v-list-item v-for="item in allCriteria" :key="item.id">
                <v-card :key="item.id" variant="flat" color="cardColor">
                  <v-table density="compact">
                    <tbody>
                      <tr>
                        <td width="2%">{{ item.id }}</td>
                        <td width="5%">{{ item.type }}</td>
                        <td width="40%">{{ item.description }}</td>
                        <td width="7%"><v-btn variant="text" color="primary">Edit</v-btn></td>
                      </tr>
                    </tbody>
                  </v-table>
                </v-card>
              </v-list-item>
            </v-list>
          </div>
          <div>
            <v-btn variant="tonal" color="primary" class="elevation-2"
              >Add new acceptance criterium</v-btn
            >
          </div>
          <div class="mt-5">
            <h2>Virtualizations</h2>
          </div>
          <div>
            <v-list>
              <v-list-item v-for="item in allVirtual" :key="item.id">
                <v-card :key="item.id" variant="flat" color="cardColor">
                  <v-table density="compact">
                    <tbody>
                      <tr>
                        <td width="21%">{{ item.type }}</td>
                        <td width="40%">{{ item.title }}</td>
                        <td width="40%">{{ item.accesable }}</td>
                        <td width="20%"><v-btn variant="text" color="primary">Edit</v-btn></td>
                      </tr>
                    </tbody>
                  </v-table>
                </v-card>
              </v-list-item>
            </v-list>
          </div>
          <div>
            <v-btn variant="tonal" color="primary" class="elevation-2"
              >Add new virtualization</v-btn
            >
          </div>
        </v-col>

        <v-col cols="12" sm="8" md="3">
          <div>
            <v-card variant="flat" color="cardColor" class="elevation-4">
              <v-card-item>
                <v-card-title><h3>Information</h3></v-card-title>
              </v-card-item>
              <v-card-text>
                <div><h3>Created On:</h3></div>
                <div>{{ createdOn }}</div>
                <div class="mt-5"><h3>Created By:</h3></div>
                <div>{{ createdBy }}</div>
                <div class="mt-5"><h3>Last modified on:</h3></div>
                <div>{{ modifiedOn }}</div>
                <div class="mt-5"><h3>Last modified by:</h3></div>
                <div>{{ modifiedBy }}</div>
              </v-card-text>
            </v-card>
          </div>
          <div class="mt-5">
            <v-card variant="flat" color="cardColor" class="elevation-4">
              <v-card-item>
                <v-card-title><h3>Deletion</h3></v-card-title>
              </v-card-item>
              <v-card-actions>
                <v-btn variant="tonal" color="error" class="elevation-2"
                  >Permanently Delete<br />Task Template</v-btn
                >
              </v-card-actions></v-card
            >
          </div>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
  <FooterTurtl />
</template>

<style></style>
