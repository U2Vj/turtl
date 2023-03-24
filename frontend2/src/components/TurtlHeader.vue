<script setup lang="ts">
/* export default {
  name: 'Header',
  computed: {
    ...mapState('auth', {
      loggedIn: (state) => state.status.loggedIn
    })
  },
  methods: {
    handleHome() {
      this.$router.push({ path: '/home' })
    },
    handleLogout() {
      this.logout()
      this.$router.push({ path: '/signin' })
    },
    handleProfile() {
      this.$router.push({ path: '/profile' })
    },
    ...mapActions('auth', ['logout'])
  }
} */
</script>

<template>
  <div>
    <v-app-bar sticky>
      <div class="flex-grow-1">
        <v-btn to="/dashboard">Dashboard</v-btn>
        <v-btn to="/classrooms">Classrooms</v-btn>
      </div>
      <template v-slot:prepend>
        <router-link to="/">
          <v-img src="@/assets/logo.svg" width="75px"></v-img>
        </router-link>
      </template>

      <template v-slot:append>
        <v-menu activator="parent">
          <template v-slot:activator="{ props }">
            <v-btn icon="mdi-dots-vertical" v-bind="props"> </v-btn>
          </template>
          <v-list>
            <v-list-item to="/profile">
              <template v-slot:prepend>
                <v-icon icon="mdi-account"></v-icon>
              </template>
              <v-list-item-title>Profile</v-list-item-title>
            </v-list-item>
            <v-list-item>
              <template v-slot:prepend>
                <v-icon icon="mdi-logout"></v-icon>
              </template>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>
  </div>

  <!--   <v-app-bar>
      <v-navbar-brand href="#">TURTL</v-navbar-brand>
      <v-navbar-nav class="ml-auto">
        <v-nav-form>
          <v-form-input size="sm" class="mr-sm-2" placeholder="Search"></v-form-input>
          <v-button size="sm" class="my-2 my-sm-0" type="submit">Search</v-button>
        </v-nav-form>
        <v-nav-item-dropdown right>
          <template v-slot:button-content>
            <em>User</em>
          </template>
          <v-dropdown-item>Profile</v-dropdown-item>
          <v-dropdown-item>Sign Out</v-dropdown-item>
        </v-nav-item-dropdown>
      </v-navbar-nav>
    </v-app-bar>
  <v-app-bar :elevation="2">
    <v-app-bar-nav-icon></v-app-bar-nav-icon>
    <template v-slot:append>
      <v-btn icon="mdi-heart"></v-btn>

      <v-btn icon="mdi-magnify"></v-btn>

      <v-btn icon="mdi-dots-vertical"></v-btn>
    </template>
  </v-app-bar> -->
</template>
