const state = {
    api: document.location.origin
}

const getters = {
    getApiUrl: function(state) {
        return state.api;
    }
}

const mutations = {
    setApiUrl(state, url) {
        state.api = url;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
}