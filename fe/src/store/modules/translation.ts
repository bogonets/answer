export default {
  namespaced: true,
  state: {
    lang: 'ko',
  },
  getters: {
    lang: state => {
      return state.lang;
    },
  },
  mutations: {
    lang(sate, val) {
      sate.lang = val;
    },
  },
};
