const state = {
    api: document.location.origin
}

const getters = {
    getApiUrl: (state) => {
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
