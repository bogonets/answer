const state = {
    layout_main_signal: false,
    login_signal: false,
}

const getters = {
    getLayoutMainSignal: function(state) {
        return state.layout_main_signal;
    },
    getLoginSignal: function(state) {
        return state.login_signal;
    }
}

const mutations = {
    setLayoutMainSignal: function(state, { bool }) {
        state.layout_main_signal = bool;
    },
    setLoginSignal: function(state, { bool }) {
        state.login_signal = bool;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
}