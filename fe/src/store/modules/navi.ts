export default {
  namespaced: true,
  state: {
    hide: false,
  },
  getters: {
    hide: state => {
      return state.hide;
    },
  },
  mutations: {
    hide(state, val) {
      state.hide = val;
    },
  },
};
