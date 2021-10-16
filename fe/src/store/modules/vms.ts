export default {
    namespaced: true,
    state: {
        wsd: [],
    },
    getters: {
        wsd: state => {
            return state.wsd;
        },
    },
    mutations: {
        wsd(state, val) {
            state.wsd = val || [];
        },
    },
}
