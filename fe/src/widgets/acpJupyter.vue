<template>
  <v-card class="main">
    <v-toolbar dense height="30px">
      <v-btn small icon id="button" ref="opener" :title="$t('open')" @click="openUrl"><v-icon size="19">fas fa-folder-open</v-icon></v-btn>
      <v-spacer></v-spacer>
      <strong><span v-if="select_name">{{select_name}}</span></strong>
      <v-spacer v-if="select_name"></v-spacer>
      <v-btn small icon id="button" :title="$t('jupyter.pip_manage')" @click="openSetting"><v-icon size="19">extension</v-icon></v-btn>
    </v-toolbar>

    <div ref="jupyter" id="jupyter">
      <v-layout v-if="!url" align-center justify-center fill-height>
        <span>{{$t('jupyter.open_project')}}</span>
      </v-layout>
      <iframe v-else :src="url" id="frame"></iframe>
		</div>

    <v-dialog
      v-model="pip_showSetting"
      scrollable  
      :overlay="false"
      max-width="750px"
      transition="dialog-transition"
      :dark="$vuetify.theme.dark"
    >
      <v-card class="pmCard">
        <div class="title">
          <v-layout align-center justify-center fill-height>
            <span>{{$t('jupyter.pip_manage')}}</span>
          </v-layout>
        </div>
        <v-divider></v-divider>
        <div class="Collapse">
          <v-card-actions class="pipInstalledCollapse">
            <span>{{$t('installed') + ' ' + $t('list')}}</span>
          </v-card-actions>
          <hr/>
        </div>
        <v-card-actions class="layoutActions">
          <v-spacer></v-spacer>
          <div class="searchZone">
          <input
          class="searchInput"
          type="text"
          :placeholder="$t('search')"
          v-model="pip_search"
          >
          <v-icon class="searchIcon">search</v-icon>
          </div>
        </v-card-actions>
        <v-card-text class="pmTextZone">
          <v-data-table
            :headers="pip_headers"
            :items="pip_pips"
            :loading="pip_tableLoading"
            :search="pip_search"
            :items-per-page="10"
            item-key="name"
            v-model="pip_selected"
            id="table"
            dense
            pagination.sync="pagination"
          >
            <template v-slot:body="{ items }">
              <tbody>
                <tr v-for="(props, index) in items" :key="index">
                  <template v-for="(item, key) in props">
                    <td v-if="key !== 'deleteMenu'" class="text-center" :key="item">{{ item }}</td>
                  </template>
                  <td>
                    <div class="tableButton-delete text-center">
                      <v-menu
                      v-model="props.deleteMenu"
                      :dark="dark"
                      offset-y
                      offset-x
                      top left
                      transition="slide-x-reverse-transition"
                      :close-on-content-click="false"
                      >
                        <template v-slot:activator="{ on }">
                          <a v-on="on"><v-icon size="14">fas fa-trash</v-icon>&nbsp;{{$t('delete')}}</a>
                        </template>
                        <v-card class="DeleteCheck">
                          <div class="menu-title">
                            <v-icon color="warning">warning</v-icon>&nbsp;&nbsp;<strong>{{$t('warning')}}</strong>
                          </div>
                          <v-divider></v-divider>
                          <v-card-text>
                            <span>{{$t('dialog_message.delete')}}</span>
                          </v-card-text>
                          <v-divider></v-divider>
                          <v-card-actions>
                            <v-btn small text @click="props.deleteMenu = false">{{$t('cancel')}}</v-btn>
                            <v-spacer></v-spacer>
                            <v-btn small text color="error" @click="onRemovePips(props)" :loading="pip_deleteLoading">{{$t('delete')}}</v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-menu>
                    </div>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-data-table>
        </v-card-text>
        <v-card class="pmTextZone pmOption">
          <v-menu 
          :dark="dark"
          top 
          offset-y 
          v-model="pip_newMenu"
          :close-on-click="false" 
          :close-on-content-click="false"
          >
            <template v-slot:activator="{on}">
              <v-btn small fab absolute bottom left v-on="on" :title="$t('jupyter.pip_installer')"><v-icon>add</v-icon></v-btn>
            </template>
            <v-card class="AddCheck">
              <div class="menu-title">
                <v-icon>queue</v-icon>&nbsp;&nbsp;<strong>{{$t('jupyter.pip_installer')}}</strong>
              </div>
              <v-divider></v-divider>
              <v-card-text>
                <input
                class="inputProjectName"
                type="text"
                :placeholder="$t('ex') + ') numpy,opencv'"
                v-model="pip_addPips"
                >
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
                <v-btn small text @click="onClosePipInstaller">{{$t('cancel')}}</v-btn>
                <v-spacer></v-spacer>
                <v-btn small text color="info" @click="onNewPips" :loading="pip_installLoading">{{$t('install')}}</v-btn>
              </v-card-actions>
            </v-card>
          </v-menu>
          <transition name="fade">
            <v-alert
              v-model="pip_alert"
              close-text="Close Alert"
              :color="pip_alertColor"
              dense
              dark
              dismissible
              outlined>
              {{ pip_alertMessage }}
            </v-alert>
          </transition>
        </v-card>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn small text @click="closeSetting">{{$t('close')}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="url_showUrl"
      scrollable  
      :overlay="false"
      max-width="750px"
      transition="dialog-transition"
      :dark="$vuetify.theme.dark"
    >
    <v-card class="pmCard" outlined>
      <div class="title">
          <v-layout align-center justify-center fill-height>
            <span>{{$t('jupyter.project_manage')}}</span>
          </v-layout>
        </div>
        <v-divider></v-divider>
        <div class="Collapse">
          <v-card-actions class="pipInstalledCollapse">
            <span>{{$t('project') + ' ' + $t('list')}}</span>
          </v-card-actions>
          <hr/>
        </div>
        <v-card-actions class="layoutActions">
          <v-spacer></v-spacer>
          <div class="searchZone">
          <input
          class="searchInput"
          type="text"
          :placeholder="$t('search')"
          v-model="url_search"
          >
          <v-icon class="searchIcon">search</v-icon>
          </div>
        </v-card-actions>
        <v-card-text class="pmTextZone">
          <v-data-table
            :headers="url_headers"
            :items="url_urls"
            :loading="url_tableLoading"
            :search="url_search"
            :items-per-page="5"
            dense
            item-key="name"
            v-model="url_selected"
            id="table"
            pagination.sync="pagination"
          >
            <template v-slot:body="{ items }">
              <tbody>
                <tr v-for="(props, index) in items" :key="index" @dblclick.stop="onOpenProject(props)">
                  <template v-for="(item, key) in props">
                    <td v-if="key !== 'token' && key !== 'deleteMenu'" :key="item" class="text-center">{{item}}</td>
                  </template>
                  <td><div class="tableButton text-center"><a @click.stop="onOpenProject(props)"><v-icon size="14">fas fa-folder-open</v-icon>&nbsp;{{$t('open')}}</a></div></td>
                  <td>
                    <div class="tableButton-delete text-center">
                      <v-menu
                      v-model="props.deleteMenu"
                      :dark="dark"
                      offset-y
                      offset-x
                      top left
                      transition="slide-x-reverse-transition"
                      :close-on-content-click="false"
                      >
                        <template v-slot:activator="{ on }">
                          <a v-on="on"><v-icon size="14">fas fa-trash</v-icon>&nbsp;{{$t('delete')}}</a>
                        </template>
                        <v-card class="DeleteCheck">
                          <div class="menu-title">
                            <v-icon color="warning">warning</v-icon>&nbsp;&nbsp;<strong>{{$t('warning')}}</strong>
                          </div>
                          <v-divider></v-divider>
                          <v-card-text>
                            <span>{{$t('dialog_message.delete')}}</span>
                          </v-card-text>
                          <v-divider></v-divider>
                          <v-card-actions>
                            <v-btn small text @click="props.deleteMenu = false">{{$t('cancel')}}</v-btn>
                            <v-spacer></v-spacer>
                            <v-btn small text color="error" @click="onDeleteProjects(props)" :loading="url_deleteLoading">{{$t('delete')}}</v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-menu>
                    </div>
                  </td>
                </tr>
              </tbody>
            </template>
          </v-data-table>
        </v-card-text>
        <v-card class="pmTextZone pmOption">
          <v-menu 
          :dark="dark"
          top 
          offset-y 
          v-model="url_newMenu"
          :close-on-click="false" 
          :close-on-content-click="false"
          >
            <template v-slot:activator="{on}">
              <v-btn small fab absolute bottom left v-on="on" :title="$t('new') + ' ' + $t('project') + ' ' + $t('create')"><v-icon>add</v-icon></v-btn>
            </template>
            <v-card class="AddCheck">
              <div class="menu-title">
                <v-icon>queue</v-icon>&nbsp;&nbsp;<strong>{{$t('new') + ' ' + $t('project')}}</strong>
              </div>
              <v-divider></v-divider>
              <v-card-text>
                <input
                class="inputProjectName"
                type="text"
                :placeholder="$t('jupyter.new_project_name')"
                v-model="url_newProjectName"
                >
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
                <v-btn small text @click="onCloseNewMenu">{{$t('cancel')}}</v-btn>
                <v-spacer></v-spacer>
                <v-btn small text color="info" @click="onNewProject" :loading="url_createLoading">{{$t('create')}}</v-btn>
              </v-card-actions>
            </v-card>
          </v-menu>
          <transition name="fade">
            <v-alert
              v-model="url_alert"
              close-text="Close Alert"
              :color="url_alertColor"
              dense
              dark
              dismissible
              outlined>
              {{ url_alertMessage }}
            </v-alert>
          </transition>
        </v-card>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn small text @click="closeUrl">{{$t('close')}}</v-btn>
        </v-card-actions>
    </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import axios from 'axios'
export default {
  name: "acpJupyter",
  props:{
    /**
		 * Init Save data from API.
		 */
    component_data: {
      default: null
    }
  },
  components:{
  },
  data(){
    return {
      // --- setting dialog data -------
      pip_showSetting: false, // pip manager dialog opener.
      pip_searchUsed: false, // search on/off.
      pip_search: "",
      pip_selected: [], // selected item of Pip list table.
      pip_tableLoading: false, // Display loading state of Pip list table.
      pip_headers: [ // header of table about Pip list.
        {
          text: this.$t("name"),
          align: "center",
          sortable: false,
          value: "name"
        },
        {
          text: this.$t("version"),
          align: "center",
          sortable: false,
          value: "version"
        },
        {
          text: this.$t("delete"),
          align: "center",
          sortable: false,
        }
      ], 
      pip_pips: [], // installed pip list.
      pip_newMenu: false, // Pip intsall Popup open and close value.
      pip_addPips: "", // Will install text of list.
      pip_installLoading: false, // install button loading state.
      pip_deleteMenu: false, // Pip Delete Popup open and close value.
      pip_deleteLoading: false, // delete button loading state.
      pip_alert: false, // pip dialog error message show and hide value.
      pip_alertMessage: "", // pip dialog error message.
      pip_alertColor: "error",
      // -----------------------
      // --- url select dialog data ---
      url_showUrl: false, // url selector dialog opener.
      url_searchUsed: false, // search on/off.
      url_search: "",
      url_selected: [], // selected item of Jupyter Url list on table.
      url_tableLoading: false, // Display loading state of Jupyter Url list table.
      url_headers: [ // header of table about Jupyter Url.
        {
          text: this.$t("name"),
          align: "center",
          sortable: false,
          value: "name"
        }, 
        {
          text: this.$t("url"),
          align: "center",
          sortable: false,
          value: "url"
        }, 
        {
          text: this.$t("created_time"),
          align: "center",
          sortable: false,
          value: "time"
        },
        {
          text: this.$t("open"),
          align: "center",
          sortable: false
        },
        {
          text: this.$t("delete"),
          align: "center",
          sortable: false
        }
      ],
      url_urls: [], // created jupyter urls.
      url_newMenu: false, // New Jupyter create Popup open and close value.
      url_newProjectName: "", // Will create Jupyter name.
      url_createLoading: false,
      url_deleteMenu: false, // Created Jupyter Delete Popup open and close value.
      url_deleteLoading: false, // delete button loading state.
      url_alert: false, // url dialog error message show and hide value.
      url_alertMessage: "", // url dialog error message.
      url_alertColor: "error",
      // ------------------------------
      select_name: "", // Select Jupyter project name.
      url: undefined, // show jypter url.
    }
  },
  computed:{
    dark() {
      return this.$vuetify.theme.dark;
    }
  },
  watch: {
  },
  methods:{
    // jupyter manage func.
    /**
     * Show Error message at Jupyter Manage Dialog.
     * @public
     * @param {string} - error message.
     */
    showUrlAlert: function (err, color) {
      var msg = "";
      if (typeof err === 'object') {
        msg = JSON.stringify(err);
      } else {
        msg = err;
      }
      this.url_alertMessage = msg;
      this.url_alertColor = color || 'error';
      this.url_alert = true;
    },
    /**
     * Hide Error message at Jupyter Manage Dialog.
     * @public
     * @param {null}
     */
    hideUrlAlert: function () {
      this.url_alertMessage = "";
      this.url_alert = false;
    },
    /**
     * Open Jupyter Manage Dialog.
     * @public
     * @param {null}
     */
    openUrl: async function () {
      if (!this.url_showUrl) {
        this.url_showUrl = true;
      }
      this.initUrl();
      this.url_tableLoading = true;
      try {
        var response = await this.$api.getJupyters(this.$store.getters["user/getAccessToken"], null, this.$store.getters["project/getSelectProject"]);
        this.$debug(this.$options.name, "getJupyters", "Response:", response);
        if (response.status === 'ERROR') {
          this.showUrlAlert(`Error: ${response.detail}`);
        }
        if (response.result) {
          if (response.result.obj) {
            this.url_urls = response.result.obj;
          } else {
            // error
            this.showUrlAlert(`Error: response data object is ${response.result.obj}`)
          }
        } else {
          // error
          this.showUrlAlert(`Error: response result is ${response.result}`);
        }
      } catch (err) {
        this.$error(this.$options.name, "getJupyters", err);
        this.showUrlAlert(`Failed: Load Jupyter projects => ${err.message}`);
      }
      this.url_tableLoading = false;
    },
    /**
     * Open Select Jupyter Url in iframe.
     * @public
     * @param {object} - Selected jupyter url item.
     */
    onOpenProject: function (select) {
      if (select.name) {
        this.select_name = select.name;
      } else {
        this.$warn(this.$options.name, "onOpenProject", "Wrong Select Jupyter Project name(", select.name, ")");
      }
      if (select.url) {
        if (select.token) {
          this.url = select.url + "/?token=" + select.token;
          this.closeUrl();
          this.saveApi();
          this.$debug(this.$options.name, "onOpenProject", "Name:", this.select_name, "Url:", this.url);
        } else {
          this.showUrlAlert("TokenError: Token is wrong");
        }
      } else {
        this.showUrlAlert("UrlError: URL is " + select.url);
      }
    },
    /**
     * Close Create Jupyter Project Popup.
     * @public
     * @param {null}
     */
    onCloseNewMenu: function () {
      if (this.url_newProjectName) {
        this.url_newProjectName = "";
      }
      this.url_newMenu = false;
    },
    /**
     * Request Create new Jupyter Project.
     * @public
     * @param {null}
     */
    onNewProject: async function () {
      if (this.url_alert) {
        this.hideUrlAlert();
      }
      this.url_createLoading = true;
      var project = this.url_newProjectName;
      this.$debug(this.$options.name, "onNewProject", "Create Project Name:", this.url_newProjectName);
      try {
        var response = await this.$api.newJupyter(this.$store.getters["user/getAccessToken"], null, this.$store.getters["project/getSelectProject"], project);
        this.$debug(this.$options.name, "newJupyter", "Response:", response);
        if (response.status === 'ERROR') {
          this.showUrlAlert(`Failed: Create ${project} project.`);
          this.$error(this.$options.name, "onNewProject::newJupyter", response.detail);
        } else {
          this.openUrl();
          this.showUrlAlert(`Success: Create ${project} project.`, 'success');
        }
      } catch (err) {
        this.$error(this.$options.name, "newJupyter", err);
        this.showUrlAlert(`Failed: Create ${project} project.`);
      }
      this.url_createLoading = false;
      this.onCloseNewMenu();
    },
    /**
     * Request Delete Select Jupyter Project.
     * @public
     * @param {null}
     */
    onDeleteProjects: async function (project) {
      this.url_deleteLoading = true;
      var projectData = this.$util.cloneObject(project);
      this.$debug(this.$options.name, "onDeleteProjects", "Delete items:", project);
      try {
        var response = await this.$api.deleteJupyters(this.$store.getters["user/getAccessToken"], null, this.$store.getters["project/getSelectProject"], project.name)
        this.$debug(this.$options.name, "deleteJupyters", "Response:", response);
        if (response.status === 'ERROR') {
          this.showUrlAlert(`Failed: Delete ${project.name} project => ${response.detail}`);
        } else {
          this.openUrl();
          if (this.url) {
            if (projectData.url === this.url.split("/?token=")[0]) {
              this.url = undefined;
            }
          }
          this.showUrlAlert(`Success: Delete ${project.name} project`, 'success');
        }
      } catch (err) {
        this.$error(this.$options.name, "deleteJypters", err);
        this.showUrlAlert(`Failed: Delete ${project.name} project`);
      }
      this.url_deleteLoading = false;
      this.url_deleteMenu = false;
    },
    /**
     * Close Jupyter Manage Dialog.
     * @public
     * @param {null}
     */
    closeUrl: function () {
      this.initUrl();
      this.url_showUrl = false;
    },
    /**
     * Initialize Project url dialog.
     * @public
     * @param {null}
     */
    initUrl: function () {
      this.url_selected = [];
      this.url_urls = [];
      this.url_searchUsed = false;
      this.url_search = "";
    },

    // pip manage dialog func.
    /**
     * Show Error message at Jupyter PIP Manage Dialog.
     * @public
     * @param {string} - error message.
     */
    showPipAlert: function (err, color) {
      var msg = "";
      if (typeof err === 'object') {
        msg = JSON.stringify(err);
      } else {
        msg = err;
      }
      this.pip_alert = true;
      this.pip_alertMessage = msg;
      this.pip_alertColor = color || 'error';
    },
    /**
     * Hide Error message at Jupyter PIP Manage Dialog.
     * @public
     * @param {null}
     */
    hidePipAlert: function () {
      this.pip_alertMessage = "";
      this.pip_alert = false;
    },
    /**
     * Open PIP Manage Dialog.
     * @public
     * @param {null}
     */
    openSetting: async function () {
      if (!this.pip_showSetting) {
        this.pip_showSetting = true;
      }
      this.initSetting();
      this.pip_tableLoading = true;
      try {
        var response = await this.$api.getJupyterPips(this.$store.getters["user/getAccessToken"], null);
        this.$debug(this.$options.name, "getJupyterPips", "Response:", response);
        if (response.status === 'ERROR') {
          this.showPipAlert(`Error: ${response.detail}`);
        } else {
          if (response.result) {
            if (response.result.obj) {
              var responsePips = response.result.obj;
              for (var pip of responsePips) {
                var result = pip.split("=="); // pip is 'pipname==${version}'
                this.pip_pips.push({ name: result[0], version: result[1] })
              }
            } else {
              // error
              this.showPipAlert(`Error: response result object is ${response.result.obj}`);
            }
          } else {
            // error
            this.showPipAlert(`Error: response result is ${response.result}`)
          }
        }
      } catch (err) {
        this.$error(this.$options.name, "getJupyterPips", err);
        this.showPipAlert('Failed: Load pip list.');
      }
      this.pip_tableLoading = false;
    },
    /**
     * Close PIP Manage Dialog.
     * @public
     * @param {null}
     */
    closeSetting: function () {
      this.initSetting();
      this.pip_showSetting = false;
    },
    /**
     * Initialize Pip manage dialog.
     * @public
     * @param {null}
     */
    initSetting: function () {
      this.pip_searchUsed = false;
      this.pip_search = "";
      this.pip_pips = [];
      this.pip_addPips = "";
    },
    /**
     * Request Remove Selected pip list.
     * @public
     * @param {null}
     */
    onRemovePips: async function (pip) {
      this.pip_deleteLoading = true;
      var pipName = pip.name;
      this.$debug(this.$options.name, "onRemovePips", pip);
      try {
        var response = await this.$api.removePip(this.$store.getters["user/getAccessToken"], null, pipName);
        this.$debug(this.$options.name, "removePips", "Response:", response);
        if (response.status === 'ERROR') {
          this.showPipAlert(`Failed: Remove ${pipName}`);
          this.$error(this.$options.name, "onRemovePips::removePip", response.data.detail);
        } else {
          this.openSetting();
          this.showPipAlert(`Success: Remove ${pipName}`, 'success');
        }
      } catch (err) {
        this.$error(this.$options.name, "removePips", err);
        this.showPipAlert(`Failed: Remove ${pipName}`);
      }
      this.pip_deleteLoading = false;
      pip.deleteMenu = false;
    },
    /**
     * Close Pip Install popup.
     * @public
     * @param {null}
     */
    onClosePipInstaller: function () {
      this.pip_addPips = "";
      this.pip_newMenu = false;
    },
    /**
     * Request Install Pip.
     * @public
     * @param {null}
     */
    onNewPips: async function () {
      if (this.pip_alert) {
        this.hidePipAlert();
      }
      if (!this.pip_addPips) {
        this.showPipAlert("Input PIP to install.");
        this.onClosePipInstaller();
        return;
      }
      this.pip_installLoading = true;
      var pipName = this.pip_addPips;
      // this.pip_addPips = this.pip_addPips.replace(" ", "");
      // var pips = this.pip_addPips.split(",");
      this.$debug(this.$options.name, "onNewPips", "Install list:", this.pip_addPips);
      try {
        var response = await this.$api.addJupyterPip(this.$store.getters["user/getAccessToken"], null, pipName);
        this.$debug(this.$options.name, "API::addJupyterPips", "Response:", response);
        if (response.status === "ERROR") {
          this.showPipAlert(`Failed: Install ${pipName} => ${response.detail}`);
        } else {
          this.openSetting();
          this.showPipAlert(`Success: Install ${pipName}`, 'success');
        }
      } catch (err) {
        this.$error(this.$options.name, "API::addJupyterPips", err);
        this.showPipAlert(`Failed: Install ${pipName}`);
      }
      this.pip_installLoading = false;
      this.onClosePipInstaller();
    },
    /**
		 * Trans Save Component Data To API.
		 * @param {null}
		 * @public
		 */
    saveApi: function () {
      var component_data = {};
      if (this.url) {
        component_data.title = this.select_name;
        component_data.url = this.url;
      }
      /**
       * Events that occur when component data is stored.
       * @type {Emit}
       */
			this.$emit("component_data", component_data);
    },
    /**
		 * Load Component Data From API.
		 * @param {null}
		 * @public
		 */
    loadApi: function () {
      if (this.component_data) {
        var copy_data = this.$util.cloneObject(this.component_data);
        for (var key in copy_data) {
          switch (key) {
            case "url": {
              this.url = copy_data[key];
              break;
            }
            case "title": {
              this.select_name = copy_data[key];
              break;
            }
          }
        }
      }
    }
  },
  created(){
  },
  mounted(){
    // load saved data.
    // <--- insert load saved data flow.

    // Add animate for Focus to opener.
    this.$nextTick(() => {
      this.loadApi();
      if (!this.url) {
        var opener = this.$refs.opener;
        if (opener) {
          opener.$el.animate([
            // keyframes
            { transform: 'scale(1)' }, 
            { transform: 'scale(1.5)' }, 
            { transform: 'scale(1)' } 
          ], { 
            // timing options
            duration: 800,
            iterations: 3
          });
        }
      }
    })
  }
}
</script>

<style scoped>
.v-toolbar:hover {
  cursor: move
}
.v-toolbar >>> .v-toolbar__content {
	padding: 0 10px !important;
}
.main {
  width: 100%;
  height: 100%;
}
.title {
  height: 50px;
}
#button {
  width: 20px; height: 20px; margin: 0 0 0 0;
}
#jupyter {
	position: absolute;
	width: 100%;
	height: calc(100% - 30px);
  top: 30px;
}
#jupyter >>> span {
  font-size: 25px;
  /* color: rgba(180, 180, 50, 0.8); */
}
#frame {
  width: 100%;
  height: 100%;
}
.errorZone {
  display: inline-block;
  position: relative;
  margin: 0;
  padding: 0;
  padding-left: 10px;
  padding-right: 10px;
}
.alert {
  border-radius: 4px;
  height: 20px;
}
.alertCancel {
  position: absolute; top: 9px; right: 20px;
}
/** Setting Dialog Style **/
.layoutText {
  margin: 0;
  padding: 0;
  padding: 10px;
}
.layoutActions {
  padding: 0px;
  border-radius: 4px;
  /* background-color: rgba(0, 0, 0, 0.3); */
}
.Collapse {
  padding: 10px;
}
.pipInstalledCollapse {
  height: 35px;
  cursor: pointer;
}
.searchZone {
  display: inline-block;
  position: relative;
  margin-left: 10px;
  margin-right: 10px;
  margin-bottom: 10px;
}
.searchInput {
  width: 100%;
  height: 35px;
  border: 2px solid;
  border-radius: 4px;
  padding-left: 5px;
  padding-right: 5px;
  outline: none;
}
.searchInput:focus {
  border-color: rgb(75, 85, 180);
}
.searchInput:focus + .searchIcon {
  color: rgb(75, 85, 180);
}
.searchIcon {
  margin: 0;
  padding: 0;
  position: absolute;
  top: 5px;
  right: 5px;
}
.installedZone {
  display: inline-block;
  position: relative;
  border: 1px solid;
  border-radius: 4px;
  margin: 5px;
  width: 100%;
  padding-left: 10px;
  padding-right: 10px;
}
.installedButton {
  margin: 0;
  padding: 0;
  position: absolute;
  top: 1px;
  right: 0px;
  width: 19px;
  height: 19px;
}
.installInput {
  width: 100%;
  height: 35px;
  border: 2px solid;
  border-radius: 4px;
  padding-left: 5px;
  padding-right: 5px;
  outline: none;
  margin-right: 10px;
}
.installInput:focus {
  border-color: rgb(75, 85, 180);
}
/** ----------------------------------------- **/
/** Project Manager Dialog Style **/
.pmCard {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}
.pmTextZone {
  margin: 0;
  padding: 5px;
  padding-left: 10px;
  padding-right: 10px;
}
/* .pmOption {
  height: 37px;
  min-height: 37px;
} */
#table {
  border: 1px solid;
  border-radius: 4px;
  border-color: rgba(255, 255, 255, 0.3);
}
#table >>> th {
  background-color: rgba(0, 0, 0, 0.3);
  font-size: 20px;
}
#table >>> .v-datatable__actions {
  border-top: 1px solid rgba(255, 255, 255, 0.3);
  background-color: rgba(0, 0, 0, 0.3) !important;
}
.tableItem {
  max-width: 270px !important;
  word-wrap: break-word;
}
.tableButton {
  padding-top: 2px;
  padding-bottom: 2px;
  padding-left: 5px;
  padding-right: 5px;
  border-radius: 5px;
  /* border: 1px solid; */
}
.tableButton:hover {
  background-color: rgba(255, 255, 255, 0.3);
}
.tableButton:active {
  background-color: rgba(255, 255, 255, 0.8);
}
.tableButton >>> a {
  /* color: rgb(114, 220, 78); */
  color: rgb(99, 171, 169);
}
.tableButton >>> .v-icon {
  /* color: rgb(114, 220, 78); */
  color: rgb(99, 171, 169);
}
.tableButton-delete >>> a {
  /* color: rgb(114, 220, 78); */
  color: rgb(179, 71, 69);
}
.tableButton-delete >>> .v-icon {
  /* color: rgb(114, 220, 78); */
  color: rgb(179, 71, 69);
}
.pmOptionButtonZone {
  border: 1px solid;
  border-color: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
  width: fit-content;
  margin: 0;
  padding: 0
}
.pmOptionButton {
  cursor: pointer;
}
.pmOptionButton--right {
  border-radius: 0px 4px 4px 0px;
}
.pmOptionButton--left {
  border-radius: 4px 0px 0px 4px;
}
.pmOptionButton:hover {
  background-color: rgba(255, 255, 255, 0.5);
}
.menu-title {
  height: 40px;
  display: flex;
  align-items: center;
  padding-left: 10px;
  padding-right: 10px;
}
.inputProjectName {
  width: 100%;
  height: 35px;
  border: 2px solid;
  border-radius: 4px;
  padding-left: 5px;
  padding-right: 5px;
  outline: none;
}
.inputProjectName:focus {
  border-color: rgb(75, 85, 180);
}
.AddCheck {
  width: 300px;
  border: 1px solid;
  border-radius: 4px;
}
.DeleteCheck {
  width: 300px;
  border: 1px solid;
  border-radius: 20px 20px 0px 20px !important;
}
/** ----------------------------------------- **/
/* Transition */
.fade-enter-active {
	transition: opacity 1s;
}
.fade-leave-active {
	transition: opacity 0.2s;
}
.fade-enter,
.fade-leave-to {
	opacity: 0;
}
.bounce-enter-active {
	animation: bounce-in 0.5s;
}
.bounce-leave-active {
	animation: bounce-in 0.3s reverse;
}
@keyframes bounce-in {
	0% {
		transform: scale(0);
	}
	30% {
		transform: scale(1.3);
	}
	100% {
		transform: scale(1);
	}
}
/** ---------------------------------------- **/
</style>
