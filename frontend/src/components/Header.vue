<template>
    <div v-if="loggedIn">
        <b-navbar type="dark" variant="info">
            <b-navbar-brand href="#" @click="handleHome">TURTL</b-navbar-brand>
            <b-navbar-nav class="ml-auto">
            <b-nav-form>
              <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
              <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
            </b-nav-form>
            <b-nav-item-dropdown right>
              <template v-slot:button-content>
                <em>User</em>
              </template>
              <b-dropdown-item @click="handleProfile">Profile</b-dropdown-item>
              <b-dropdown-item @click="handleLogout" >Sign Out</b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-navbar>
    </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
    name: 'Header',
    computed: {
        ...mapState('auth', {
            loggedIn: state => state.status.loggedIn
        })
    },
    methods: {
        handleHome () {
            this.$router.push({ path: '/home' })
        },
        handleLogout () {
            this.logout()
            this.$router.push({ path: '/signin' })
        },
        handleProfile () {
            this.$router.push({ path: '/profile' })
        },
        ...mapActions('auth', [
            'logout'
        ])
    }
}
</script>
