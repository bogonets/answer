const state = {
  navi_show: false,
  navi_mini: true,
  navi_width: 200,
  // layout_index: 0,
  compo_open: false,
  compo_width: 200,
  open_add_layout: false
}

const getters = {
  getNaviShow: function (state) {
    return state.navi_show;
  },
  getNaviMini: function (state) {
    return state.navi_mini;
  },
  getNaviWidth: function (state) {
    return state.navi_width;
  },
  // getLayoutIndex: function (state) {
  //   return state.layout_index;
  // },
  getCompoOpen: function (state) {
    return state.compo_open;
  },
  getCompoWidth: function (state) {
    return state.compo_width;
  },
  getOpenAddLayout: function (state) {
    return state.open_add_layout;
  }
}

const mutations = {
  setNaviShow: function (state, {bool}) {
    state.navi_show = bool;
  },
  setNaviMini: function (state, {bool}) {
    state.navi_mini = bool;
  },
  setNaviWidth: function (state, {width}) {
    state.navi_width = width;
  },
  // setLayoutIndex: function (state, {index}) {
  //   state.layout_index = index;
  // },
  setCompoOpen: function (state, {bool}) {
    state.compo_open = bool;
  },
  setCompoWidth: function (state, {width}) {
    state.compo_width = width;
  },
  setOpenAddLayout: function (state, {bool}) {
    state.open_add_layout = bool;
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
}
