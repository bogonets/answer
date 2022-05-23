interface ExtraInterface {
  dark: boolean;
  lang: string;
  timezone: string;
}

interface UserInterface {
  extra: ExtraInterface;
}

interface StateInterface {
  access: string;
  refresh: string;
  user: UserInterface;
  preference: object;
}

export default {
  namespaced: true,
  state: {
    access: '',
    refresh: '',
    user: {
      extra: {
        dark: false,
        lang: '',
        timezone: '',
      } as ExtraInterface,
    } as UserInterface,
    preference: {},
  } as StateInterface,
  getters: {
    already: (state: StateInterface) => {
      return !!state.access && !!state.refresh && !!state.user;
    },
    access: (state: StateInterface) => {
      return state.access;
    },
    refresh: (state: StateInterface) => {
      return state.refresh;
    },
    user: (state: StateInterface) => {
      return state.user;
    },
    userExtra: (state: StateInterface) => {
      return state.user.extra || {};
    },
    userExtraDark: (state: StateInterface) => {
      if (state.user.extra !== undefined) {
        return state.user.extra.dark || false;
      }
      return false;
    },
    userExtraLang: (state: StateInterface) => {
      if (state.user.extra !== undefined) {
        return state.user.extra.lang || '';
      }
      return '';
    },
    userExtraTimezone: (state: StateInterface) => {
      if (state.user.extra !== undefined) {
        return state.user.extra.timezone || '';
      }
      return '';
    },
    preference: (state: StateInterface) => {
      return state.preference;
    },
  },
  mutations: {
    access(state: StateInterface, value: string) {
      state.access = value;
    },
    refresh(state: StateInterface, value: string) {
      state.refresh = value;
    },
    user(state: StateInterface, value: UserInterface) {
      state.user = value;
    },
    userExtra(state: StateInterface, value: ExtraInterface) {
      state.user.extra = value;
    },
    userExtraDark(state: StateInterface, value: boolean) {
      state.user.extra.dark = value;
    },
    userExtraLang(state: StateInterface, value: string) {
      state.user.extra.lang = value;
    },
    userExtraTimezone(state: StateInterface, value: string) {
      state.user.extra.timezone = value;
    },
    preference(state: StateInterface, value: object) {
      state.preference = value;
    },
  },
};
