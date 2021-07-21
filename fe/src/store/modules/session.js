export default {
    namespaced: true,
    state: {
        access: '',
        refresh: '',
        user: {},
    },
    getters: {
        access: state => {
            return state.access;
        },
        refresh: state => {
            return state.refresh;
        },
        user: state => {
            return state.user;
        },
    },
    mutations: {
        access(sate, val) {
            sate.access = val;
        },
        refresh(sate, val) {
            sate.refresh = val;
        },
        user(sate, val) {
            sate.user = val;
        }
    },
}
