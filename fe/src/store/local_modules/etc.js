const state = {
    api_url: "http://127.0.0.1:20001"
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