<template>
  <div class="optionZone">
    <v-btn
      :small="small"
      :icon="!!icon && !name"
      :color="color"
      @click="onPropertyWrite"
      :loading="signal"
    >
      <v-icon v-if="!!icon && iconLeft" :left="true">{{ icon }}</v-icon>
      <span v-if="!!name">{{ name }}</span>
      <v-icon v-if="!!icon && iconRight" :right="true">{{ icon }}</v-icon>
    </v-btn>
  </div>
</template>

<script>
import axios from "axios";
import { Observable } from "rxjs";
export default {
  name: "ControlReadButton",
  props: {
    small: {
      type: Boolean,
      default: false
    },
    icon: {
      type: String,
      default: null
    },
    iconLeft: {
      type: Boolean,
      default: true
    },
    color: {
      type: String,
      default: undefined
    },
    name: {
      type: String,
      default: "Write"
    },
    propertyName: {
      type: String,
      default: undefined
    },

    // Auto.
    taskName: {
      type: String,
      default: undefined
    },
    lambdaUid: {
      type: String,
      default: undefined
    },
    sendData: null
  },
  components: {},
  data() {
    return {
      signal: false
    };
  },
  computed: {
    iconRight() {
      return !this.iconLeft;
    }
  },
  methods: {
    onPropertyWrite: function() {
      // this.$debug(this.$options.name, "onPropertyWrite::To API", "AccessToken:", this.$store.getters["user/getAccessToken"]);
      // this.$debug(this.$options.name, "onPropertyWrite::To API", "RefreshToken:", this.$store.getters["user/getRefreshToken"]);
      // this.$debug(this.$options.name, "onPropertyWrite::To API", "Selected Project:", this.$store.getters["project/getSelectProject"]);
      this.$debug(
        this.$options.name,
        "onPropertyWrite::To API",
        "TaskName:",
        this.taskName,
        "LambdaUid:",
        this.lambdaUid,
        "propertyName:",
        this.propertyName
      );
      this.$debug(
        this.$options.name,
        "onPropertyWrite::To API",
        "Send Data:",
        this.sendData
      );
      this.signal = true;

      // Test Check.
      // alert(`TaskName: ${this.taskName}\nLambdaUid: ${this.lambdaUid}\npropertyName:${this.propertyName}\nsendData:${this.sendData}`);
    }
  },
  created() {},
  mounted() {},
  beforeDestroy() {
    this.api = null;
  },
  subscriptions() {
    const $signal = this.$watchAsObservable("signal", { immediate: true })
      .pluck("newValue")
      .filter(signal => signal == true) // if signal is true.
      .debounceTime(1000);
    return {
      getBuckets: Observable.combineLatest($signal, signal => ({
        signal
      })).flatMap(({ signal }) =>
        this.$api
          .setPropertyValue(
            this.$store.getters["user/getAccessToken"],
            this.$store.getters["user/getRefreshToken"],
            this.$store.getters["project/getSelectProject"],
            this.taskName,
            this.lambdaUid,
            this.propertyName,
            this.sendData
          )
          .do(res => {
            // success.
            this.$emit("writeSuccess", this.sendData);
          })
          .catch(error => {
            // failed.
            return Observable.of(null);
          })
          .do(() => {
            this.signal = false;
          })
      )
    };
  }
};
</script>

<style scoped>
.optionZone {
  margin: 5px 10px;
}
</style>
