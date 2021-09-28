export default {
    namespaced: true,
    state: {
        group: '',
        project: '',
        features: [],
        extra: {},
        layout: {read: false, write: false},
        storage: {read: false, write: false},
        manager: {read: false, write: false},
        graph: {read: false, write: false},
        member: {read: false, write: false},
        setting: {read: false, write: false},
    },
    getters: {
        group: state => {
            return state.group;
        },
        project: state => {
            return state.project;
        },
        features: state => {
            return state.features;
        },
        extra: state => {
            return state.extra;
        },
        layoutRead: state => {
            return state.layout.read;
        },
        layoutWrite: state => {
            return state.layout.write;
        },
        storageRead: state => {
            return state.storage.read;
        },
        storageWrite: state => {
            return state.storage.write;
        },
        managerRead: state => {
            return state.manager.read;
        },
        managerWrite: state => {
            return state.manager.write;
        },
        graphRead: state => {
            return state.graph.read;
        },
        graphWrite: state => {
            return state.graph.write;
        },
        memberRead: state => {
            return state.member.read;
        },
        memberWrite: state => {
            return state.member.write;
        },
        settingRead: state => {
            return state.setting.read;
        },
        settingWrite: state => {
            return state.setting.write;
        },
    },
    mutations: {
        group(state, val) {
            state.group = val || '';
        },
        project(state, val) {
            state.project = val || '';
        },
        features(state, val) {
            state.features = val || [];
        },
        extra(state, val) {
            state.extra = val || {};
        },
        layoutRead(state, val) {
            state.layout.read = !!val;
        },
        layoutWrite(state, val) {
            state.layout.write = !!val;
        },
        storageRead(state, val) {
            state.storage.read = !!val;
        },
        storageWrite(state, val) {
            state.storage.write = !!val;
        },
        managerRead(state, val) {
            state.manager.read = !!val;
        },
        managerWrite(state, val) {
            state.manager.write = !!val;
        },
        graphRead(state, val) {
            state.graph.read = !!val;
        },
        graphWrite(state, val) {
            state.graph.write = !!val;
        },
        memberRead(state, val) {
            state.member.read = !!val;
        },
        memberWrite(state, val) {
            state.member.write = !!val;
        },
        settingRead(state, val) {
            state.setting.read = !!val;
        },
        settingWrite(state, val) {
            state.setting.write = !!val;
        },
    },
}
