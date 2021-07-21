export default {
    namespaced: true,
    state: {
        dark: false,
    },
    getters: {
        dark: state => {
            return state.dark;
        },
    },
    mutations: {
        dark(state, val) {
            state.dark = val;
        }
    },
}
