<template>
  <v-dialog
    v-model="dialog_show"
    persistent
    width="350"
    :dark="this.$vuetify.theme.dark"
  >
    <v-card>
      <v-card-title primary-title>
        <div>
          <h3 class="headline mb-0">{{ $t(timer_title) }}</h3>
        </div>
      </v-card-title>

      <v-card-text>
        <v-switch
          v-model="onoff"
          :label="onoff ? $t(timer_start) : $t(timer_close)"
        />
        <v-text-field
          v-model="interval"
          :label="$t(timer_second_setting) + ' (' + $t('second') + ')'"
          type="number"
        ></v-text-field>
      </v-card-text>

      <v-card-actions>
        <v-btn @click="onCancel" small>{{ $t("cancel") }}</v-btn>
        <v-spacer />
        <v-btn @click="onApply" small>{{ $t("apply") }}</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
/**
 * Timer Setting Dialog For timer component.
 * @author hadoo
 */
export default {
  name: "adlgTimerSetting",
  props: {
    /**
     * Show and hide dialog.
     */
    dialog: {
      type: Boolean,
      default: false,
    },

    /**
     * Timer Status.
     */
    timer_state: {
      type: Boolean,
      default: false,
    },

    /**
     * Timer interval.
     */
    timer_interval: {
      type: Number,
      default: 5000,
    },
  },
  components: {},
  data() {
    return {
      timer_title: "timer_setting",
      timer_start: "timer_start",
      timer_close: "timer_stop",
      timer_second_setting: "timer_time_setting",
      onoff: false,
      interval: 5000,
      dialog_show: false,
      isShow: false,
    };
  },
  computed: {},
  watch: {
    dialog() {
      if (this.dialog) {
        this.dialog_show = true;
        this.initialize();
      } else {
        this.dialog_show = false;
      }
    },
    isShow() {
      this.$debug(this.$options.name, "watch::isShow", this.isShow);
    },
  },
  methods: {
    /**
     * Apply(Ok) event.
     * @public
     */
    onApply: function() {
      var timer_data = {};
      timer_data.state = this.onoff;
      timer_data.interval = this.interval;
      this.onClose();
      /**
       * For apply event trans.
       * @property {object} - timer setting data.
       */
      this.$emit("onApply", timer_data);
    },

    /**
     * Cancel event.
     * @public
     */
    onCancel: function() {
      this.initialize();
      this.onClose();
    },

    /**
     * Initialize.
     * @public
     */
    initialize: function() {
      this.onoff = this.timer_state;
      this.interval = this.timer_interval;
    },

    /**
     * Close event.
     * @public
     */
    onClose: function() {
      this.dialog_show = false;
      /**
       * For close dialog.
       * @property {boolean} - Change dialog open value to false.
       */
      this.$emit("onClose", false);
    },

    /**
     * Key down event For catch esc, enter event.
     * @public
     * @param {keyEvent}
     */
    onKeydown: function(event) {
      this.$debug(this.$options.name, "onKeydown $event =>", event);
      var code = event.keyCode;
      switch (code) {
        case 27:
          this.onClose();
          break;
        case 13:
          this.onApply();
          break;
        default:
          return;
      }
    },
  },
  created() {},
  mounted() {
    // this.initialize();
  },
};
</script>
<style scoped></style>
