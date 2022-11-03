const initialState = { current: {} }

export const classroom = {
    namespaced: true,
    state: initialState,
    actions: {
        selectClassroom ({ commit }, classroom) {
            commit('setCurrentClassroom', classroom)
        }
    },
    mutations: {
        setCurrentClassroom (state, classroom) {
            state.current = classroom
        }
    }
}
