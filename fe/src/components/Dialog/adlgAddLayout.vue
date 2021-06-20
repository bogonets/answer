<template>
  <v-dialog
    :dark="this.$vuetify.theme.dark"
    v-model="open_add_layout"
    persistent
    max-width="290"
  >
    <v-card class="mx-auto" @keypress.enter.stop="onOk">
      <v-card-title class="headline">{{$t('add_layout')}}</v-card-title>
      <v-divider></v-divider>
      <v-card-text style="padding: 10px;">
        <v-text-field
          v-model="name"
          outlined
          prepend-icon="dashboard"
          :label="$t('layout_name')"
          type="text"
          @input="onChangeName"
          hide-details
          ref="layoutname"
          @keypress.enter.stop="onOk"
          @keydown.27.stop="onCancel"
          autofocus
          tabindex="1"
        ></v-text-field>
        <!-- <v-text-field
					v-model="panels"
					prepend-icon="note"
					:label="$t('panels_number')"
					type="tel"
					mask="#"
					@keyup.enter="onEnter"
					@wheel="onWheel"
        ></v-text-field>-->
        <transition name="fade">
          <v-alert
            v-if="alert.show"
            :value="alert.show"
            :type="alert.type"
            :icon="alert.type"
            outlined
            class="alert-style"
          >{{ alert.msg }}</v-alert>
        </transition>
      </v-card-text>
      <!-- <v-divider></v-divider> -->
      <v-card-actions>
        <v-btn text @click="onCancel" tabindex="3">{{$t('cancel')}}</v-btn>
        <v-spacer></v-spacer>
        <v-btn
          text
          @click="onOk"
          :loading="add_layout_signal || exist_check_signal"
          tabindex="2"
        >{{$t('ok')}}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { Observable } from "rxjs";

/**
 * Add Layout Setting Dialog.
 * @author hadoo
 */
export default {
  name: "adlgAddLayout",
  props: {},
  components: {},
  data() {
    return {
      // add_layout_signal: false,
      name: "",
      panels: 1,
      exist_check_signal: false,
      add_layout_signal: false,

      alert: {
        show: false,
        type: "error",
        msg: ""
      }
    };
  },
  methods: {
    /**
     * Show Alert Message.
     * @public
     * @param {string} - Alert type. [success, warning, error, info]
     * @param {string} - Display message.
     * @param {number} - Delete time.
     */
    showAlert: function(type, msg, timeout) {
      var time = timeout || 3500;
      this.alert.show = true;
      this.alert.type = type;
      this.alert.msg = msg;
    },
    /**
     * Hide Alert Message.
     * @public
     */
    hideAlert: function() {
      this.alert.show = false;
      this.alert.msg = "";
    },
    /**
     * Change Event about changed layout name. for hide alert.
     * @public
     */
    onChangeName: function() {
      this.hideAlert();
    },
    /**
     * Enter Key event on textfiled of type number.
     * @public
     */
    onEnter: function() {
      this.onOk();
    },
    /**
     * Mouse Wheel event on textfield of type number.
     * @public
     * @param {mouseWheelEvent}
     */
    onWheel: function(event) {
      if (event.deltaY > 0) {
        if (this.panels == 1) {
          return;
        }
        --this.panels;
      } else {
        if (this.panels == 9) {
          return;
        }
        ++this.panels;
      }
    },

    /**
     * Cancel event. Close Dialog.
     * @public
     */
    onCancel: function() {
      this.$store.commit("drawer/setOpenAddLayout", { bool: false });
    },
    /**
     * Ok or Apply. Make Layout and close dialog.
     * @public
     */
    onOk: function() {
      if (Number(this.panels) <= 0) {
        alert("Panel must be greater than 0.");
        this.panels = 1;
        return;
      } else if (this.checkSpecialCharacter()) {
        this.showAlert("error", this.$t("Special Character not allowed!!"));
        return;
      } else if (this.name == "") {
        this.showAlert("error", this.$t("layout_errors.empty_name"));
        return;
      }
      this.exist_check_signal = true;
    },

    /**
     * Make Intialization Layout data.
     * @public
     * @return {object} - Added new layout data.
     */
    makeAddLayoutData: function() {
      var body = {};
      var panels = [];
      for (var count = 0; count < this.panels; ++count) {
        var panel = this.$store.getters["dashboard/getDefaultPanel"];
        panel.id = "" + Math.random() + "" + Math.random(); // uid.
        panel.z = count; // z-index.
        panels.push(panel);
      }
      body.name = this.name;
      body.panels = this.$util.dashboard_jTos(panels);
      return body;
    },
    checkSpecialCharacter: function() {
      var pattern_spc = /[/~!@#$%^&*()_+|<>?:{}]/; // 특수문자
      if (pattern_spc.test(this.name)) {
        return true;
      }
      return false;
    }
  },
  computed: {
    open_add_layout() {
      return this.$store.getters["drawer/getOpenAddLayout"];
    }
  },
  watch: {
    open_add_layout() {
      if (this.open_add_layout) {
        this.$nextTick().then(() => {
          this.$refs.layoutname.focus();
        });
      }
    }
  },
  created() {},
  mounted() {},
  subscriptions() {
    const $exist_check_signal = this.$watchAsObservable("exist_check_signal", {
      immediate: true
    })
      .pluck("newValue")
      .filter(exist_check_signal => exist_check_signal == true); // if signal is true.

    const $add_layout_signal = this.$watchAsObservable("add_layout_signal", {
      immediate: true
    })
      .pluck("newValue")
      .filter(add_layout_signal => add_layout_signal == true);

    return {
      result: Observable.combineLatest(
        $exist_check_signal,
        exist_check_signal => ({ exist_check_signal })
      ).flatMap(({ exist_check_signal }) =>
        this.$api
          .isExistLayout(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"],
            this.name
          )
          .do(res => {
            // console.log("[AddLayout::subsriptions] ", res);
            if (res.check) {
              this.showAlert("warning", this.$t("layout_errors.existed_name"));
              return Observable.of(null);
            } else {
              this.add_layout_signal = true;
            }
          })
          .catch(err => {
            this.$error(this.$options.name, "[API::isExistlayout]", err);
            this.showAlert("error", this.$t("check_console_log"));
            return Observable.of(null);
          })
          .do(() => {
            this.exist_check_signal = false;
            // this.$store.commit("signal/setAddLayoutSignal", {bool: false});
          })
      ),
      add_result: Observable.combineLatest(
        $add_layout_signal,
        add_layout_signal => ({ add_layout_signal })
      ).flatMap(({ add_layout_signal }) =>
        this.$api
          .createLayout(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["project/getSelectProject"],
            this.makeAddLayoutData()
          )
          .do(res => {
            this.$store.commit("project/setSelectLayout", {
              layoutName: this.name
            });
            this.name = "";
            this.$store.commit("drawer/setOpenAddLayout", { bool: false });
            this.$store.commit("signal/setLayoutMainSignal", { bool: true });
          })
          .catch(err => {
            this.$error(this.$options.name, "[API::createLayout]", err);
            this.showAlert("error", this.$t("check_console_log"));
            return Observable.of(null);
          })
          .do(() => {
            this.add_layout_signal = false;
          })
      )
    };
  }
};
</script>

<style scoped>
/* .v-text-field >>> .v-text-field__details {
	height: 0px !important;
} */
.alert-style {
  /* height: 25px; */
  border-radius: 5px;
  margin-top: 10px;
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
