export default {
  namespaced: true,
  state: {
    dark: false,
    timezone: '',
  },
  getters: {
    dark: state => {
      return state.dark;
    },
    timezone: state => {
      return state.timezone;
    },
  },
  mutations: {
    dark(state, val) {
      state.dark = val;
    },
    timezone(state, val) {
      state.timezone = val;
    },
  },
};
