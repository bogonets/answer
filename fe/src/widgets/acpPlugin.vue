<template>
  <v-card class="main">
    <v-toolbar dense height="30px">
      <v-spacer />
      <v-tooltip bottom open-delay="1000">
        <template v-slot:activator="{ on }">
          <v-btn
            v-on="on"
            small
            icon
            :disabled="openSetting"
            style="width: 30px; height: 30px; margin: 0 0 0 0"
            @click="onOpenSetting"
          >
            <v-icon size="20">settings</v-icon>
          </v-btn>
        </template>
        <span>{{ $t("setting") }}</span>
      </v-tooltip>
    </v-toolbar>

    <div ref="frame_div" id="frame_div">
      <iframe ref="frame" id="frame" v-if="pluginSrc" :src="pluginSrc"></iframe>
    </div>

    <transition name="fade">
      <div v-if="openSetting" id="dialog">
        <v-card id="dialog__content">
          <v-card-title>{{ $t("select_data") }}</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <v-text-field
              filled
              :label="$t('plugin')"
              append-outer-icon="folder_open"
              @click:append-outer="onLocalFile"
              v-model="cacheData['pluginSrc']"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn @click="onCancelSetting">{{ $t("cancel") }}</v-btn>
            <v-spacer></v-spacer>
            <v-btn @click="onOkSetting">{{ $t("ok") }}</v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </transition>
  </v-card>
</template>

<script>
export default {
  name: "acpPlugin",
  props: {
    /**
     * Init Save data from API.
     */
    component_data: {
      type: Object,
      default: null
    }
  },
  components: {},
  data() {
    return {
      frame: null,
      pluginSrc: null,
      openSetting: false,

      cacheData: { pluginSrc: null }
    };
  },
  computed: {},
  methods: {
    /**
     * Initialize this component.
     * @public
     */
    initialize: function() {
      this.frame = this.$refs.frame;
      this.loadApi();
    },

    /**
     * Open setting dialog.
     * @public
     */
    onOpenSetting: function() {
      this.openSetting = true;
      this.cacheData["pluginSrc"] = this.pluginSrc;
    },

    /**
     * Open finder and select file.
     * @public
     */
    onLocalFile: function() {
      var finder = document.createElement("input");
      finder.setAttribute("type", "file");
      finder.click();
      finder.addEventListener("change", evt => {
        var selectFile = evt.target.files[0];
        var url = URL.createObjectURL(selectFile);
        this.cacheData["pluginSrc"] = url;
      });
    },

    /**
     * Close setting dialog.
     * @public
     */
    onCancelSetting: function() {
      this.openSetting = false;
    },

    /**
     * Apply setting value.
     * @public
     */
    onOkSetting: function() {
      this.openSetting = false;
      this.pluginSrc = this.cacheData["pluginSrc"];
      if (this.pluginSrc.substring(0, 4) === "blob") {
        this.saveApi(false);
      } else {
        this.saveApi(true);
      }
    },

    /**
     * Save this component data to API.
     * @public
     * @param {boolean} - Is save?
     */
    saveApi: function(isSave) {
      var component_data = {};
      if (isSave) {
        component_data["pluginSrc"] = this.pluginSrc;
      } else {
        component_data = {};
      }
      /**
       * Events that occur when component data is stored.
       * @type {Emit}
       */
      this.$emit("component_data", component_data);
    },

    /**
     * Load this component data from API.
     * @public
     */
    loadApi: function() {
      if (this.component_data) {
        var copy_data = this.$util.cloneObject(this.component_data);
        for (var key in copy_data) {
          switch (key) {
            case "pluginSrc": {
              this.pluginSrc = copy_data[key];
            }
          }
        }
      }
    }
  },
  created() {},
  mounted() {
    this.initialize();
  }
};
</script>

<style scoped>
.v-toolbar {
  cursor: move;
}
.v-toolbar >>> .v-toolbar__content {
  padding: 0 5px !important;
}
.main {
  width: 100%;
  height: 100%;
}
#no_img {
  position: absolute;
  width: 100%;
  height: calc(100% - 30px);
  top: 30px;
}
#frame_div {
  position: absolute;
  width: 100%;
  height: calc(100% - 30px);
  top: 30px;
}
#frame {
  position: absolute;
  width: 100%;
  height: 100%;
}
#img_zone {
  width: 100%;
  height: 100%;
}
#dialog {
  position: absolute;
  display: flex;
  flex-wrap: wrap;
  width: 100%;
  height: calc(100% - 30px);
  padding: 15px 15px 15px 15px;
  background-color: rgba(25, 25, 25, 0.7);
  overflow: auto;
  justify-content: center;
  align-content: center;
}
#dialog__content {
  width: auto;
  max-width: 95%;
  max-height: 80%;
}
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
</style>
