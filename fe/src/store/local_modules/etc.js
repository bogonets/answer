const state = {
    api_url: document.location.origin
}

const getters = {
    getApiUrl: function(state) {
        return state.api_url;
    }
}

const mutations = {
    setApiUrl(state, { url }) {
        state.api_url = url;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
}