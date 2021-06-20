const state = {
  accessToken: null,
  refreshToken: null,
  id: null,
  eamil: null,
  phone: null,
}

const getters = {
  getAccessToken: function (state) {
    return state.accessToken;
  },
  getRefreshToken: function (state) {
    return state.refreshToken;
  },
  getUserID: function (state) {
    return state.id;
  },
  getUserEmail: function (state) {
    return state.email;
  },
  getUserPhone: function (state) {
    return state.phone;
  },
}

const mutations = {
  login(state, {accessToken, refreshToken, id, email, phone}) {
    state.accessToken = accessToken;
    state.refreshToken = refreshToken;
    state.id = id;
    state.email = email;
    state.phone = phone;
  },
  logout(state) {
    state.accessToken = null;
    state.refreshToken = null;
    state.id    = null;
    state.email = null;
    state.phone = null;
  },
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
}
