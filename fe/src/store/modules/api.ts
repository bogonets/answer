export default {
  namespaced: true,
  state: {
    api: document.location.origin,
  },
  getters: {
    origin: state => {
      return state.api;
    },
  },
  mutations: {
    origin(state, val) {
      state.api = val;
    },
  },
};
