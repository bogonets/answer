interface StateInterface {
  enable: boolean;
}

export default {
  namespaced: true,
  state: {
    enable: false,
  } as StateInterface,
  getters: {
    enable: (state: StateInterface) => {
      return state.enable;
    },
  },
  mutations: {
    enable(state: StateInterface, value: boolean) {
      state.enable = value;
    },
  },
};
