import Vue from 'vue'
import Vuex from 'vuex'

import { auth } from './modules/auth'
import { classroom } from './modules/classroom'

Vue.use(Vuex)

// This file is the root of the Vuex state.
// The sub-states auth and classroom get included.

export default new Vuex.Store({
    state: {},
    mutations: {},
    actions: {},
    modules: {
        auth,
        classroom
    }
})
