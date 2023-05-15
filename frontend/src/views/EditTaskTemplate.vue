<script setup lang="ts">
import { ref } from 'vue'
import TurtlHeader from '@/components/TurtlHeader.vue'
import Footer from '@/components/Footer.vue'
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
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col justify="space-between">
          <v-row>
            <v-col cols="auto">
              <h1>{{ taskName }}</h1>
              <v-text-field
                v-if="onlyRead === false"
                prepend-inner-icon="mdi-pencil"
                type="edit"
                v-model="taskName"
              >
              </v-text-field>
            </v-col>
            <v-col cols="auto">
              <v-btn @click="toggleEdit">{{ editLabel }}</v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <h2>Task Description</h2>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-textarea
                clearable
                label="Write here the description"
                v-model="taskDescription"
              ></v-textarea>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <h2>Acceptance Criteria</h2>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-list>
                <v-list-item v-for="item in allCriteria" :key="item.id">
                  <v-card :key="item.id" variant="outlined">
                    <v-table density="compact">
                      <tbody>
                        <tr>
                          <td width="2%">{{ item.id }}</td>
                          <td width="5%">{{ item.type }}</td>
                          <td width="40%">{{ item.description }}</td>
                          <td width="7%"><v-btn variant="text">Edit</v-btn></td>
                          <td width="10%">Move Up</td>
                          <td width="10%">Move Down</td>
                        </tr>
                      </tbody>
                    </v-table>
                  </v-card>
                </v-list-item>
              </v-list>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn variant="outlined">+ Add new acceptance criterium</v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <h2>Virtualizations</h2>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12">
              <v-list>
                <v-list-item v-for="item in allVirtual" :key="item.id">
                  <v-card :key="item.id" variant="outlined">
                    <v-table density="compact">
                      <tbody>
                        <tr>
                          <td width="21%">{{ item.type }}</td>
                          <td width="40%">{{ item.title }}</td>
                          <td width="40%">{{ item.accesable }}</td>
                          <td width="20%"><v-btn variant="text">Edit</v-btn></td>
                        </tr>
                      </tbody>
                    </v-table>
                  </v-card>
                </v-list-item>
              </v-list>
            </v-col>
            <v-col>
              <v-btn variant="outlined">+ Add new virtualization</v-btn>
            </v-col>
          </v-row>
        </v-col>
        <v-col sm="8" md="4" offset="1" justify="space-between">
          <v-col>
            <v-card variant="outlined">
              <v-card-item>
                <v-card-title><h3>Information</h3></v-card-title>
              </v-card-item>
              <v-card-text>
                <v-table density="compact">
                  <tbody>
                    <tr>
                      <td>Created On:</td>
                      <td>{{ createdOn }}</td>
                    </tr>
                    <tr>
                      <td>Created By:</td>
                      <td>{{ createdBy }}</td>
                    </tr>
                    <tr>
                      <td>Last modified on:</td>
                      <td>{{ modifiedOn }}</td>
                    </tr>
                    <tr>
                      <td>Last modified by:</td>
                      <td>{{ modifiedBy }}</td>
                    </tr>
                  </tbody>
                </v-table>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col>
            <v-card variant="outlined">
              <v-card-item>
                <v-card-title><h3>Export</h3></v-card-title>
              </v-card-item>
              <v-card-actions>
                <v-btn variant="outlined">Export Task Template</v-btn>
              </v-card-actions></v-card
            >
          </v-col>
          <v-col>
            <v-card variant="outlined">
              <v-card-item>
                <v-card-title><h3>Deletion</h3></v-card-title>
              </v-card-item>
              <v-card-actions>
                <v-btn text variant="outlined">Permanently Delete<br />Task Template</v-btn>
              </v-card-actions></v-card
            >
          </v-col>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
  <Footer></Footer>
</template>

<style></style>
