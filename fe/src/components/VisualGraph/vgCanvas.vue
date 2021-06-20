<template>
  <div id="canvas_main">
    <v-toolbar height="24">
      <v-btn
        small
        icon
        style="margin: 0; margin-left: -5px;"
        :disabled="disabled_load_btn"
        @click="onOpenLocalFile"
      >
        <v-icon
          v-html="'fas fa-folder-open'"
          size="20"
          :title="$t('open_local')"
        ></v-icon>
      </v-btn>
      <v-btn
        small
        icon
        style="margin: 0"
        :disabled="disabled_download_btn"
        @click="onDownload"
      >
        <v-icon
          v-html="'fas fa-download'"
          size="20"
          :title="$t('download_local')"
        ></v-icon>
      </v-btn>
      <v-divider
        style="margin: 0; margin-left: 5px; margin-right: 5px;"
        vertical
      ></v-divider>
      <v-btn
        small
        icon
        style="margin: 0;"
        :disabled="disabled_download_btn"
        @click="openGraphStatusBoard"
      >
        <v-icon
          v-html="'fas fa-list-alt'"
          size="20"
          :title="$t('show_graph_state')"
        ></v-icon>
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn
        small
        icon
        style="margin: 0;"
        @click="onSaveGraph"
        :loading="saveSignal || load_signal"
        :disabled="disabled_download_btn"
      >
        <v-icon v-html="'fas fa-upload'" size="20" :title="$t('save')"></v-icon>
      </v-btn>
      <v-divider
        style="margin: 0; margin-left: 5px; margin-right: 5px;"
        vertical
      ></v-divider>
      <v-btn
        small
        icon
        style="margin: 0; margin-right: -5px;"
        @click="onClearGraph"
        :disabled="disabled_download_btn"
      >
        <v-icon v-html="'fas fa-trash-alt'" size="20"></v-icon>
      </v-btn>
    </v-toolbar>

    <v-card style="width: 100%; height: 100%;" ref="canvasCard">
      <div style="width: 100%; height: 100%; position: absolute">
        <canvas
          ref="mycanvas"
          width="2000"
          height="2000"
          v-resize="onResize"
          :style="this.$backgroundColor()"
        ></canvas>
      </div>
    </v-card>

    <v-snackbar
      v-model="alert"
      top
      right
      absolute
      multi-line
      :timeout="alert_timeout"
      style="opacity: .8; margin: 0; margin-right: 10px; margin-top: 10px"
    >
      <v-layout row wrap style="overflow-y: auto !important; max-height: 80px">
        <v-flex xs12 v-for="msg in alert_msg" :key="msg">
          <span :style="'color:' + alert_color">{{ msg }}</span>
        </v-flex>
      </v-layout>
      <!-- <template v-for="msg in alert_msg">
        <p :style="'color:' + alert_color" :key="msg">{{msg}}<br/></p>
            </template>-->
      <v-icon @click="alert = false">clear</v-icon>
    </v-snackbar>

    <check-dialog
      :open="checkDialog"
      :title="$t(checkDialogTitle)"
      :messages="checkMessgaes"
      :msgI18n="true"
      @onCancel="onCheckCancel"
      @onOk="onCheckOk"
    ></check-dialog>

    <v-dialog
      v-model="statusBoard"
      persistent
      :overlay="false"
      transition="dialog-transition"
      :dark="this.$vuetify.theme.dark"
      width="500"
    >
      <v-card width="500">
        <v-card-title>
          <strong>{{ $t("graph_status") }}</strong>
        </v-card-title>
        <v-divider></v-divider>
        <div style="padding: 10px; width: 100%; height: 400px;">
          <a-json-field
            style="height: 100%;"
            :json="jsonData"
            :tabSize="2"
            :readonly="true"
            :resize="'vertical'"
            outline
          ></a-json-field>
        </div>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn small @click.stop="closeStatusBoard">{{ $t("ok") }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import CheckDialog from "@/components/Dialog/adlgCheck.vue";

import { Observable } from "rxjs";
import { installGraph } from "@/services/visualgraph/graph/GraphInstaller.js";
import { addLambda } from "@/services/visualgraph/lambda/addLambda.js";

export default {
  props: {},

  components: {
    CheckDialog,
  },

  data() {
    return {
      name: "vgCanvas",
      graph_controller: null,
      graph_canvas: null,
      resize_ready: false,
      save_data: null,
      saveSignal: false,
      alert: false,
      alert_msg: null,
      alert_colors: {
        error: "rgb(231, 116, 112)",
        warn: "#ffde03",
        default: null,
      },
      alert_color: null,
      alert_timeout: 5000,
      getBoxSignal: false,
      load_signal: false,
      disabled_load_btn: true,
      disabled_download_btn: true,

      checkDialog: false,
      checkLocal: false,
      checkDialogTitle: "warning",
      checkMessgaes: ["warn_alldata_clear", "ques_want_delete"],

      statusTimer: null,
      statusSignal: false,
      statusBoard: false,
      jsonData: null,

      isPlaying: false,
    };
  },

  computed: {
    // eslint-disable-next-line vue/return-in-computed-property
    checkExistLambda() {
      if (this.graph_controller) {
        if (this.graph_controller._nodes.length === 0) {
          return {
            existed: false,
            length: this.graph_controller._nodes.length,
          };
        } else {
          return {
            existed: true,
            length: this.graph_controller._nodes.length,
          };
        }
      }
    },
    // eslint-disable-next-line vue/return-in-computed-property
    checkExistTask() {
      if (this.graph_controller) {
        if (this.graph_controller._tasks.length === 0) {
          return {
            existed: false,
            length: this.graph_controller._tasks.length,
          };
        } else {
          return {
            existed: true,
            length: this.graph_controller._tasks.length,
          };
        }
      }
    },
  },

  watch: {
    checkExistTask() {
      if (!this.checkExistTask.existed) {
        this.alertMsg(this.alert_colors.default, [this.$t("make_task_please")]);
      } else {
        if (!this.checkExistLambda.existed) {
          this.alertMsg(this.alert_colors.default, [
            this.$t("make_lambda_please"),
          ]);
        }
      }
    },
  },

  methods: {
    /**
     * Install Graph when Create This Component.
     * @public
     * @param {null}
     */
    installGraph: function() {
      this.$debug(this.name, "installGraph", "intalling...");
      installGraph(this);
      this.$debug(this.name, "installGraph", "done.");
    },

    /**
     * Initialize when Get lambda templete from API.
     * @public
     * @param {null}
     */
    initialize: function() {
      this.$debug(this.name, "initialize", "start...");
      this.isPlaying = false;
      this.alert_msg = null;
      this.graph_controller = new this.LGraph();
      this.graph_controller.last_node_id = 0;
      this.graph_controller.last_task_id = 0;
      this.graph_controller.last_link_id = 0;
      var temp_canvas = this.$refs.mycanvas;
      temp_canvas.width = temp_canvas.clientWidth;
      temp_canvas.height = temp_canvas.clientHeight;
      this.graph_canvas = new this.LGraphCanvas(
        temp_canvas,
        this.graph_controller
      );
      this.graph_canvas.preventMouseEvent(false);
      this.graph_controller.start();

      if (!this.resize_ready) {
        this.resize_ready = true;
      }
      this.disabled_load_btn = false;
      this.disabled_download_btn = false;
      this.load_signal = true;
      this.$debug(this.name, "initialize", "done.");
    },

    /**
     * Open Graph Status board.
     * @public
     */
    openGraphStatusBoard: function() {
      this.statusBoard = true;
      this.statusSignal = true;
      this.statusTimer = setInterval(() => {
        if (!this.statusSignal) {
          this.statusSignal = true;
        }
      }, 3000);
    },

    /**
     * Close Graph Status board.
     * @public
     */
    closeStatusBoard: function() {
      this.statusBoard = false;
      if (this.statusTimer) {
        clearInterval(this.statusTimer);
        this.statusTimer = null;
      }
    },

    /**
     * Add Lambda template from API.
     * @public
     * @param {templates} - labmda templetes.
     */
    addLambda: function(templates) {
      addLambda(this, templates);
    },

    /**
     * Setting Load saved graph data from API.
     * @public
     * @param {loadData} - saved graph data.
     */
    setLoadData: function(loadData) {
      this.clearGraph();
      if (typeof loadData === "string") {
        loadData = JSON.parse(loadData);
      }
      this.graph_controller.configure(loadData);
      this.graph_controller.change(); // refresh.
      if (this.alert) {
        this.alert = false;
      }
    },

    /**
     * Delete All Task and All Lambda.
     * @public
     * @param {null}
     */
    clearGraph: function() {
      this.onDeselectLambda();
      this.graph_controller.clear();
      this.$debug(this.name, "clearGraph", "All Clear.");
    },

    /**
     * Showing alert message.
     * @public
     * @param {string} - Color value.
     * @param {array} - Messages.
     * @param {number} - Timeout.
     */
    alertMsg: function(alertColor, alertMsg, alertTimeout) {
      this.alert_color = alertColor;
      this.alert_msg = alertMsg;
      if (alertTimeout !== 0) {
        this.alert_timeout = alertTimeout || 5000; // default 5 second.
      } else {
        this.alert_timeout = 0; // unlimited.  please this.alert = false --> close.
      }
      this.$nextTick(() => {
        this.alert = true;
      });
    },

    /**
     * Saving modified task data from detail setting window.
     * @public
     * @param {object} - modified task data from detail setting window.
     */
    saveTask: function(taskData) {
      if (taskData.msg) {
        taskData.msg[0] = taskData.result.title + ": " + taskData.msg[0];
      }
      if (taskData.success) {
        for (var i = 0; i < this.graph_controller._tasks.length; ++i) {
          var targetTask = this.graph_controller._tasks[i];
          if (taskData.result.id === targetTask.id) {
            if (taskData.result.ui_setting) {
              for (var prop of taskData.result.ui_setting) {
                for (var taskProp of targetTask.properties) {
                  if (prop.name === taskProp.name) {
                    if (
                      taskProp.type === "int" &&
                      taskProp.rule === "read_and_write"
                    ) {
                      taskProp.value = parseInt(prop.component.value);
                    } else if (
                      taskProp.type === "float" &&
                      taskProp.rule === "read_and_write"
                    ) {
                      taskProp.value = parseFloat(prop.component.value);
                    } else if (
                      taskProp.type === "double" &&
                      taskProp.rule === "read_and_write"
                    ) {
                      taskProp.value = parseFloat(prop.component.value);
                    } else if (taskProp.rule === "read_and_write") {
                      if (prop.component.value === this.$t("null")) {
                        taskProp.value = "";
                      } else {
                        taskProp.value = prop.component.value;
                      }
                    }
                  }
                }
              }
            }
            if (taskData.result.title) {
              targetTask.title = taskData.result.title;
            }
            // this.alertMsg(this.alert_colors.default, taskData.msg);
          }
        }
      } else {
        this.alertMsg(this.alert_colors.error, taskData.msg);
        this.$warn(this.name, "saveTask", "Details:", taskData.msg);
      }
    },

    /**
     * Saving modified lambda data from detail setting window.
     * @public
     * @param {object} - modified lambda data from detail setting window.
     */
    saveLambda: function(lambdaData) {
      if (lambdaData.msg) {
        lambdaData.msg[0] = lambdaData.result.title + ": " + lambdaData.msg[0];
      }
      if (lambdaData.success) {
        var emitData = lambdaData.result;
        var nodes = this.graph_controller._nodes;
        for (var i = 0; i < nodes.length; ++i) {
          var node = nodes[i];
          if (emitData.id) {
            if (node.id === emitData.id) {
              if (emitData.ui_setting) {
                for (var prop of emitData.ui_setting) {
                  for (var nodeProp of node.properties) {
                    if (prop.name === nodeProp.name) {
                      if (nodeProp.type === "int") {
                        nodeProp.value = parseInt(prop.component.value);
                      } else if (nodeProp.type === "float") {
                        nodeProp.value = parseFloat(prop.component.value);
                      } else if (nodeProp.type === "double") {
                        nodeProp.value = parseFloat(prop.component.value);
                      } else {
                        if (prop.component.value === this.$t("null")) {
                          nodeProp.value = "";
                        } else {
                          nodeProp.value = prop.component.value;
                        }
                      }
                    }
                  }
                }
              }
              if (emitData.uid) {
                node.uid = emitData.uid;
              }
              if (emitData.title) {
                node.title = emitData.title;
              }
              if (emitData.shape) {
                node.shape = emitData.shape;
              }
              if (emitData.signals) {
                node.signals = emitData.signals;
              } else {
                node.signals = [];
              }
              if (emitData.inputs) {
                node.inputs = emitData.inputs;
                // /** tag or group match about links. */
                // for (var a in node.inputs) {
                // 	var input = node.inputs[a];
                // 	if (input.link === -1) {
                // 		continue;
                // 	}
                // 	for (var b in this.graph_controller.links) {
                // 		var link = this.graph_controller.links[b];
                // 		if (input.link === link.id) {
                // 			var outputId = link.origin_id;
                // 			var outputIndex = link.origin_slot;
                // 			for (var c in this.graph_controller._nodes) {
                // 				var target = this.graph_controller._nodes[c];
                // 				if (target.id === outputId) {
                // 					if (!this.LiteGraph.isValidConnection(target.outputs[outputIndex].type, input.type)) {
                // 						node.disconnectInput(parseInt(a));
                // 					}
                // 				}
                // 			}
                // 		}
                // 	}
                // }
              }
              if (emitData.outputs) {
                node.outputs = emitData.outputs;
                // /** tag or group match about links. */
                // for (var a in node.outputs) {
                // 	var output = node.outputs[a];
                // 	for (var b in output.links) {
                // 		var outputLink = output.links[b];
                // 		for (var c in this.graph_controller.links) {
                // 			var link = this.graph_controller.links[c];
                // 			if (outputLink === link.id) {
                // 				var inputId = link.target_id;
                // 				var inputIndex = link.target_slot;
                // 				for (var d in this.graph_controller._nodes) {
                // 					var target = this.graph_controller._nodes[d];
                // 					if (target.id === inputId) {
                // 						if (!this.LiteGraph.isValidConnection(output.type, target.inputs[inputIndex].type)) {
                // 							target.disconnectInput(inputIndex);
                // 						}
                // 					}
                // 				}
                // 			}
                // 		}
                // 	}
                // }
              }
              for (var index = 0; index < emitData.flags.length; ++index) {
                node.flags[emitData.flags[index].key] =
                  emitData.flags[index].value;
              }
            } else {
              continue;
            }
          } else {
            this.$error(this.name, "saveLambda", "ID Error. ID:", emitData.id);
          }
        }
      } else {
        this.alertMsg(this.alert_colors.error, lambdaData.msg);
        this.$warn(
          this.name,
          "saveLambda",
          "Save Failed. Details:",
          lambdaData.msg
        );
      }
    },

    /**
     * Saving modified lambda or task data from detail setting window.
     * @public
     * @param {object} - modified lambda or task data from detail setting window.
     */
    saveSetting: function(settingData) {
      if (settingData.result.type === "task") {
        this.saveTask(settingData);
      } else {
        this.saveLambda(settingData);
      }
      this.graph_controller.change();
    },

    /**
     * Delete lambda or task.
     * @public
     * @param {object} - lambda or task.
     */
    deleteLambdaNTask: function(LnT) {
      this.graph_controller.remove(LnT);
    },

    /**
     * Open Delete Check Dialog from ContextMenu.
     * @public
     */
    openDeleteCheck: function() {
      /**
       * Delete event. Transfer event to DetailSetting.
       * @type {emit}
       * @param {boolean} - Static value (true).
       */
      this.$emit("openDeleteCheck", true);
    },

    onSaveTask: function(taskId) {
      var result = this.graph_controller.serialize();

      var task = [];
      var nodeList = [];
      var linkList = [];

      // remove unmatched tasks
      for (var i = 0; i < result.tasks.length; i++) {
        if (result.tasks[i].id == taskId) {
          task.push(result.tasks[i]);
          break;
        }
      }

      // create nodeList
      for (var i = 0; i < result.nodes.length; i++) {
        if (result.nodes[i].task_id == taskId) {
          nodeList.push(result.nodes[i]);
        }
      }

      // create links
      for (var i = 0; i < result.links.length; i++) {
        // check origin_id and target_id
        for (var j = 0; j < nodeList.length; j++) {
          if (
            result.links[i].origin_id == nodeList[j].id ||
            result.links[i].tarket_id == nodeList[j].id
          ) {
            linkList.push(result.links[i]);
          }
        }
      }

      result.tasks = task;
      result.nodes = nodeList;
      result.links = linkList;

      this.isPlaying = true;
      this.save_data = result;
      this.saveSignal = true;
      this.alertMsg(this.alert_colors.default, [this.$t("please_wait")]);
    },

    /**
     * Load local graph data - FileType: JSON.
     * @public
     */
    LoadLocalFile: function() {
      var a = document.createElement("input");
      a.setAttribute("type", "file");
      a.click();
      var self = this;
      a.addEventListener("change", (evt) => {
        var file = evt.target.files[0];
        var reader = new FileReader();
        reader.onload = function() {
          var json = JSON.parse(reader.result);
          self.clearGraph();
          self.graph_controller.configure(json);
          self.graph_controller.change();
          self.$debug(self.name, "LoadLocalFile", "Load Local File:", file);
        };
        reader.readAsText(file);
      });
    },

    /**
     * Check Duplicate Task and Lambda.
     * @public
     * @param {object} - Graph Data(Tasks and Lambdas).
     */
    checkDuplicate: function(graph) {
      var tasks = graph.tasks;
      var lambdas = graph.nodes;
      var resultTasks = this.checkTaskDuplicate(tasks);
      if (resultTasks[0]) {
        var resultLambdas = this.checkLambdaDuplicate(tasks, lambdas);
        if (resultLambdas[0]) {
          return true;
        } else {
          this.$error(
            this.$options.name,
            "Duplicated lambda",
            resultLambdas[2] + " -> " + resultLambdas[1]
          );
          this.alertMsg(this.alert_colors.error, [
            this.$t("lambda_duplicated"),
            this.$t("task") + ": " + resultLambdas[2],
            this.$t("lambda") + ": " + resultLambdas[1],
          ]);
          return false;
        }
      } else {
        this.$error(this.$options.name, "Duplicated Task", resultTasks[1]);
        this.alertMsg(this.alert_colors.error, [
          this.$t("task_duplicated"),
          this.$t("task") + ": " + resultTasks[1],
        ]);
        return false;
      }
    },

    /**
     * Check Duplicate Task.
     * @public
     * @param {array} - Tasks.
     */
    checkTaskDuplicate: function(tasks) {
      for (var i = 0; i < tasks.length; ++i) {
        var task = tasks[i].title;
        for (var j = 0; j < tasks.length; ++j) {
          if (i == j) {
            continue;
          }
          var target = tasks[j].title;
          if (task === target) {
            return [false, task];
          }
        }
      }
      return [true, null];
    },

    /**
     * Check Duplicate Lambda in Task.
     * @public
     * @param {array} - Tasks.
     * @param {array} - Lambdas.
     */
    checkLambdaDuplicate: function(tasks, lambdas) {
      for (var i = 0; i < tasks.length; ++i) {
        var lambdasInTask = tasks[i].nodes;
        var checkArray = [];
        for (var id of lambdasInTask) {
          for (var j = 0; j < lambdas.length; ++j) {
            var lambda = lambdas[j];
            if (lambda.id === id) {
              checkArray.push(lambda.title);
            }
          }
        }
        var copyArray = checkArray.slice();
        for (var index = 0; index < checkArray.length; ++index) {
          var lambdaTitle = checkArray[index];
          for (var index2 = 0; index2 < copyArray.length; ++index2) {
            if (index === index2) {
              continue;
            }
            var target = copyArray[index2];
            if (lambdaTitle === target) {
              return [false, lambdaTitle, tasks[i].title];
            }
          }
        }
      }
      return [true, null];
    },

    /**
     * Downlaod graph data - FileType: JSON.
     * @public
     */
    onDownload: function() {
      var serialize = this.graph_controller.serialize();
      var ser_str = JSON.stringify(serialize, null, 4);
      var blob = new Blob([ser_str], { type: "application/json" });
      var downloader = document.createElement("a");
      downloader.style = "display: none";
      downloader.href = URL.createObjectURL(blob);
      var date = new Date();
      var year = date.getFullYear().toString();
      var month = (date.getMonth() + 1).toString();
      var day = date.getDate();
      downloader.download = year + "_" + month + "_" + day + "_" + "graph.json";
      // eslint-disable-next-line no-undef
      downloader.click();
      setTimeout(function() {
        // 다운로드가 안되는 경우 방지
        // eslint-disable-next-line no-undef
      }, 300);
      this.$debug(
        this.name,
        "onDownload",
        "Save Graph Data. File:",
        year + "_" + month + "_" + day + "_" + "graph.json"
      );
    },

    /**
     * Send selected lambda data to Detail setting window.
     * @public
     * @param {object} - selected lambda`s data.
     */
    onSelectLambda: function(lambdaData) {
      /**
       * Select lambda event. Transfer event to DetailSetting.
       * @type {emit}
       * @param {object} - selected lambdas`s data.
       */
      this.$emit("selectedLambda", lambdaData);
    },

    /**
     * Send selceted task data to Detail setting window.
     * @public
     * @param {object} - selected task`s data
     */
    onSelectTask: function(taskData) {
      /**
       * Select task event. Transfer event to DetailSetting.
       * @type {emit}
       * @param {object} - selected task`s data.
       */
      this.$emit("selectedTask", taskData);
    },

    /**
     * Send deselceted lambda event to Detail setting window.
     * @public
     */
    onDeselectLambda: function() {
      /**
       * Deselect lambda event. Transfer event to DetailSetting. (For detail setting initialize.)
       * @type {emit}
       * @param {boolean} - Static value (true).
       */
      this.$emit("deselectedLambda", true);
    },

    /**
     * Send deselceted task event to Detail setting window.
     * @public
     */
    onDeselectTask: function() {
      /**
       * Deselect task event. Transfer event to DetailSetting. (For detail setting initialize.)
       * @type {emit}
       * @param {boolean} - Static value (true).
       */
      this.$emit("deselectedTask", true);
    },

    /**
     * Open local file finder when select ok in CheckDialog.
     * @public
     */
    onOpenLocalFile: function() {
      this.checkLocal = true;
      this.checkMessgaes = ["warn_olddata_clear", "ques_want_continue"];
      this.checkDialog = true;
    },

    /**
     * Save Graph To API.
     * @public
     */
    onSaveGraph: function() {
      var result = this.graph_controller.serialize();
      if (this.checkDuplicate(result)) {
        if (result.nodes.length === 0) {
          // if node`s number is zero, No save graph.
          this.alertMsg(this.alert_colors.error, [
            this.$t("lambda_is_not_exist"),
          ]);
          this.$warn(this.name, "onSaveGraph", this.$t("lambda_is_not_exist"));
          return;
        }
        if (result.tasks.length === 0) {
          // if task`s number is zero, No save graph.
          this.alertMsg(this.alert_colors.error, [
            this.$t("task_is_not_exist"),
          ]);
          this.$warn(this.name, "onSaveGraph", this.$t("task_is_not_exist"));
          return;
        }

        // initialize_only 일 경우 save 후 read_only 로 변경
        // for (let index = 0; index < result.nodes.length; ++index) {
        //   for (let j = 0; j < result.nodes[index].properties.length; ++j) {
        //   if (result.nodes[index].properties[j].rule) {
        //     if (result.nodes[index].properties[j].rule === "initialize_only") {
        //     result.nodes[index].properties[j].rule = "read_only";
        //     }
        //   }
        //   }
        // }

        this.isPlaying = true;
        this.save_data = result;
        this.saveSignal = true; // send signal.
        this.alertMsg(this.alert_colors.default, [this.$t("please_wait")]);
      } else {
        // save & play failed.
      }
    },

    /**
     * Open CheckDialog for All delete graph canvas data.
     * @public
     */
    onClearGraph: function() {
      this.checkMessgaes = ["warn_alldata_clear", "ques_want_delete"];
      this.checkDialog = true;
    },

    /**
     * Cancel Event in CheckDialog - Stop Event.
     * @public
     */
    onCheckCancel: function() {
      this.checkDialog = false;
    },

    /**
     * OK Event in CheckDialog - Continue Event.
     * @public
     */
    onCheckOk: function() {
      if (this.checkLocal) {
        this.LoadLocalFile();
        this.checkLocal = false;
      } else {
        this.clearGraph();
      }
      this.checkDialog = false;
    },

    /**
     * Graph canvas`s resize event.
     * @public
     */
    // eslint-disable-next-line no-unused-vars
    onResize: function(event) {
      if (this.resize_ready) {
        var set_canvas = this.$refs.mycanvas;
        set_canvas.width = set_canvas.clientWidth;
        set_canvas.height = set_canvas.clientHeight;
        this.graph_canvas.setCanvas(set_canvas);
        this.graph_controller.change();
      }
    },
  },

  created() {
    this.installGraph();
  },

  mounted() {
    this.alertMsg(this.alert_colors.default, [this.$t("loading") + "..."], 0);

    if (this.$templateStore.getters["getLambdaTemplates"].length == undefined) {
      this.getBoxSignal = true;
    } else {
      this.addLambda(this.$templateStore.getters["getLambdaTemplates"]);
      this.initialize();
    }
  },

  beforeDestroy() {
    if (this.graph_controller) {
      this.graph_controller = null;
    }
    if (this.graph_canvas) {
      this.graph_canvas = null;
    }
    if (this.statusTimer) {
      clearInterval(this.statusTimer);
      this.statusTimer = null;
    }
  },

  // vue-rx async part.
  subscriptions() {
    const $getBoxSignal = this.$watchAsObservable("getBoxSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((getBoxSignal) => getBoxSignal == true); // if signal is true.
    const $saveSignal = this.$watchAsObservable("saveSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((saveSignal) => saveSignal == true); // if signal is true.
    const $load_signal = this.$watchAsObservable("load_signal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((load_signal) => load_signal == true);
    const $statusSignal = this.$watchAsObservable("statusSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((statusSignal) => statusSignal == true);
    return {
      main_result: Observable.combineLatest($getBoxSignal, (getBoxSignal) => ({
        getBoxSignal,
        // eslint-disable-next-line no-unused-vars
      })).flatMap(({ getBoxSignal }) =>
        this.$api
          .getLambdaTemplates(this.$store.getters["user/getAccessToken"])
          .do((res) => {
            this.$debug(
              this.name,
              "subscriptions::getLambdaTemplates",
              "Response:",
              res.result.obj
            );

            this.$templateStore.commit("setLambdaTemplates", res.result.obj);

            this.addLambda(res.result.obj);
            this.initialize();
          })
          .catch((err) => {
            // // For test.
            // var obj = require("@/components/VisualGraph/test/changeControls.json").obj;
            // this.addLambda(obj);
            // this.initialize();
            this.$error(this.name, "subscriptions::getLambdaTemplates", err);
            if (this.alert) {
              this.alert = false;
            }
            this.$nextTick().then(() => {
              this.alertMsg(this.alert_colors.error, [
                this.$t("load_template_failed"),
              ]);
            });
            return Observable.of(null);
          })
          .do(() => {
            this.$nextTick().then(() => {
              this.getBoxSignal = false;
              if (this.graph_canvas) {
                this.graph_canvas.preventMouseEvent(false);
              }
              // this.disabled_load_btn = false;
              // this.disabled_download_btn = false;
            });
          })
      ),
      saveResult: Observable.combineLatest($saveSignal, (saveSignal) => ({
        saveSignal,
        // eslint-disable-next-line no-unused-vars
      })).flatMap(({ saveSignal }) =>
        this.$api
          .saveLambda(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"],
            this.save_data
          )
          .do((res) => {
            this.$debug(
              this.name,
              "subscriptions::saveLambda",
              "Save Success. Response:",
              res
            );

            if (this.save_data.tasks.length != 1) {
              this.load_signal = true;
            }
          })
          .catch((err) => {
            this.$error(this.name, "subscriptions::saveLambda", err);
            if (this.isPlaying) {
              this.alertMsg(this.alert_colors.error, [
                this.$t("execute_failed"),
              ]);
              this.isPlaying = false;
            } else {
              this.alertMsg(this.alert_colors.error, [this.$t("save_failed")]);
            }
            return Observable.of(null);
          })
          .do(() => (this.saveSignal = false))
      ),
      load_result: Observable.combineLatest($load_signal, (load_signal) => ({
        load_signal,
        // eslint-disable-next-line no-unused-vars
      })).flatMap(({ load_signal }) =>
        this.$api
          .getLambda(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"]
          )
          .do((res) => {
            if (res.result && res.result.obj) {
              this.$debug(
                this.name,
                "subscriptions::getLambda(Load)",
                "Reponse:",
                res.result.obj
              );
              this.setLoadData(res.result.obj);
              if (this.isPlaying) {
                this.alertMsg(this.alert_colors.default, [
                  this.$t("execute_success"),
                ]);
                this.isPlaying = false;
              }
            }
          })
          .catch((err) => {
            this.$error(this.name, "subscriptions::getLambda", err);
            if (this.isPlaying) {
              this.alertMsg(this.alert_colors.error, [
                this.$t("execute_failed"),
              ]);
              this.isPlaying = false;
            } else {
              this.alertMsg(this.alert_colors.error, [this.$t("load_failed")]);
            }
            return Observable.of(null);
          })
          .do(() => {
            this.load_signal = false;
          })
      ),
      statusResult: Observable.combineLatest($statusSignal, (statusSignal) => ({
        statusSignal,
        // eslint-disable-next-line no-unused-vars
      })).flatMap(({ statusSignal }) =>
        this.$api
          .getGraphStatus(
            this.$store.getters["user/getAccessToken"],
            null,
            this.$store.getters["project/getSelectProject"]
          )
          .do((res) => {
            this.$debug(
              this.name,
              "subscriptions::getGraphStatus",
              "Reponse:",
              res
            );
            var result = {};
            var response = res.result.obj;
            if (response.tasks) {
              var tasks = response.tasks;
              for (var task of tasks) {
                result[task.name] = task.state;
              }
            }
            this.jsonData = result;
          })
          .catch((err) => {
            this.$error(this.name, "subscriptions::getGraphStatus", err);
            return Observable.of(null);
          })
          .do(() => {
            this.statusSignal = false;
          })
      ),
    };
  },
};
</script>

<style scoped>
#canvas_main {
  width: 100%;
  height: 100%;
}
#mycanvas {
  width: 100%;
  /* top: 24px; */
  /* height: calc(100% - 24px); */
  height: calc(100% - 42px);
  /* height: 500px; */
  position: absolute;
  /* border: 1px solid red; */
}
#alert {
  width: 300px;
  height: 100%;
  border: 1px solid rgba(125, 125, 125, 0.5);
}
.v-toolbar >>> .v-toolbar__content {
  padding: 0 0 0 0;
  padding-left: 15px;
  padding-right: 15px;
  /* padding-right: 5px; */
}
</style>
