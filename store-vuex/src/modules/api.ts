interface StateInterface {
  origin: string;
}

export default {
  namespaced: true,
  state: {
    origin: document.location.origin,
  } as StateInterface,
  getters: {
    origin: (state: StateInterface) => {
      return state.origin;
    },
  },
  mutations: {
    origin(state: StateInterface, value: string) {
      state.origin = value;
    },
  },
};
