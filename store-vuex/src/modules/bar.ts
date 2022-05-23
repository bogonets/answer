interface StateInterface {
  hide: boolean;
  navi: boolean;
}

export default {
  namespaced: true,
  state: {
    hide: false,
    navi: false,
  } as StateInterface,
  getters: {
    hide: (state: StateInterface) => {
      return state.hide;
    },
    navi: (state: StateInterface) => {
      return state.navi;
    },
  },
  mutations: {
    hide(state: StateInterface, value: boolean) {
      state.hide = value;
    },
    navi(state: StateInterface, value: boolean) {
      state.navi = value;
    },
  },
};
