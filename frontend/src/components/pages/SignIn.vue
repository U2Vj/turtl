<template>
    <b-jumbotron header="TURTL" lead="The Virtual Network Security Lab" class="jumbo">
    <b-card
        align="center"
        border-variant="primary"
        header-bg-variant="primary"
        header-text-variant="white"
        class="signin">
        <b-form>
            <b-form-group id="input-group-email" label="Email" label-for="input-email">
                <b-form-input
                    id="input-email"
                    v-model="email"
                    type="email"
                    :state="validEmail"
                    required
                    placeholder="Enter name/email"
                ></b-form-input>
            </b-form-group>
            <b-form-group id="input-group-name" label="Password" label-for="input-name">
                <b-form-input
                    id="input-name"
                    v-model="password"
                    type="password"
                    required
                    placeholder="Enter password"
                ></b-form-input>
            </b-form-group>
            <b-button size="lg" :disabled="!validInput" @click="handleLogin"  type="submit" variant="success" class="loginButton">Sign In</b-button>
            <hr/>
            <b-button size="sm" variant="outline-primary" @click="handleRegisterRedirect">New to TURTL? Register here!</b-button>
        </b-form>
    </b-card>
    </b-jumbotron>
</template>

<script>
import { mapActions } from 'vuex'
export default {
    data () {
        return {
            email: '',
            password: ''
        }
    },
    methods: {
        async handleLogin (event) {
            const result = await this.login(this.user)
            if (result === 'Request failed with status code 400') {
                this.showErrorMessage()
            } else {
                this.showLoginMessage()
                this.$router.push({ path: '/home' })
            }
        },
        showErrorMessage () {
            this.$bvToast.toast('E-Mail or Password incorrect!', {
                title: 'Login Failed',
                variant: 'danger',
                solid: true,
                autoHideDelay: 2000
            })
        },
        showLoginMessage () {
            this.$bvToast.toast('Welcome to TURTL!', {
                title: 'Signin successful',
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
        handleRegisterRedirect () {
            this.$router.push({ path: '/register' })
        },
        ...mapActions('auth', [
            'login'
        ])
    },
    computed: {
        user: function () {
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
        validPassword: function () {
            return this.password.length >= 8
        },
        validInput: function () {
            return this.validEmail && this.validPassword
        }
    }
}
</script>

<style scoped>
.signin {
    max-width: 20rem;
    margin: 2rem auto 0 auto;
}
.jumbo {
    margin-bottom: 0;
    height: 100%;
}
</style>
