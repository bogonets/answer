export default {
  namespaced: true,
  state: {
    hide: false,
    navi: false,
  },
  getters: {
    hide: state => {
      return state.hide;
    },
    navi: state => {
      return state.navi;
    },
  },
  mutations: {
    hide(state, val) {
      state.hide = val;
    },
    navi(state, val) {
      state.navi = val;
    },
  },
};
