const state = {
  language: "ko"
}

const getters = {
  getLanguage: function (state) {
    return state.language;
  }
}

const mutations = {
  setLanguage(state, { language }) {
    state.language = language;
  },
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
}
