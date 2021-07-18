const state = {
  language: 'ko'
}

const getters = {
  getLanguage: function (state) {
    return state.language;
  }
}

const mutations = {
  setLanguage(state, lang) {
    state.language = lang;
  },
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
}
