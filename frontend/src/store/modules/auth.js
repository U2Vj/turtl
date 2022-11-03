import AuthService from '../services/auth'

// Load a saved token from localStorage.
const user = JSON.parse(localStorage.getItem('user'))

// Set the initial state
const initialState = user ? { status: { loggedIn: true, errorMsg: '' }, user } : { status: { loggedIn: false, errorMsg: '' }, user: null }

// State to handle all authentication logic.

// Export state so it can be imported inside the root state.
export const auth = {
    // Namespaced allows the state to be found as auth inside the components.
    namespaced: true,
    state: initialState,
    actions: {
        // Actions can be called from the components.
        async login ({ commit }, user) {
            return await AuthService.login(user).then(
                data => {
                    commit('loginSuccess', data.user)
                    return Promise.resolve(data)
                },
                error => {
                    commit('loginFailure', error.message)
                    return error.message
                }
            )
        },
        async update ({ commit }, user) {
            return await AuthService.update(user).then(
                data => {
                    commit('updateSuccess', data.user)
                    return Promise.resolve(user)
                },
                error => {
                    commit('updateFailure', error.message)
                    return error.message
                }
            )
        },
        logout ({ commit }) {
            AuthService.logout()
            commit('logout')
        },
        async register ({ commit }, user) {
            return await AuthService.register(user).then(
                response => {
                    commit('registerSuccess')
                    return Promise.resolve(response.data)
                },
                error => {
                    commit('registerFailure')
                    return error.message
                }
            )
        }
    },
    mutations: {
        // Mutations modify/mutate the state object.
        loginSuccess (state, user) {
            state.status.loggedIn = true
            state.status.errorMsg = ''
            state.user = user
        },
        loginFailure (state, message) {
            state.status.loggedIn = false
            state.status.errorMsg = message
            state.user = null
        },
        updateSuccess (state, user) {
            state.user = user
        },
        updateFailure (state, message) {
            state.status.errorMsg = message
        },
        logout (state) {
            state.status.loggedIn = false
            state.user = null
        },
        registerSuccess (state) {
            state.status.loggedIn = false
        },
        registerFailure (state) {
            state.status.loggedIn = false
        }
    }
}
