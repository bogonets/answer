<template>
  <v-card class="main">
    <v-toolbar dense height="30px">
      <v-spacer />
      <slot name="buttonExpantion"></slot>
      <v-btn class="toolbar--button" icon @click.stop="openSettingDialog">
        <v-icon size="20">settings</v-icon>
      </v-btn>
    </v-toolbar>

    <v-dialog
      v-model="openSetting"
      scrollable
      :overlay="false"
      max-width="500px"
      transition="dialog-transition"
      :dark="$vuetify.theme.dark"
    >
      <v-card>
        <v-card-title>{{ $t("setting") }}</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <div v-if="dialog.tasks.length !== 0">
            <span>{{ $t("task") }}:&nbsp;</span>
            <v-select
              :label="$t('task')"
              :items="dialog.tasks"
              item-text="title"
              v-model="dialog.task"
              @change="selectTask"
            ></v-select>
          </div>
          <div v-if="dialog.lambdas.length !== 0">
            <span>{{ $t("lambda") }}:&nbsp;</span>
            <v-select
              :label="$t('lambda')"
              :items="dialog.lambdas"
              item-text="title"
              v-model="dialog.lambda"
              @change="selectLambda"
            ></v-select>
          </div>
          <div v-if="dialog.properties.length !== 0">
            <span>{{ $t("properties") }}:&nbsp;</span>
            <v-select
              :items="dialog.properties"
              item-text="name"
              v-model="dialog.propertyName"
              :label="$t('properties')"
              @change="selectProperty"
            ></v-select>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn small @click="closeSetting">{{ $t("cancel") }}</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            small
            :disabled="!(dialog.task && dialog.lambda && propertyName)"
            @click="saveAndCloseSetting"
            >{{ $t("ok") }}</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- 내용 -->
    <!-- <div>
      <span>{{ type }}&nbsp;</span>
    </div> -->
    <template>
      <v-card
        v-click-outside="{
          handler: onClickOutsideWithConditional,
          closeConditional,
        }"
        @click="conditional = true"
      >
        <v-text-field
          v-if="
            getComponentType(type, lambdaInfo, propertyName) === 'v-text-field'
          "
          :label="propertyName"
          :value="propertyValue"
          v-model="propertyValue"
        ></v-text-field>
        <v-btn
          v-if="
            getComponentType(type, lambdaInfo, propertyName) === 'v-btn' &&
              type == 'props'
          "
          >{{ propertyName }}</v-btn
        >
        <v-select
          v-if="getComponentType(type, lambdaInfo, propertyName) === 'v-select'"
          :label="propertyName"
          :items="property.valid.list"
          v-model="propertyValue"
        ></v-select>
      </v-card>
      <div
        v-if="
          type == 'meta' &&
            getComponentType(type, lambdaInfo, propertyName) === 'rois_control'
        "
        style="width: 100%; height:100%;"
      >
        <rois-widget
          :taskName="task"
          :propertyName="propertyName"
          :lambdaUid="lambdaUid || null"
          :metaData="lambdaInfo.info.meta"
        ></rois-widget>
      </div>
      <div v-else-if="type == 'meta'" style="width: 100%; height: 100%">
        <lambda-widget
          :taskName="task"
          :propertyName="propertyName"
          :lambdaUid="lambdaUid || null"
          :metaData="lambdaInfo.info.meta"
        ></lambda-widget>
      </div>
    </template>
  </v-card>
</template>

<script>
import { Observable } from "rxjs";
import LambdaWidget from "@/components/LambdaWidget/Widget.vue";
import RoisWidget from "@/components/Graph/RoisWidget.vue";

export default {
  name: "acpLambdaViewer",
  props: {
    /**
     * Init Save data from API.
     */
    component_data: {
      default: null,
    },
  },
  components: {
    LambdaWidget,
    RoisWidget,
  },
  data() {
    return {
      openSetting: false,
      dialog: {
        response: null,
        tasks: [],
        task: undefined,
        taskId: undefined,

        lambdas: [],
        lambda: undefined,
        lambdaId: undefined,
        lambdaType: undefined,

        properties: [],
      },

      lambdaInfo: undefined,
      lambdaNtask: null,

      task: undefined,
      taskId: undefined,

      lambda: undefined,
      lambdaId: undefined,
      lambdaUid: undefined,
      lambdaType: undefined,

      type: undefined,
      property: undefined,
      propertyName: undefined,
      propertyValue: undefined,

      componentType: undefined,

      metaData: undefined,

      templateSignal: false,

      showWidget: false,

      conditional: false,
      propertySignal: false,

      self: null,
    };
  },
  computed: {},
  methods: {
    /**
     * Initialize Dialog data And Open Dialog.
     * @public
     */
    openSettingDialog: function() {
      // Initialize Dialog data.
      this.dialog.response = null;
      this.dialog.tasks = [];
      this.dialog.task = undefined;

      this.dialog.lambdas = [];
      this.dialog.lambda = undefined;

      this.dialog.properties = [];
      this.dialog.propertyName = undefined;
      this.dialog.propertyValue = undefined;

      // Open Dialog.
      this.openSetting = true;
    },

    /**
     * Select task event. Find Lambdas of Selected Task.
     * @public
     */
    selectTask: function() {
      this.$debug(
        this.$options.name,
        "selectTask",
        "Select task:",
        this.dialog.task
      );
      this.$debug(
        this.$options.name,
        "selectTask",
        "Tasks:",
        this.dialog.tasks
      );
      this.dialog.lambdas = [];
      this.dialog.properties = [];
      var t = null;
      for (var task of this.dialog.tasks) {
        if (task.title !== this.dialog.task) {
          continue;
        }
        if (task.title === this.dialog.task) {
          var inLambdaIds = task.nodes.slice(); // Lambda id of Selected Task.
          for (var id of inLambdaIds) {
            for (var lambda of this.dialog.response.nodes) {
              if (id === lambda.id) {
                // Find lambda.
                this.dialog.lambdas.push(lambda);
              }
            }
          }
          this.taskId = task.id;
        }
      }
      if (this.dialog.lambdas.length !== 0 && this.lambda) {
        this.dialog.lambda = this.lambda;
        setTimeout(() => {
          // after updated UI.
          this.selectLambda();
        }, 500);
      }
      this.$debug(
        this.$options.name,
        "selectTask",
        "In Lambdas:",
        this.dialog.lambdas
      );
    },

    /**
     * Select lambda event.
     * @public
     */
    selectLambda: function() {
      this.$debug(
        this.$options.name,
        "selectLambda",
        "Select Lambda:",
        this.dialog.lambda
      );
      for (var lambda of this.dialog.lambdas) {
        if (lambda.title !== this.dialog.lambda) {
          continue;
        }
        if (lambda.title === this.dialog.lambda) {
          // property 추가
          this.dialog.properties = this.$util.cloneObject(lambda.properties);

          this.lambdaId = lambda.id;
          this.lambdaUid = lambda.uid;
          this.lambdaType = lambda.type;
          this.lambdaInfo = this.setLambdaInfo(this.lambdaType);

          var templates = this.$templateStore.getters["getLambdaTemplates"];

          // meta 추가
          for (var template of templates) {
            if (
              lambda.type ==
              template.info.category + "/" + template.info.name
            ) {
              if (template.info.meta && template.info.meta.gui)
                this.dialog.properties.unshift(template.info.meta.gui);
            }
          }
        }
      }
      if (this.dialog.properties.length !== 0 && this.propertyName) {
        this.dialog.propertyName = this.propertyName;
      }

      this.$debug(
        this.$options.name,
        "selectLambda",
        "In Property:",
        this.dialog.properties
      );
    },

    selectProperty: function() {
      // properties 에서 name 찾기.
      for (var prop of this.dialog.properties) {
        if (prop.value == this.dialog.propertyName) {
          this.type = "props";
          this.propertyName = prop.name;
          this.propertyValue = prop.value;
        } else if (prop.value === "" && prop.name == this.dialog.propertyName) {
          this.type = "props";
          this.propertyName = prop.name;
          this.propertyValue = undefined;
        } else if (prop.name == this.dialog.propertyName) {
          this.type = "meta";
          this.propertyName = prop.name;
          this.propertyValue = undefined;
        }
      }

      this.property = this.makeCurrentProperty(
        this.type,
        this.propertyName,
        this.lambdaInfo
      );
    },

    /**
     * Close Setting Dialog.
     * @public
     */
    closeSetting: function() {
      this.openSetting = false;
    },

    /**
     * Save Setting Data And Close Setting Dialog.
     * @public
     */
    saveAndCloseSetting: function() {
      // save data.
      this.task = this.dialog.task;
      this.lambda = this.dialog.lambda;
      // close dialog.
      this.closeSetting();
      // save to api.
      this.saveApi();

      this.$debug(
        this.$options.name,
        "saveAndCloseSetting",
        "Select Task:",
        this.task,
        "Select Lambda:",
        this.lambda,
        "Select Property:",
        this.propertyName
      );
    },

    makeMetaComponent: function() {
      var component = {};
      component.name = this.metaData.gui.name;
      this.metaComponent = component;
    },
    /**
     * Trans Save Component Data To API.
     * @param {null}
     * @public
     */
    saveApi: function() {
      var component_data = {};
      if (this.task) {
        component_data.task = this.task;
        component_data.taskId = this.taskId;
      }
      if (this.lambda) {
        component_data.lambda = this.lambda;
        component_data.lambdaId = this.lambdaId;
        component_data.lambdaUid = this.lambdaUid;
        component_data.lambdaType = this.lambdaType;
      }
      if (this.propertyName) {
        component_data.propertyName = this.propertyName;
        component_data.propertyValue = this.propertyValue;
        component_data.type = this.type;
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
    loadApi: function() {
      if (this.component_data) {
        var copy_data = this.$util.cloneObject(this.component_data);
        for (var key in copy_data) {
          switch (key) {
            case "task": {
              this.task = copy_data[key];
              break;
            }
            case "lambda": {
              this.lambda = copy_data[key];
              break;
            }
            case "lambdaId": {
              this.lambdaId = copy_data[key];
              break;
            }
            case "lambdaUid": {
              this.lambdaUid = copy_data[key];
              break;
            }
            case "lambdaType": {
              this.lambdaType = copy_data[key];
              break;
            }
            case "propertyName": {
              this.propertyName = copy_data[key];
              break;
            }
            case "propertyValue": {
              this.propertyValue = copy_data[key];
              break;
            }
            case "type": {
              this.type = copy_data[key];
              break;
            }
          }
        }
      }

      // templateStore 데이터가 없는경우
      if (
        this.$templateStore.getters["getLambdaTemplates"].length == undefined
      ) {
        this.templateSignal = true;
      } else if (this.lambdaType) {
        this.lambdaInfo = this.setLambdaInfo(this.lambdaType);
        this.property = this.makeCurrentProperty(
          this.type,
          this.propertyName,
          this.lambdaInfo
        );
      }
    },

    setLambdaInfo: function(type) {
      for (var obj of this.$templateStore.getters["getLambdaTemplates"]) {
        if (type == obj.info.category + "/" + obj.info.name) {
          return obj;
        }
      }
    },

    // mode : props , meta , ...
    // info : lambdaTemplate (single)
    // name : this.propertyName
    getComponentType: function(mode, lambda, name) {
      if (!(mode && lambda && name)) {
        return null;
      }
      if (mode == "props") {
        for (var prop of lambda.props) {
          if (prop.name == name) {
            return this.getPropFieldType(prop);
          }
        }
      } else if (mode == "meta") {
        return this.getMetaFieldType(lambda.info.meta);
      }
    },

    makeCurrentProperty: function(type, name, lambda) {
      if (type == "props") {
        for (var prop of lambda.props) {
          if (prop.name == name) {
            if (prop.valid && typeof prop.valid === "object") {
              if (prop.valid.hasOwnProperty("list")) {
                if (typeof prop.valid.list === "string") {
                  if (prop.valid.list.includes(";")) {
                    var sep = prop.valid.list.split(";");
                    for (var index = 0; index < sep.length; ++index) {
                      if (sep[index] === "null") {
                        sep[index] = this.$t("null");
                      }
                    }
                    prop.valid.list = sep;
                  }
                }
              }
            }
            return prop;
          }
        }
      } else if (type == "meta") {
        return lambda.info.meta;
      }
    },

    getPropFieldType: function(prop) {
      var textType = ["text", "label", "csv", "str", "int", "float", "double"];

      if (textType.includes(prop.type)) {
        if (prop.valid && typeof prop.valid === "object") {
          if (prop.valid.hasOwnProperty("list")) {
            return "v-select";
          }
        }
        return "v-text-field";
      }

      // else if(prop.type === "btn")
      // ...
      // else if(prop.type === "color")
      // ...
      else return "v-text-field";
    },

    getMetaFieldType: function(meta) {
      // gui...
      return meta.gui.name;
    },

    showPropertyWidget: function() {
      this.showWidget = true;
    },

    onClickOutsideWithConditional() {
      this.propertySignal = true;
      this.conditional = false;
    },
    closeConditional(e) {
      return this.conditional;
    },
  },
  created() {
    /* EMPTY */
  },

  mounted() {
    this.loadApi();
  },

  beforeDestroy() {},

  subscriptions() {
    const $openSetting = this.$watchAsObservable("openSetting", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((openSetting) => openSetting == true); // if signal is true.

    const $templateSignal = this.$watchAsObservable("templateSignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((templateSignal) => templateSignal == true);

    const $propertySignal = this.$watchAsObservable("propertySignal", {
      immediate: true,
    })
      .pluck("newValue")
      .filter((propertySignal) => propertySignal == true);

    return {
      setProps: Observable.combineLatest($propertySignal, (propertySignal) => ({
        propertySignal,
      })).flatMap(({ propertySignal }) =>
        this.$api
          .setPropertyValue(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.task,
            this.lambdaUid,
            this.propertyName,
            this.propertyValue
          )
          .do((res) => {
            this.saveApi();
          })
          .catch((error) => {})
          .do(() => {
            this.propertySignal = false;
          })
      ),

      graphInfo: Observable.combineLatest($openSetting, (openSetting) => ({
        openSetting,
      })).flatMap(({ openSetting }) =>
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
              this.dialog.response = this.$util.cloneObject(res.result.obj);
              this.dialog.tasks = this.$util.cloneObject(
                this.dialog.response.tasks
              );
              if (this.task) {
                setTimeout(() => {
                  this.dialog.task = this.task;
                  this.selectTask();
                }, 500);
              }
            }
          })
          .catch((err) => {
            this.$error(this.name, "subscriptions::getLambda", err);
            return Observable.of(null);
          })
          .do(() => {
            // this.load_signal = false;
          })
      ),
      templateResult: Observable.combineLatest(
        $templateSignal,
        (templateSignal) => ({
          templateSignal,
        })
      ).flatMap(({ templateSignal }) =>
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

            if (this.lambdaType) {
              this.lambdaInfo = this.setLambdaInfo(this.lambdaType);
              this.property = this.makeCurrentProperty(
                this.type,
                this.propertyName,
                this.lambdaInfo
              );
            }
          })
          .catch((err) => {
            this.$error(this.name, "subscriptions::getLambdaTemplates", err);
          })
          .do(() => {
            this.templateSignal = false;
          })
      ),
    };
  },
};
</script>

<style scoped>
.v-toolbar:hover {
  cursor: move;
}
.v-toolbar >>> .v-toolbar__content {
  padding: 0 10px !important;
}
.toolbar--button {
  width: 20px;
  height: 20px;
}
.main {
  width: 100%;
  height: 100%;
}
#img_parent {
  position: absolute;
  width: 100%;
  height: calc(100% - 30px);
  top: 30px;
}
</style>
