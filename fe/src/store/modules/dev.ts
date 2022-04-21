export default {
  namespaced: true,
  state: {
    enable: false,
  },
  getters: {
    enable: state => {
      return state.enable;
    },
  },
  mutations: {
    enable(state, val) {
      state.enable = val;
    },
  },
};
