const state = {
  dark: true
}

const getters = {
  getTheme: function (state) {
    return state.dark;
  }
}

const mutations = {
  setTheme(state, {bool}) {
    state.dark = bool;
  },
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
}
