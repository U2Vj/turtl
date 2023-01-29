<template>
    <b-jumbotron header="TURTL" lead="The Virtual Network Security Lab" class="jumbo">
    <b-card
        align="center"
        border-variant="primary"
        header-bg-variant="primary"
        header-text-variant="white"
        class="resetPassword">
        <form v-on:submit.prevent="handleSubmit">
            <b-form-group id="input-group-password1" label="Password" label-for="input-password1">
                <b-form-input
                    id="input-password1"
                    v-model="password"
                    type="password"
                    :state="validPassword"
                    required
                    placeholder="Enter your new password"
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
            <b-button size="lg"  type="submit" variant="success" >Submit</b-button>
            <hr/>
        </form>
    </b-card>
    </b-jumbotron>
</template>

<script>
import axios from 'axios'

export default {
    data () {
        return {
            password: '',
            passwordConfirm: '',
            token: '',
            uidb64: ''
        }
    },
    methods: {
        async handleSubmit () {
            if (this.password) {
                var errorStatus
                await axios.post('http://localhost:8000/api/password-reset-complete', {
                    password: this.password,
                    uidb64: this.$route.params.uidb64,
                    token: this.$route.params.token,
                    passwordConfirm: this.passwordConfirm
                }).catch(function (error) {
                    if (error.response) {
                        errorStatus = error.response.status
                    }
                })
                if (errorStatus === 401) {
                    this.showErrorMessage()
                } else {
                    this.showSuccessMessage()
                    this.$router.push({ path: '/signin' })
                }
            }
        },
        showErrorMessage () {
            this.$bvToast.toast('Reset link is invalid', {
                title: 'Password reset failed',
                variant: 'danger',
                solid: true,
                autoHideDelay: 2000
            })
        },
        showSuccessMessage () {
            this.$bvToast.toast('You have successfully reseted your password', {
                title: 'Password Reset successfull',
                variant: 'success',
                solid: true,
                autoHideDelay: 2000
            })
        }
    },
    computed: {
        samePasswords: function () {
            return (this.validPassword && (this.password === this.passwordConfirm))
        },
        validPassword: function () {
            return this.password.length >= 8
        }

    }
}
</script>

<style scoped>
.resetPassword {
    max-width: 20rem;
    margin: 2rem auto 0 auto;
}
.jumbo {
    margin-bottom: 0;
    height: 100%;
}
</style>
