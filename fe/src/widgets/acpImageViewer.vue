<template>
  <v-card class="main">
    <v-toolbar dense height="30px">
      <v-btn 
      v-if="timer === null"
      :disabled="!(task && lambda && output)"
      class="toolbar--button" 
      icon 
      :loading="sendSignal"
      @click.stop="getImage">
        <v-icon size="20">refresh</v-icon>
      </v-btn>
      <v-spacer/>
      <slot name="buttonExpantion"></slot>
      <v-btn class="toolbar--button" icon @click.stop="openSettingDialog"><v-icon size="20">settings</v-icon></v-btn>
    </v-toolbar>

    <div ref="img_parent" id="img_parent">
      <acv-img-viewer ref="viewer" :isFill="true" :src="imgSrc"></acv-img-viewer>
      <slot name="imageExpantion"></slot>
		</div>

    <v-snackbar 
		v-model="alert" 
		top 
		right 
		absolute 
		multi-line 
		:timeout="alert_timeout" 
		style="opacity: .8; margin: 0; margin-right: 10px; margin-top: 10px">
			<v-layout row wrap style="overflow-y: auto !important; max-height: 80px">
				<v-flex xs12 v-for="msg in alert_msg" :key="msg">
					<span :style="'color:' + alert_color">{{msg}}</span>
				</v-flex>
			</v-layout>
			<v-btn flat @click="alert = false">{{$t('close')}}</v-btn>
		</v-snackbar>

    <v-dialog
      v-model="openSetting"
      scrollable 
      :overlay="false"
      max-width="500px"
      transition="dialog-transition"
      :dark="$vuetify.theme.dark"
    >
      <v-card>
        <v-card-title>
          {{$t('setting')}}
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-text-field
            :label="$t('timer_time_setting') + '(ms)' + ' [' + -1 + ' : ' + $t('timer_stop') + ']'"
            type="number"
            v-model.number="dialog.interval"
          ></v-text-field>
          <div v-if="dialog.tasks.length !== 0">
            <span>{{$t('task')}}:&nbsp;</span><v-select
              :label="$t('task')"
              :items="dialog.tasks"
              item-text="title"
              v-model="dialog.task"
              @change="selectTask"
            ></v-select>
          </div>
          <div v-if="dialog.lambdas.length !== 0">
            <span>{{$t('lambda')}}:&nbsp;</span><v-select
              :label="$t('lambda')"
              :items="dialog.lambdas"
              item-text="title"
              v-model="dialog.lambda"
              @change="selectLambda"
            ></v-select>
          </div>
          <div v-if="dialog.outputs.length !== 0">
            <span>{{$t('output_slot')}}:&nbsp;</span><v-select
              :items="dialog.outputs"
              item-text="name"
              v-model="dialog.output"
              :label="$t('output_slot')"
            ></v-select>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-btn small @click="closeSetting">{{$t('cancel')}}</v-btn>
          <v-spacer></v-spacer>
          <v-btn small :disabled="!(dialog.task && dialog.lambda && dialog.output)" @click="saveAndCloseSetting">{{$t('ok')}}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import acvImgViewer from "@/components/Image/acvSimpleImageViewer.vue";
import { Observable } from "rxjs";
export default {
  name: "acpImageViewer2",
  props:{
    /**
		 * Init Save data from API.
		 */
    component_data: {
      default: null
    }
  },
  components:{
    acvImgViewer,
  },
  data(){
    return {
      imgType: null,
      imgSrc: "",

      openSetting: false,
      dialog: {
        response: null,
        tasks: [],
        task: undefined,
        lambdas: [],
        lambda: undefined,
        outputs: [],
        output: undefined,
        interval: 2000
      },

      task: undefined,
      lambda: undefined,
      output: undefined,

      sendSignal: false,

      timer: null,
      interval: 2000,

      alert: false,
      alert_timeout: 5000,
      alert_msg: [],
      alert_color: "rgb(231, 116, 112)",
			alert_colors: { error: "rgb(231, 116, 112)", warn: "#ffde03", default: null },
    }
  },
  computed:{

  },
  methods:{
    /**
     * Initialize Dialog data And Open Dialog.
     * @public
     */
    openSettingDialog: function () {
      // Initialize Dialog data.
      this.dialog.response = null;
      this.dialog.tasks = [];
      this.dialog.task = undefined;
      this.dialog.lambdas = [];
      this.dialog.lambda = undefined;
      this.dialog.outputs = [];
      this.dialog.output = undefined;
      this.dialog.interval = this.interval;
      // Open Dialog.
      this.openSetting = true;
    },

    /**
     * Select task event. Find Lambdas of Selected Task.
     * @public
     */
    selectTask: function () {
      this.$debug(this.$options.name, "selectTask", "Select task:", this.dialog.task);
      this.$debug(this.$options.name, "selectTask", "Tasks:", this.dialog.tasks);
      this.dialog.lambdas = [];
      this.dialog.outputs = [];
      var t = null;
      for (var task of this.dialog.tasks) {
        if (task.title !== this.dialog.task) {
          continue;
        }
        if (task.title === this.dialog.task) {
          var inLambdaIds = task.nodes.slice(); // Lambda id of Selected Task.
          for (var id of inLambdaIds) {
            for (var lambda of this.dialog.response.nodes) {
              if (id === lambda.id) { // Find lambda.
                this.dialog.lambdas.push(lambda);
              }
            }
          }
        }
      }
      if (this.dialog.lambdas.length !== 0 && this.lambda) {
        this.dialog.lambda = this.lambda;
        setTimeout(() => { // after updated UI.
          this.selectLambda();
        }, 500);
      }
      this.$debug(this.$options.name, "selectTask", "In Lambdas:", this.dialog.lambdas);
    },

    /**
     * Select lambda event. Find Output slot of Selected lambda.
     * @public
     */
    selectLambda: function () {
      this.$debug(this.$options.name, "selectLambda", "Select Lambda:", this.dialog.lambda);
      for (var lambda of this.dialog.lambdas) {
        if (lambda.title !== this.dialog.lambda) {
          continue;
        }
        if (lambda.title === this.dialog.lambda) {
          this.dialog.outputs = this.$util.cloneObject(lambda.outputs);
        }
      }
      if (this.dialog.outputs.length !== 0 && this.output) {
        this.dialog.output = this.output;
      }
      this.$debug(this.$options.name, "selectLambda", "In Outputs:", this.dialog.outputs);
    },

    /**
     * Close Setting Dialog.
     * @public
     */
    closeSetting: function () {
      this.openSetting = false;
    },

    /**
     * Save Setting Data And Close Setting Dialog.
     * @public
     */
    saveAndCloseSetting: function () {
      // save data.
      this.task = this.dialog.task;
      this.lambda = this.dialog.lambda;
      this.output = this.dialog.output;
      this.interval = this.dialog.interval;
      // close dialog.
      this.closeSetting();
      // save to api.
      this.saveApi();
      // restart.
      this.clearInterval();
      this.getImage();

      this.$debug(this.$options.name, "saveAndCloseSetting", "Select Task:", this.task, "Select Lambda:", this.lambda, "Select output:", this.output);
    },

    /**
     * Set send signal(image load from API) Repeat(Timer). 
     * @public
     */
    getImage: function () {
      this.sendSignal = true;
      if (this.interval > 0) {
        this.timer = setInterval(() => {
          if (!this.sendSignal) {
            this.sendSignal = true;
          }
        }, this.interval);
      }
      // this.sendSignal = true;
    },

    /**
     * Clear send signal timer.
     * @public
     */
    clearInterval: function () {
      if (this.timer) {
        clearInterval(this.timer);
        this.timer = null;
      }
    },

    /**
		 * Trans Save Component Data To API.
		 * @param {null}
		 * @public
		 */
    saveApi: function () {
      var component_data = {};
      if (this.task) {
        component_data.task = this.task;
      }
      if (this.lambda) {
        component_data.lambda = this.lambda;
      }
      if (this.output) {
        component_data.output = this.output;
      }
      component_data.interval = this.interval;
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
            case "task": {
              this.task = copy_data[key];
              break;
            }
            case "lambda": {
              this.lambda = copy_data[key];
              break;
            }
            case "output": {
              this.output = copy_data[key];
              break;
            }
            case "interval": {
              this.interval = copy_data[key];
              break;
            }
          }
        }
      }
    },
    
    /**
     * Show Alert Message.
     * @public
     * @param {array} - messages.
     * @param {string} - success, error, info, warning.
     * @param {number} - timeout value.
     */
    showAlert: function (alertMsg, alertType, alertTimeout) {
      this.alert_color = alertType ? this.alert_colors[alertType] : this.alert_colors.error;
      this.alert_msg = alertMsg;
      	if (alertTimeout !== 0) {
				this.alert_timeout = alertTimeout || 5000; // default 5 second.
			} else {
				this.alert_timeout = 0; // unlimited.  please this.alert = false --> close.
			}
      this.$nextTick()
      .then(() => {
        this.alert = true;
      })
    }
  },

  created(){ /* EMPTY */  },

  mounted(){
    this.loadApi();
    this.$nextTick()
    .then(() => {
      if (this.task && this.lambda && this.output) {
        this.getImage(); // Auto start.
      }
    })
  },

  beforeDestroy(){
    this.clearInterval();
  },

  subscriptions() {
		const $openSetting = this.$watchAsObservable("openSetting", {immediate: true})
    .pluck("newValue")
    .filter(openSetting => openSetting == true) // if signal is true.
    const $sendSignal = this.$watchAsObservable("sendSignal", {immediate: true})
    .pluck("newValue")
    .filter(sendSignal => sendSignal == true) // if signal is true.
    return {
      graphInfo: Observable.combineLatest($openSetting, openSetting => ({openSetting})).flatMap(({openSetting}) => 
        this.$api.getLambda(this.$store.getters["user/getAccessToken"], this.$store.getters["project/getSelectProject"])
					.do(res => {
						if (res.result && res.result.obj) {
              this.$debug(this.name, "subscriptions::getLambda(Load)", "Reponse:", res.result.obj);
              this.dialog.response = this.$util.cloneObject(res.result.obj);
              this.dialog.tasks = this.$util.cloneObject(this.dialog.response.tasks);
              if (this.task) {
                setTimeout(() => {
                  this.dialog.task = this.task;
                  this.selectTask();
                }, 500);
              }
						}
					})
					.catch(err => {
						this.$error(this.name, "subscriptions::getLambda", err);
						return Observable.of(null);
					})
					.do(() => {
						// this.load_signal = false;
					})
      ),
      imageData: Observable.combineLatest($sendSignal, sendSignal => ({sendSignal})).flatMap(({sendSignal}) => 
        this.$api.getImageFromAPI(this.$store.getters["user/getAccessToken"], this.$store.getters["user/getRefreshToken"], this.$store.getters["project/getSelectProject"], this.task, this.lambda, this.output)
          .do(res => {
            this.$debug(this.name, "subscriptions::getImageFromAPI", "Response:", res);
            this.imgType = res.headers['content-type'];
            var bin = Buffer.from(res.data, 'binary').toString('base64');
            var result = "data:image/*;base64," + bin;
            this.imgSrc = result;
          })
          .catch(err => {
            this.showAlert([this.$t("image_load_failed"), this.$t("network.status_code") + ": " + err.response.status]);
            this.$error(this.name, "subscriptions::indexImage", "RESPONSE:", err.response);
            return Observable.of(null);
          })
          .do(() => this.sendSignal = false )
      )
    }
  }
}
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
