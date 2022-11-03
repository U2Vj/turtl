<template>
    <b-card
        header="Profile"
        align="center"
        border-variant="primary"
        header-bg-variant="primary"
        header-text-variant="white"
        class="profile">
        <b-avatar :text="initials" size="9rem"></b-avatar>
        <b-form>
            <b-form-group id="input-group-username" label="Username" label-for="input-username">
                <b-form-input
                    id="input-username"
                    v-model="user.username"
                    type="text"
                    :state="validUsername"
                    :disabled="locked"
                    required
                    placeholder="Enter your Username"
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-email" label="Email" label-for="input-email">
                <b-form-input
                    id="input-email"
                    v-model="user.email"
                    type="email"
                    :state="validEmail"
                    :disabled="locked"
                    required
                    placeholder="Enter your email"
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-password1" label="Password" label-for="input-password1">
                <b-form-input
                    id="input-password1"
                    v-model="password"
                    type="password"
                    :state="validPassword"
                    :disabled="locked"
                    required
                    placeholder="Enter your password"
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-password2" label-for="input-password2">
                <b-form-input
                    id="input-password2"
                    v-model="passwordConfirm"
                    type="password"
                    :state="samePasswords"
                    :disabled="locked"
                    required
                    placeholder="Confirm your password"
                ></b-form-input>
            </b-form-group>
        </b-form>
        <b-button v-if="locked" size="lg" @click="toggleForm"  type="submit" variant="primary" class="updateButton">Edit</b-button>
        <b-button v-if="!locked" size="lg" :disabled="!validInput" @click="handleUpdate"  type="submit" variant="success" class="updateButton">Save</b-button>
    </b-card>
</template>

<script>
import { mapActions, mapState } from 'vuex'

export default {
    name: 'Profile',
    data () {
        return {
            locked: true,
            password: '',
            passwordConfirm: ''
        }
    },
    computed: {
        initials: function () {
            return this.user.username.substring(0, 2).toUpperCase()
        },
        validEmail: function () {
            return this.validateEmail(this.user.email)
        },
        validUsername: function () {
            return this.validateUsername(this.user.username)
        },
        samePasswords: function () {
            return (this.validPassword && (this.password === this.passwordConfirm))
        },
        validPassword: function () {
            return this.password.length >= 8
        },
        validInput: function () {
            return this.validUsername && this.validEmail && this.samePasswords
        },
        userData: function () {
            return {
                user: {
                    username: this.user.username,
                    email: this.user.email,
                    password: this.password
                }
            }
        },
        ...mapState('auth', {
            loggedIn: state => state.status.loggedIn,
            user: state => state.user
        })
    },
    methods: {
        toggleForm () {
            this.locked = !this.locked
        },
        async handleUpdate () {
            await this.update(this.userData)
            this.toggleForm()
        },
        validateEmail (email) {
            // eslint-disable-next-line no-useless-escape
            const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return re.test(String(email).toLowerCase())
        },
        validateUsername (username) {
            const re = /^[a-z0-9_-]{4,15}$/
            return re.test(String(username))
        },
        ...mapActions('auth', [
            'update'
        ])
    }
}
</script>
<style scoped>
.profile {
    max-width: 20rem;
    margin: 2rem auto 0 auto;
}
</style>
