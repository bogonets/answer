const state = {
  selected_index: 0,
  navi_list: [
    {
      title: "layout",
      icon: "dashboard",
      active: true,
      level: 10,
      submenu: [],
      expands: [{ name: "add_layout", icon: "add" }],
    },
    {
      title: "storage",
      icon: "fas fa-database",
      level: 10,
    },
    {
      title: "graph_setting",
      icon: "account_tree",
      level: 10,
    },
    {
      title: "airjoy_manage",
      icon: "fas fa-wind",
      level: 10,
    },
    {
      title: "airjoy_graph",
      icon: "fas fa-chart-bar",
      level: 10,
    },
    {
      title: "airjoy_monitor",
      icon: "fas fa-border-all",
      level: 10,
    },
    {
      title: "tables",
      icon: "fas fa-database",
      level: 10,
    },
    {
      title: "files",
      icon: "fas fa-folder-open",
      level: 10,
    },
    {
      title: "tasks",
      icon: "fas fa-tasks",
      level: 10,
    },
    {
      title: "vms",
      icon: "fas fa-cctv",
      level: 10,
    },
    {
      title: "auth_management",
      icon: "fas fa-users-cog",
      level: 10,
    },
  ],
  select_project: "",
  view_navi_list: [],
  select_layout: "",
};

const getters = {
  isAuth: function(state) {
    return true;
  },
  isOperator: function(state) {
    return state.project_auth >= 80;
  },
  isAdmin: function(state) {
    return state.project_auth >= 100;
  },
  getSelectIndex: function(state) {
    return state.selected_index;
  },
  getMenuList: function(state) {
    return state.navi_list;
  },
  getSelectProject: function(state) {
    return state.select_project;
  },
  getViewMenuList: function(state) {
    return state.view_navi_list;
  },
  getSelectLayout: function(state) {
    return state.select_layout;
  },
  getProjectAuth: function(state) {
    return state.project_auth;
  },
};
const mutations = {
  setSelectIndex: function(state, { index }) {
    state.selected_index = index;
  },
  setSelectProject: function(state, { name }) {
    state.select_project = name;
  },
  setProjectAuth: function(state, { auth }) {
    state.project_auth = auth;
  },
  setViewNaviList: function(state, { menus }) {
    var menu_list = [];
    state.view_navi_list = [];
    if (getters.isAdmin(state)) {
      state.view_navi_list = state.navi_list;
    } else {
      state.navi_list.forEach((navi) => {
        if (navi.title != "auth_management") {
          menu_list.push(navi);
        }
      });
      state.view_navi_list = menu_list;
    }
  },
  setLayouts: function(state, { layouts }) {
    if (!state.view_navi_list.length) {
      return;
    }
    state.view_navi_list[0].submenu = [];
    if (layouts) {
      for (var index = 0; index < layouts.length; ++index) {
        state.view_navi_list[0].submenu.push({
          name: layouts[index],
          icon: "dashboard",
        });
      }
    }
  },
  setSelectLayout: function(state, { layoutName }) {
    state.select_layout = layoutName;
  },
  addLayout: function(state, { name }) {
    var re_menu = [];
    var before_submenu = state.project_menu_list[0].submenu;
    // console.log(before_submenu);
    // console.log(typeof before_submenu);
    // console.log("Length: ", before_submenu.length);
    for (var index = 0; index < before_submenu.length - 1; ++index) {
      re_menu.push(before_submenu[index]);
    }
    re_menu.push({ name: name, icon: "view_module" });
    state.project_menu_list[0].submenu = re_menu;
  },
  toggleListActive: function(state, { item }) {
    if (item.active !== null && item.active !== undefined) {
      item.active = !item.active;
    } else {
      console.warn(
        "store/project/toggleListActive existedError:",
        "item active is",
        item.active
      );
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
};
