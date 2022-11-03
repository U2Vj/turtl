<template>
  <b-card-group deck class="cardgroup">
    <b-card
      v-for="item in items" :key="item.id"
      :title="item.room"
      :border-variant="item.completed === true? 'success':'danger'"
    >
      <b-card-text v-if="item.role === 'Attack'">
        <img class="customIcon" alt="Sword" src="@/assets/sword.png"/>
        Role: {{item.role}}
      </b-card-text>
      <b-card-text v-else>
        <img class="customIcon" alt="Shield" src="@/assets/shield.png"/>
        Role: {{item.role}}
      </b-card-text>
      <b-card-text>
        Description: {{item.description}}
      </b-card-text>
      <b-button variant="outline-primary" @click="enterClassroom(item)">Go to Room</b-button>
    </b-card>
  </b-card-group>
</template>

<script>
import { mapActions } from 'vuex'
export default {
    data () {
        return {
            fields: ['id', 'room', 'role', 'description', 'completed', 'route'],
            items: [
                { id: '1', room: 'Man in the middle', role: 'Attack', description: 'testtext', completed: true },
                { id: '2', room: 'Man in the middle', role: 'Defense', description: 'testtext', completed: false },
                { id: '3', room: 'Firewall', role: 'Attack', description: 'testtext', completed: false },
                { id: '4', room: 'Firewall', role: 'Defense', description: 'testtext', completed: false }
            ]
        }
    },
    methods: {
        enterClassroom (item) {
            this.selectClassroom(item)
            this.$router.push({ path: 'classroom' }) // Link to routes does not work properly
        },
        ...mapActions('classroom', [
            'selectClassroom'
        ])
    }
}
</script>

<style scoped>
.cardgroup{
  margin: auto;
  margin-top: 2%;
  width: 80%;
}
.customIcon{
  height: 20px;
  width: 20px;
}
</style>
