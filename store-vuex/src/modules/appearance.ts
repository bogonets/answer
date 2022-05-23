interface StateInterface {
  dark: boolean;
  timezone: string;
}

export default {
  namespaced: true,
  state: {
    dark: false,
    timezone: '',
  } as StateInterface,
  getters: {
    dark: (state: StateInterface) => {
      return state.dark;
    },
    timezone: (state: StateInterface) => {
      return state.timezone;
    },
  },
  mutations: {
    dark(state: StateInterface, value: boolean) {
      state.dark = value;
    },
    timezone(state: StateInterface, value: string) {
      state.timezone = value;
    },
  },
};
