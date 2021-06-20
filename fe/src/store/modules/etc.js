const state = {
    open_spinner: false,
    loading_liner: false,
}

const getters = {
    getOpenSpinner: function(state) {
        return state.open_spinner;
    },
    getLoadingLiner: function(state) {
        return state.loading_liner;
    }
}

const mutations = {
    setOpenSpinner(state, { bool }) {
        state.open_spinner = bool;
    },
    setLoadingLiner: function(state, { bool }) {
        state.loading_liner = bool;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
}