export default {
  namespaced: true,
  state: {
    access: '',
    refresh: '',
    user: {},
    preference: {},
  },
  getters: {
    already: state => {
      return !!state.access && !!state.refresh && !!state.user;
    },
    access: state => {
      return state.access;
    },
    refresh: state => {
      return state.refresh;
    },
    user: state => {
      return state.user;
    },
    userDark: state => {
      return state.user.dark || false;
    },
    userLang: state => {
      return state.user.lang || '';
    },
    userTimezone: state => {
      return state.user.timezone || '';
    },
    preference: state => {
      return state.preference;
    },
  },
  mutations: {
    access(state, val) {
      state.access = val;
    },
    refresh(state, val) {
      state.refresh = val;
    },
    user(state, val) {
      state.user = val;
    },
    userDark(state, val) {
      state.user.dark = val;
    },
    userLang(state, val) {
      state.user.lang = val;
    },
    userTimezone(state, val) {
      state.user.timezone = val;
    },
    preference(state, val) {
      state.preference = val;
    },
  },
};
