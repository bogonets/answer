const state = {
    dash_active: false,
    dash_save: true,
    dash_infos: null,
    default_panel: { x: 0, y: 0, w: 300, h: 300, before: null, component: null },
    panels: Array()
}

const getters = {
    getDefaultPanel: function(state) {
        var newDefaultPanel = JSON.parse(JSON.stringify(state.default_panel));
        var uid = Math.random() + Math.random();
        newDefaultPanel.id = uid;
        return newDefaultPanel;
    },
    getDashActive: function(state) {
        return state.dash_active;
    },
    getDashSave: function(state) {
        return state.dash_save;
    },
    getDashInfos: function(state) {
        return state.dash_infos;
    },
    getDashInfo: function(state, { index }) {
        return state.dash_infos[index];
    },
    getPanels: function(state) {
        return state.panels;
    }
}

const mutations = {
    setDashActive: function(state, { bool }) {
        state.dash_active = bool;
    },
    setDashSave: function(state, { bool }) {
        state.dash_save = bool;
    },
    setDashInfos: function(state, { datas }) {
        state.dash_infos = datas;
    },
    setDashInfo: function(state, { mainIndex, panelIndex, data }) {
        state.dash_infos[mainIndex].panels[panelIndex].x = data.x;
        state.dash_infos[mainIndex].panels[panelIndex].y = data.y;
        state.dash_infos[mainIndex].panels[panelIndex].w = data.w;
        state.dash_infos[mainIndex].panels[panelIndex].h = data.h;
    },
    // insertComponent: function (state, {mainIndex, panelIndex, component}) {
    //   state.dash_infos[mainIndex].panels[panelIndex].component = component;
    // },
    insertComponent: function(state, { index, component }) {
        state.panels[index].component = component;
    },
    insertLayout: function(state, { name, panels_num }) {
        var index = 0;
        var panels = [];
        var default_panel = state.default_panel;
        for (index; index < panels_num; ++index) {
            // let object = null;
            // object = { x: default_panel.x, y: 0, w: 150, h: 150, component: null };
            panels.push({
                x: default_panel.x,
                y: 0,
                w: 150,
                h: 150,
                component: null
            });
        }
        state.dash_infos.push({ name: name, panels: panels });
    },
    addPanel: function(state, { z }) {
        var newDefaultPanel = JSON.parse(JSON.stringify(state.default_panel));
        var uid = "" + Math.random() + "" + Math.random();
        newDefaultPanel.id = uid;
        newDefaultPanel.z = z;
        state.panels.push(newDefaultPanel);
    },
    deletePanel: function(state, { index }) {
        state.panels.splice(index, 1);
        state.panels = [...state.panels];
        // var copy = state.panels.slice();
        // copy.splice(index, 1);
        // this.setPanels(state, { panels: copy });
    },
    deleteAllPanels: function (state) {
        state.panels = [];
    },
    setPanels: function(state, { panels }) {
        state.panels = panels;
    },
    fullScreenPanel: function (state, {index, beforePanel, afterPanel}) {
        if (!beforePanel) {
            console.warn("[STORE::DASHBOARD::fullScreenPanel] [WARN] Not found before panel data.");
            return;
        }
        var before = JSON.parse(JSON.stringify(beforePanel));
        state.panels[index].before = {};
        state.panels[index].before.x = before.x;
        state.panels[index].before.y = before.y;
        state.panels[index].before.w = before.w;
        state.panels[index].before.h = before.h;
        var after = JSON.parse(JSON.stringify(afterPanel));
        state.panels[index].x = after.x;
        state.panels[index].y = after.y;
        state.panels[index].w = after.w;
        state.panels[index].h = after.h;
        state.panels[index].z = 100;
    },
    returnSize: function (state, {index}) {
        if (!state.panels[index].before) {
            console.warn("[STORE::DASHBOARD::returnSize] [WARN] Not found before data.");
            return;
        }
        state.panels[index].w = state.panels[index].before.w;
        state.panels[index].h = state.panels[index].before.h;
    },
    returnPosition: function (state, {index}) {
        if (!state.panels[index].before) {
            console.warn("[STORE::DASHBOARD::returnPosition] [WARN] Not found before data.");
            return;
        }
        state.panels[index].x = state.panels[index].before.x;
        state.panels[index].y = state.panels[index].before.y;
    },
    clearBeforeData: function (state, {index}) {
        if (state.panels[index].before) {
            state.panels[index].before = null;
        }
    },
    movePanel: function (state, {index, afterPanel}) {
        var after = JSON.parse(JSON.stringify(afterPanel));
        state.panels[index].x = after.x;
        state.panels[index].y = after.y;
    },
    resizePanel: function (state, {index, afterPanel}) {
        var after = JSON.parse(JSON.stringify(afterPanel));
        state.panels[index].w = after.w;
        state.panels[index].h = after.h;
    },
    activePanel: function (state, {index}) {
        state.panels[index].z = 100;
    },
    deactivePanel: function (state, {index}) {
        state.panels[index].z = index;
    },
    setComponentOfPanel: function(state, { index, component_data }) {
        if (state.panels[index].component) {
            state.panels[index].component.component_data = component_data;
        } else {
            console.warn("[STORE::DASHBOARD::setComponentOfPanel] [WARN] No component data in panel.");
        }
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
}