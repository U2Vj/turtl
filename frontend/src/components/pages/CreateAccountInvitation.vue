
<template>
  <b-container fluid>
    <b-card>
      <form v-on:submit.prevent="addInvitation">
        <b-form-group id="input-group-email" label="Email" label-for="input-email">
          <b-form-input
              id="id_email"
              v-model="email"
              type="email"
              :state="validEmail"
              required
              name="email"
              placeholder="Enter the email to send invation"
          ></b-form-input>
        </b-form-group>
        <b-button size="lg" @click="handleRegister"  type="submit" variant="success">Invite</b-button>
      </form>
    </b-card>
  </b-container>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

import axios from 'axios'

export default {

    components: {
        Navbar
    },
    data () {
        const columns = [
            { label: 'Email', name: 'email_users' }
        ]

        return {
            email: '',
            errors: [],
            users: [],
            columns: columns
        }
    },
    methods: {
        showSuccessMessage () {
            this.$bvToast.toast('Invite was succesfull', {
                title: 'Invitation was successful',
                variant: 'success',
                solid: true,
                autoHideDelay: 2000
            })
        },
        validateEmail (email) {
        // eslint-disable-next-line no-useless-escape
            const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return re.test(String(email).toLowerCase())
        },
        async addInvitation () {
            if (this.email) {
                await axios.post('http://localhost:8000/api/request-reset-email', {
                    email: this.email
                })
                this.showSuccessMessage()
            }
        },
        getUsers () {
            axios.get('http://localhost:8000/api/users/get', { params: this.tableShow })
                .then(response => {
                    this.users = response.data
                })
        }
    }
}
</script>

<style scoped>
</style>
