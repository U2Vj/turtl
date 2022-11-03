<template>
    <b-jumbotron header="TURTL" lead="The Virtual Network Security Lab" class="jumbo">
    <b-card
        align="center"
        border-variant="primary"
        header-bg-variant="primary"
        header-text-variant="white"
        class="register">
        <b-form>
            <b-form-group id="input-group-username" label="Username" label-for="input-username">
                <b-form-input
                    id="input-username"
                    v-model="username"
                    type="text"
                    :state="validUsername"
                    required
                    placeholder="Enter your Username"
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-email" label="Email" label-for="input-email">
                <b-form-input
                    id="input-email"
                    v-model="email"
                    type="email"
                    :state="validEmail"
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
                    required
                    placeholder="Confirm your password"
                ></b-form-input>
            </b-form-group>
            <b-button size="lg" @click="handleRegister"  type="submit" variant="success" class="loginButton">Register</b-button>
            <hr/>
            <b-button size="sm" variant="outline-primary" @click="handleLoginRedirect">Allready have an Account? Sign In!</b-button>
        </b-form>
    </b-card>
    </b-jumbotron>
</template>

<script>
import { mapActions } from 'vuex'
export default {
    data () {
        return {
            username: '',
            email: '',
            password: '',
            passwordConfirm: ''
        }
    },
    methods: {
        async handleRegister (event) {
            const result = await this.register(this.user)
            if (result === 'Request failed with status code 400') {
                this.showErrorMessage()
            } else {
                await this.login(this.userLogin)
                this.$router.push({ path: '/home' })
            }
        },
        showErrorMessage () {
            this.$bvToast.toast('Email allready in use!', {
                title: 'Registration failed',
                variant: 'danger',
                solid: true,
                autoHideDelay: 2000
            })
        },
        validateEmail (email) {
            // eslint-disable-next-line no-useless-escape
            const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
            return re.test(String(email).toLowerCase())
        },
        validateUsername (username) {
            const re = /^[a-zA-Z0-9_-]{4,15}$/
            return re.test(String(username))
        },
        handleLoginRedirect () {
            this.$router.push({ path: '/signin' })
        },
        ...mapActions('auth', [
            'register',
            'login'
        ])
    },
    computed: {
        user: function () {
            return {
                user: {
                    username: this.username,
                    email: this.email,
                    password: this.password
                }
            }
        },
        userLogin: function () {
            return {
                user: {
                    email: this.email,
                    password: this.password
                }
            }
        },
        validEmail: function () {
            return this.validateEmail(this.email)
        },
        validUsername: function () {
            return this.validateUsername(this.username)
        },
        samePasswords: function () {
            return (this.validPassword && (this.password === this.passwordConfirm))
        },
        validPassword: function () {
            return this.password.length >= 8
        },
        validInput: function () {
            return this.validUsername && this.validEmail && this.samePasswords
        }
    }
}
</script>

<style scoped>
.register {
    max-width: 20rem;
    margin: 2rem auto 0 auto;
}
.jumbo {
    margin-bottom: 0;
    height: 100%;
}
</style>
