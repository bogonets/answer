<template>
  <v-card class="main" v-resize="onParentResize" id="dashboard">
    <v-toolbar height="24px">
      <v-btn
        v-if="operator"
        small
        text
        icon
        @click="onAddPanel"
        :title="$t('add_panel')"
      >
        <v-icon>library_add</v-icon>
      </v-btn>
      &nbsp;
      <!-- border -->
      <v-tooltip bottom>
        <template v-if="operator" v-slot:activator="{ on }">
          <v-btn small text icon @click="openComponentList" v-on="on">
            <v-icon>list</v-icon>
          </v-btn>
        </template>
        <span>{{ $t("open_component_list") }}</span>
      </v-tooltip>

      <v-spacer></v-spacer>
      <v-btn
        v-if="operator"
        small
        text
        icon
        @click="onOpenDeleteCheckDialog"
        :loading="delete_signal"
        :title="$t('delete_layout')"
      >
        <v-icon>close</v-icon>
      </v-btn>
    </v-toolbar>
    <v-card class="parent--container" ref="parent--container">
      <v-card class="parent elevation-0" ref="parent">
        <drop class="drop-zone">
          <template v-for="(panel, index) in realtime_panel">
            <adb-dashboard-panel
              :key="panel.id || index + Math.random()"
              :x="panel.x"
              :y="panel.y"
              :w="panel.w"
              :h="panel.h"
              :z="panel.z"
              :draggable="operator"
              :resizable="operator"
              :parent="true"
              :drag-handle="panel.component ? '.v-toolbar' : undefined"
              class="panel-class"
              class-name-active="panel-active-class"
              :returnSizable="
                panel.before !== null && panel.before !== undefined
              "
              @dragstop="onDragstop($event, index)"
              @resizing="onResizing($event, index)"
              @resizestop="onResizestop($event, index)"
              @deletePanel="onDeletePanel(index, panel)"
              @fullscreen="onFullscreen(index, panel)"
              @defaultScreen="onDefaultScreen(index, panel)"
              @activated="onActivated(index, panel)"
              @deactivated="onDeactivated(index, panel)"
            >
              <drop class="drop-zone" @drop="insertComponent($event, index)">
                <div style="height: 100%; width: 100%; overflow: hidden;">
                  <component
                    v-if="
                      panel.component != null && panel.component != undefined
                    "
                    :is="panel.component.name"
                    :component_data="panel.component.component_data"
                    @component_data="onChangeComponentData($event, index)"
                    :resizeTrigger="resizeTrigger"
                  ></component>
                  <template v-else>
                    <div style="width: 100%; height: 100%;">
                      <v-layout align-center justify-center fill-height>
                        <v-btn
                          v-if="operator"
                          small
                          outlined
                          icon
                          @click="openComponentList"
                        >
                        <v-icon>add</v-icon>
                        </v-btn>
                      </v-layout>
                    </div>
                  </template>
                </div>
              </drop>
            </adb-dashboard-panel>
          </template>
        </drop>
      </v-card>
    </v-card>
    <v-dialog
      v-model="checkDialog"
      persistent
      :overlay="false"
      width="250px"
      max-width="500px"
      transition="dialog-transition"
      :dark="this.$vuetify.theme.dark"
    >
      <v-card>
        <v-card-title primary-title>
          <v-icon color="warning">warning</v-icon>
          <h3 class="headline mb-0">{{ $t("warning") }}</h3>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <p>{{ $t("info_delete_save_value") }}</p>
          <p>{{ $t("q_want_delete_layout") }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="checkDialog = false">{{ $t("cancel") }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn @click="onDeleteLayout">{{ $t("ok") }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import { Observable } from "rxjs";

import adbDashboardPanel from "@/components/Dashboard/adbDashboardPanel";
// import acpTableEventSource from "@/widgets/acpTableEventSource";
import acpTable from "@/widgets/acpTable";
import acpVodPlayer from "@/widgets/acpVodPlayer";
import acpImageViewer from "@/widgets/acpImageViewer";
import acpPlugin from "@/widgets/acpPlugin";
import acpJupyter from "@/widgets/acpJupyter";
import acpBlobViewer from "@/widgets/acpBlobsViewer";
import acpLambdaViewer from "@/widgets/acpLambdaViewer";
import RoisWidget from "@/components/Graph/RoisWidget.vue";

/**
 * Parent Window of DashboardPanel.
 * @author hadoo
 */

export default {
  name: "adbDashboard",
  components: {
    adbDashboardPanel,
    // acpTableEventSource,
    acpTable,
    acpVodPlayer,
    acpImageViewer,
    acpPlugin,
    acpJupyter,
    acpBlobViewer,
    acpLambdaViewer,
    RoisWidget,
  },
  props: {
    /**
     * 'active' is Draggable Controll value or Resizable Controll value.
     */
    active: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      panel_index: Number,
      resizeTrigger: null,
      save_signal: false,
      delete_signal: false,
      checkDialog: false,
      operator: Boolean,
    };
  },
  created() {
    this.operator = this.$store.getters["project/isOperator"];
  },
  methods: {
    /**
     * Window Resize Event of Dashboard. Unused.
     * @public
     */
    onParentResize: function() {
      // var card = document.getElementById('dashboard');
    },

    /**
     * Open component list drawer.
     * @public
     */
    openComponentList: function() {
      if (this.$store.getters["drawer/getCompoOpen"]) {
        this.$store.commit("drawer/setCompoOpen", { bool: false });
      } else {
        this.$store.commit("drawer/setCompoOpen", { bool: true });
      }
    },

    /**
     * Get Panel information method.
     * @param {number} - index of Selected panel.
     * @public
     * @returns {object} - Panel's info.
     */
    getPanelInfo: function(index) {
      var main_index = this.$store.getters["drawer/getLayoutIndex"];
      var panels_info = this.$store.getters["dashboard/getDashInfos"][
        main_index
      ].panels;
      var result = { index: index, info: panels_info[index] };
      return result;
    },

    /**
     * Send Save signal to API.
     * @public
     */
    savePanel: function() {
      setTimeout(() => {
        if (!this.save_signal) {
          this.save_signal = true;
        }
      }, 500);
    },

    /**
     * Add Panel event.
     * @public
     */
    onAddPanel: function() {
      this.$store.commit("dashboard/addPanel", {
        z: this.realtime_panel.length,
      });
      this.savePanel();
    },

    /**
     * Drop event of DashboardPanel and Insert Component.
     * @public
     * @param {object} - Components to be inserted.
     * @param {index} - Move panel(Panel to hold Component) index.
     */
    insertComponent: function(insert_component, index) {
      var new_data = this.$util.cloneObject(insert_component);
      this.$store.commit("dashboard/insertComponent", {
        index: index,
        component: new_data,
      });
      this.savePanel();
    },

    /**
     * Open delete check dialog.
     * @public
     */
    onOpenDeleteCheckDialog: function() {
      this.checkDialog = true;
    },

    /**
     * Delete layout event. Send delete signal to API.
     * @public
     */
    onDeleteLayout: function() {
      this.delete_signal = true;
      this.checkDialog = false;
    },

    // ######################################################
    // ################# Panel(Dashboard) Event ####################
    // ######################################################
    /**
     * Dragstop event of DashboardPanel.
     * @param {object} - Changed x,y,w,h value information.
     * @param {number} - Selected Panel index.
     * @public
     */
    onDragstop: function(event, index) {
      this.$store.commit("dashboard/movePanel", {
        index: index,
        afterPanel: event,
      });
      this.savePanel();
    },
    /**
     * Resizing event of DashboardPanel. Unused.
     * @param {object} - Changed x,y,w,h value information.
     * @public
     */
    onResizing: function(event) {
      if (this.operator) {
        this.resizeTrigger = {};
        this.resizeTrigger.w = event.w;
        this.resizeTrigger.h = event.h;
      }
    },
    /**
     * Resizestop event of DashboardPanel.
     * @param {object} - Changed x,y,w,h value information.
     * @param {number} - Selected Panel index.
     * @public
     */
    onResizestop: function(event, index) {
      this.$store.commit("dashboard/resizePanel", {
        index: index,
        afterPanel: event,
      });
      this.savePanel();
    },

    /**
     * Delete panel event.
     * @public
     * @param {number} - Selected panel index.
     */
    onDeletePanel: function(index) {
      this.$store.commit("dashboard/deletePanel", { index: index });
      this.savePanel();
    },

    /**
     * Change Fullscreen event.
     * @public
     * @param {number} - Selected panel index.
     * @param {object} - Selected panel data.
     */
    onFullscreen: function(index, panel) {
      var full = {
        x: 0,
        y: 0,
        w: this.$refs.parent.$el.clientWidth,
        h: this.$refs.parent.$el.clientHeight,
      };
      this.$store.commit("dashboard/fullScreenPanel", {
        index: index,
        beforePanel: panel,
        afterPanel: full,
      });
      this.savePanel();
    },

    /**
     * Return origin size.
     * @public
     * @param {number} - Selected panel index.
     */
    onDefaultScreen: function(index) {
      this.$store.commit("dashboard/returnSize", { index: index });
      this.$nextTick().then(() => {
        this.$store.commit("dashboard/returnPosition", { index: index });
        this.$store.commit("dashboard/clearBeforeData", { index: index });
        this.savePanel();
      });
    },

    /**
     * Panels` activated event.
     * @public
     * @param {number} - Selected panel index.
     */
    onActivated: function(index) {
      this.$store.commit("dashboard/activePanel", { index: index });
    },

    /**
     * Panels` deactivated event.
     * @public
     * @param {number} - Selected panel index.
     * @param {object} - Selected panel data.
     */
    onDeactivated: function(index, panel) {
      if (!panel.before) {
        this.$store.commit("dashboard/deactivePanel", { index: index });
      }
    },

    /**
     * Save Panel`s component data. And Send Save signal to API.
     * @public
     * @param {object} - Component data.
     * @param {number} - Selected panel index.
     */
    onChangeComponentData: function(event, index) {
      this.$store.commit("dashboard/setComponentOfPanel", {
        index: index,
        component_data: event,
      });
      this.savePanel();
    },
  },
  computed: {
    /**
     * Realtime change panel information(data).
     */
    realtime_panel() {
      if (this.$store.getters["dashboard/getPanels"]) {
        return this.$store.getters["dashboard/getPanels"];
      } else {
        return [];
      }
    },
  },
  watch: {
    save_signal() {
      if (this.save_signal) {
        this.$store.commit("etc/setLoadingLiner", { bool: true });
      } else {
        this.$store.commit("etc/setLoadingLiner", { bool: false });
      }
    },
  },
  mounted() {
    // this.$store.commit("dashboard/", {panels: this.panels});
  },
  beforeDestroy() {
    this.$store.commit("dashboard/deleteAllPanels");
  },
  subscriptions() {
    const $save_signal = this.$watchAsObservable("save_signal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((save_signal) => save_signal == true);
    const $delete_signal = this.$watchAsObservable("delete_signal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((delete_signal) => delete_signal == true); // if signal is true.
    return {
      save_result: Observable.combineLatest($save_signal, (save_signal) => ({
        save_signal,
        // eslint-disable-next-line no-unused-vars
      })).flatMap(({ save_signal }) =>
        this.$api
          .sendPanelsData(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"],
            this.$store.getters["project/getSelectLayout"],
            this.$util.dashboard_jTos(
              this.$store.getters["dashboard/getPanels"]
            )
          )
          .do((res) => {
            this.$debug(
              this.$options.name,
              "subscriptions::sendPanelsData",
              "Send Success. Response:",
              res
            );
          })
          .catch((err) => {
            this.$error(
              this.$options.name,
              "subscriptions::sendPanelsData",
              "Send Failed. Details:",
              err
            );
            return Observable.of(null);
          })
          .do(() => (this.save_signal = false))
      ),
      delete_result: Observable.combineLatest(
        $delete_signal,
        (delete_signal) => ({ delete_signal })
        // eslint-disable-next-line no-unused-vars
      ).flatMap(({ delete_signal }) =>
        this.$api
          .deleteLayout(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"],
            this.$store.getters["project/getSelectLayout"]
          )
          .do((res) => {
            this.$store.commit("project/setSelectLayout", { layoutName: null });
            this.$router.push(this.$page.project);
            this.$store.commit("signal/setLayoutMainSignal", { bool: true });
            this.$debug(
              this.$options.name,
              "subcriptions::deleteLayout",
              "Delete Layout Success. Response:",
              res
            );
          })
          .catch((err) => {
            this.$error(
              this.$options.name,
              "subcriptions::deleteLayout",
              "Delete Layout Failed. Details:",
              err
            );
            return Observable.of(null);
          })
          .do(() => {
            this.delete_signal = false;
          })
      ),
    };
  },
};
</script>

<style scoped>
.main {
  width: 100%;
  height: 100%;
  /* border: 1px dotted #aaaaaa !important; */
}
.parent--container {
  width: 100%;
  height: calc(100% - 24px);
  background-color: rgba(48, 48, 48, 0.3);
  padding-top: 27px;
}
.parent {
  width: 100%;
  height: 100%;
  background-color: transparent;
}
.drop-zone {
  /* border: 1px dotted #f0f0f0; */
  /* background-color: rgba(48, 48, 48, 0.5); */
  width: 100%;
  height: 100%;
}
.v-toolbar >>> .v-toolbar__content {
  padding-left: 5px;
  padding-right: 5px;
}
.v-btn {
  margin: 0 !important;
  padding: 0 !important;
}
.menu_divider {
  margin-left: 3px;
  margin-right: 3px;
}
.panel-class {
  background-color: rgba(125, 125, 125, 0.2);
}
.panel-active-class {
  border: 1px solid black;
  -webkit-box-shadow: 10px 10px 5px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 10px 10px 5px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 10px 10px 5px 0px rgba(0, 0, 0, 0.75);
}
</style>
