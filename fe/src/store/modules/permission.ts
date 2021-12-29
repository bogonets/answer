export default {
    namespaced: true,
    state: {
        group: '',
        project: '',
        permissions: [],
    },
    getters: {
        group: state => {
            return state.group;
        },
        project: state => {
            return state.project;
        },
        permissions: state => {
            return state.permissions;
        },
    },
    mutations: {
        group(state, val) {
            state.group = val || '';
        },
        project(state, val) {
            state.project = val || '';
        },
        permissions(state, val) {
            state.permissions = val || [];
        },
    },
}
