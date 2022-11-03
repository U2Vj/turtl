import axios from 'axios'

const API_URL = 'http://localhost:8000/api/'

// This service handle the all authentication logic.

class AuthService {
    async login (user) {
        return await axios
            .post(API_URL + 'users/login', user)
            .then(
                response => {
                    if (response.data.user.token) {
                        localStorage.setItem('user', JSON.stringify(response.data.user))
                    }

                    return response.data
                }
            )
    }

    async update (user) {
        return await axios
            .post(API_URL + 'user', user)
            .then(
                response => {
                    if (response.data.user.token) {
                        localStorage.setItem('user', JSON.stringify(response.data.user))
                    }

                    return response.data
                }
            )
    }

    logout () {
        localStorage.removeItem('user')
    }

    async register (user) {
        return await axios.post(API_URL + 'users/register', user)
    }
}

// This method can be called to add an authentication header with the token to an request.
// This need to happen for all calls which need the token, like all docker calls.
export function authHeader () {
    const user = JSON.parse(localStorage.getItem('user'))

    if (user && user.token) {
        return { Authorization: 'Bearer ' + user.token }
    } else {
        return {}
    }
}

export default new AuthService()
