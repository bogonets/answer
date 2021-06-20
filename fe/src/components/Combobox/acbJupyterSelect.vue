<template>
  <div>
    <div class="progress-container">
      <v-progress-linear v-if="getSignal" class="progress" :indeterminate="true" height="3" color="rgb(136, 241, 162)"></v-progress-linear>
    </div>
    <v-select
    ref="selector"
    class="selector"
    prepend-inner-icon="fab fa-python"
    :disabled="disabled"
    :label="label"
    :value="value"
    :dense="dense"
    :items="items"
    :outlined="outline"
    :solo="solo"
    :filled="box"
    :no-data-text="noData"
    :hide-details="false"
    :error-messages="errorMessage"
    :error="error"
    @mouseenter.native="onRetry"
    @input="changeValue($event)"
    >
    </v-select>
  </div>
</template>

<script>
/**
 * Dynamic item select FROM core jupyter data.
 * @author hadoo
 */
import { Observable } from "rxjs";
export default {
  name: "acbJupyterSelect",
  props:{
    /**
     * This component label.
     */
    label: {
      type: String,
      default: "Jupyter"
    },
    /**
     * Vuetify 1.5 Input style Outline mode.
     */
    outline: {
      type: Boolean,
      default: true
    },
    /**
     * Vuetify 1.5 Input style Box mode.
     */
    box: {
      type: Boolean,
      default: false
    },
    /**
     * Vuetify 1.5 Input style solo mode.
     */
    solo: {
      type: Boolean,
      default: false
    },
    /**
     * List dense style.
     */
    dense: {
      type: Boolean,
      default: true
    },
    /**
     * Disabled.
     */
    disabled: {
      type: Boolean,
      default: false
    },
    /**
     * Attached Task name.
     */
    taskName: {
      type: String,
      default: ""
    },
    /**
     * Attached Lambda name.
     */
    lambdaType: {
      type: String,
      default: ""
    },
    /**
     * Used Property name.
     */
    propName: {
      type: String,
      default: ""
    },
    /**
     * Real select data.
     */
    value: {
      type: String
    },
  },
  components:{

  },
  data(){
    return {
      items: [], // Jupyter items.
      error: false, // Error Display.
      errorMessage: "", // Show Error Message Text.
      noData: "loading_data",
      getSignal: false, // Send GetData to API.
    }
  },
  computed:{
  },
  watch:{
  },
  methods:{
    /**
     * When change event, trans data to child v-model
     * @public
     * @param {inputEvent} - change data.
     */
    changeValue: function (val) {
      this.$debug(this.$options.name, "changeValue", "Value:", val);
      /**
       * Trans result data.
       * @type {emit}
       * @param {object} - result data.
       */
      this.$emit("input", val);
    },
    /**
     * Get Jupyter File list.
     * @public
     * @param {mouseEnterEvent} - not used.
     */
    onRetry: function ($event) {
      this.hideError();
      this.noData = this.$t("loading_data");
      this.getSignal = true;
    },
    showError: function (msg) {
      this.error = true;
      this.errorMessage = `Error: ${msg}`
    },
    hideError: function () {
      this.error = false;
    }
    // getTestData: function () {
    //   return new Promise((resolve, reject) => {
    //     try {
    //       var response = {};
    //       response.result = {};
    //       response.result.obj = ['AAA', 'BBB', 'CCC', 'DDD'];
    //       resolve(response);
    //     } catch (err) {
    //       reject(err);
    //     }
    //   })
    // },
    // getTest: function () {
    //   return Observable
    //     .fromPromise(this.getTestData())
    //     .map(response => response)
    //     .catch(error => Observable.throw(error))
    // }
  },
  created(){
    if (this.value) {
      this.getSignal = true;
    }
  },
  mounted(){
    this.noData = this.$t('no_data_table');
  },
  subscriptions() {
		const $getSignal = this.$watchAsObservable("getSignal", {immediate: true})
			.pluck("newValue")
      .filter(getSignal => getSignal == true) // if signal is true.
      // .debounceTime(3000)
		return {
      main_result: Observable.combineLatest($getSignal, getSignal => ({ getSignal }))
      .flatMap(({ getSignal }) =>
				// this.getTest()
				this.$api.getJupyterFiles(this.$store.getters["user/getAccessToken"], this.$store.getters["user/getRefreshToken"], this.lambdaType, this.propName)
					.do(res => {
            this.$debug(this.$options.name, "subscriptions::getJupyterFiles", "Response:", res);
            if (res.status === 'ERROR') {
              this.showError(res.detail);
            } else {
              if (res.result) {
                if (res.result.obj) {
                  this.items = res.result.obj;
                  this.hideError();
                  if (this.value) {
                    var find = this.items.indexOf(this.value);
                    if (find < 0) {
                      this.value = "";
                      this.showError('Not found saved value.');
                    }
                  }
                } else {
                  this.showError('Response data is empty.');
                }
              } else {
                this.showError('Response data is empty.');
              }
            }
					})
					.catch(err => {
            this.$error(this.$options.name, "subscriptions::getJupyterFiles", err);
            this.$error(this.$options.name, "subscriptions::getJupyterFiles", "Check TaskName(",   this.taskName, ")");
            this.$error(this.$options.name, "subscriptions::getJupyterFiles", "Check lambdaType(", this.lambdaType, ")");
            this.$error(this.$options.name, "subscriptions::getJupyterFiles", "Check PropName(",   this.propName, ")");
            this.items = [];
            this.showError(err.message);
						return Observable.of(null);
					})
					.do(() => {
						this.getSignal = false;
            this.noData = this.$t('no_data_table');
					})
			)
		};
	}
}
</script>

<style scoped>
/* .selector >>> .v-text-field__details {
  height: 0px;
  max-height: 0px;
  min-height: 0px;
  padding: 0px;
  margin: 0px;
} */
/* .selector >>> .v-input__slot {
  height: 0px !important;
  max-height: 0px !important;
  margin: 0px;
  padding: 0px;
} */
.progress-container {
  position: absolute;
  width: 100%;
  margin-top: 0px;
  padding-left: 2px;
  padding-right: 2px;
}
.progress {
  margin: 0;
  border-radius: 8px;
}
</style>