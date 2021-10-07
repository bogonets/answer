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
        userExtra: state => {
            return state.user.extra || {};
        },
        userExtraDark: state => {
            if (state.user.extra !== undefined) {
                return state.user.extra.dark || false;
            }
            return false;
        },
        userExtraLang: state => {
            if (state.user.extra !== undefined) {
                return state.user.extra.lang || '';
            }
            return '';
        },
        userExtraTimezone: state => {
            if (state.user.extra !== undefined) {
                return state.user.extra.timezone || '';
            }
            return '';
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
        userExtra(state, val) {
            state.user.extra = val;
        },
        userExtraDark(state, val) {
            if (state.user.extra === undefined) {
                state.user.extra = {};
            }
            state.user.extra.dark = val;
        },
        userExtraLang(state, val) {
            if (state.user.extra === undefined) {
                state.user.extra = {};
            }
            state.user.extra.lang = val;
        },
        userExtraTimezone(state, val) {
            if (state.user.extra === undefined) {
                state.user.extra = {};
            }
            state.user.extra.timezone = val;
        },
        preference(state, val) {
            state.preference = val;
        },
    },
}
