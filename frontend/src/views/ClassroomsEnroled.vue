<script setup lang="ts">
import { ref } from 'vue'
import TurtlHeader from '@/components/TurtlHeader.vue'
import Footer from '@/components/Footer.vue'
const items = ref([
  {
    id: '1',
    room: 'Man in the middle',
    role: 'Attack',
    description: 'testtext',
    completed: true
  },
  {
    id: '2',
    room: 'Man in the middle',
    role: 'Defense',
    description: 'testtext',
    completed: false
  },
  { id: '3', room: 'Firewall', role: 'Attack', description: 'testtext', completed: false },
  { id: '4', room: 'Firewall', role: 'Defense', description: 'testtext', completed: false }
])
</script>

<template>
  <turtl-header></turtl-header>
  <v-main>
    <v-container fluid>
      <v-row>
        <v-col v-for="item in items" :key="item.id" cols="12" sm="6" md="3">
          <v-card
            :key="item.id"
            :title="item.room"
            :border-variant="item.completed === true ? 'success' : 'danger'"
            variant="flat"
		        color="cardColor"
          >
            <v-card-text v-if="item.role === 'Attack'">
              <v-icon icon="mdi-sword"></v-icon>
              Role: {{ item.role }}
            </v-card-text>
            <v-card-text v-else>
              <v-icon icon="mdi-shield"></v-icon>
              Role: {{ item.role }}
            </v-card-text>
            <v-card-text> Description: {{ item.description }} </v-card-text>
            <v-card-actions>
              <v-btn  variant="text" color="primary">Go to Room</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
  <Footer></Footer>
</template>

<style scoped>
.cardgroup {
  margin: auto;
  margin-top: 2%;
  width: 80%;
}
.customIcon {
  height: 20px;
  width: 20px;
}
</style>
