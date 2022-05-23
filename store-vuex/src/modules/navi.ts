interface StateInterface {
  hide: boolean;
}

export default {
  namespaced: true,
  state: {
    hide: false,
  } as StateInterface,
  getters: {
    hide: (state: StateInterface) => {
      return state.hide;
    },
  },
  mutations: {
    hide(state: StateInterface, value: boolean) {
      state.hide = value;
    },
  },
};
