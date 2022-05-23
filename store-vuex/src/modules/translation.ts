interface StateInterface {
  lang: string;
}

export default {
  namespaced: true,
  state: {
    lang: 'ko',
  } as StateInterface,
  getters: {
    lang: (state: StateInterface) => {
      return state.lang;
    },
  },
  mutations: {
    lang(sate: StateInterface, value: string) {
      sate.lang = value;
    },
  },
};
