const state = {
  dark: true
}

const getters = {
  getTheme: function (state) {
    return state.dark;
  }
}

const mutations = {
  setTheme(state, dark) {
    state.dark = dark;
  },
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
}
