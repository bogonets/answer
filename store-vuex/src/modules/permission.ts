interface StateInterface {
  group: string;
  project: string;
  permissions: Array<string>;
}

export default {
  namespaced: true,
  state: {
    group: '',
    project: '',
    permissions: [],
  } as StateInterface,
  getters: {
    group: (state: StateInterface) => {
      return state.group;
    },
    project: (state: StateInterface) => {
      return state.project;
    },
    permissions: (state: StateInterface) => {
      return state.permissions;
    },
  },
  mutations: {
    group(state: StateInterface, value: string) {
      state.group = value || '';
    },
    project(state: StateInterface, value: string) {
      state.project = value || '';
    },
    permissions(state: StateInterface, value: Array<string>) {
      state.permissions = value || [];
    },
  },
};
