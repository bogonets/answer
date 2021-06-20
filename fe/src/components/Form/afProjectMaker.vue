<template>
	<v-card :class="activeClass">
		<v-progress-linear v-if="duplicatedSignal || createSignal" :indeterminate="true" height="5" class="loadingbar"></v-progress-linear>
		<v-card-title v-if="useTitle">
			<span class="headline">{{ title ? title : $t('create_project.new_project') }}</span>
		</v-card-title>
		<v-divider v-if="useTitle"></v-divider>
		<v-card-text class="pa-5">
			<v-form>
				<div v-if="useSelection" class="subtitle">
					<i class="fas fa-star"></i><span>{{ ' ' + $t('demand') }}</span>
					<hr>
				</div>
				<v-text-field
        outlined
				dense
				:hide-details="!projectNameErr"
				:error="projectNameErr"
				:error-messages="projectNameMsg"
				type="text"
				ref="projectName"
				v-model="projectName"
				:label="$t('project_name')"
				@input="onInputProjectname"
				autofocus
				tabindex="1"
				@keypress.enter.stop="onNewProject"
				></v-text-field>
				<div class="duplicated-pane" ref="duplicatedMessage">
					<span v-if="alertMessage" :style="'color: ' + COLORS[duplicated_button_status]">{{ alertMessage }}</span>
				</div>
        <template v-if="useSelection">
          <div class="subtitle">
            <i class="fas fa-check"></i><span>{{ ' ' + $t('selection') }}</span>
            <hr>
          </div>
          <v-radio-group v-model="publicAndPrivate" row dense>
            <v-radio
            :label="$t('public')" :value="'public'">
            </v-radio>
            <v-radio
            :label="$t('private')" :value="'private'">
            </v-radio>
          </v-radio-group>
          <v-textarea
          v-model="description"
          outlined
          dense
          :label="$t('discription')">
          </v-textarea>
        </template>
			</v-form>
		</v-card-text>
		<v-divider></v-divider>
		<v-card-actions>
			<v-btn text @click="onCancel" tabindex="3">{{ $t(cancelText) }}</v-btn>
			<v-spacer></v-spacer>
			<v-btn text color="info" @click="onNewProject" tabindex="2">{{ $t('create') }}</v-btn>
		</v-card-actions>
		<v-snackbar
			v-model="networkErr"
			:timeout="5000"
			top right
		>
			<span :style="'color: ' + COLORS.error">{{ $t('create_project.network_error') }}</span>
			<v-btn text icon @click.stop="networkErr = false"><v-icon>close</v-icon></v-btn>
		</v-snackbar>
	</v-card>
</template>

<script>
import { Observable } from "rxjs";
export default {
	props:{
		/**
		 * Show title.
		 */
		useTitle: {
			type: Boolean,
			default: true
		},
		/**
		 * Activated class (Vuetify css class).
		 */
		activeClass: {
			type: String,
			default: ''
		},
    /**
     * Form title.
     */
		title: {
			type: String,
			default: undefined
    },
    /**
     * use selection options.
     */
    useSelection: {
      type: Boolean,
      default: false
		},
		/**
		 * Cancel button text.
		 */
		cancelText: {
			type: String,
			default: "close"
		}
	},
	components:{

	},
	data(){
		return {
      // Signal.
      duplicatedSignal: false,
      createSignal: false,

      // Project text input timer.
      inputTimer: null,

      // Project name.
      projectName: "",
      projectNameErr: false,
      projectNameMsg: "",

      // Selections.
      publicAndPrivate: "public",
      description: "",

      // Send data to API.
      sendData: {},

      // Messages.
      alertMessage: "",
			alertColor: '#888888FF',
			COLORS: {
				default: "#888888FF",
				success: "rgb(103, 173, 91)",
				error: "rgb(222, 93, 89)"
			},
      networkErr: false,

      // Duplicated.
			duplicated_button_name: this.$t('duplicate_check'),
			duplicated_button_status: 'default',
		}
	},
	computed:{
		demand_duplicate () { // Make sure that you have duplicate checked.
			// if (this.duplicated_button_status === 'success') {
			// 	return true;
			// } else {
			// 	return false;
			// }
			return true;
		}
	},
	methods:{
		/**
		 * Check wrong project name funciton.
		 * @public
		 */
		checkProjectName: function () {
			if (!this.projectName) { // project name empty.
				this.projectNameErr = true;
				this.projectNameMsg = this.$t("create_project.empty_project_name");
				if (this.$refs.projectName) {
					this.$refs.projectName.focus();
				}
				return false;
			}
			return true;
		},

		/**
		 * Check duplicated project name (Send to API).
		 * @public
		 */
		checkDuplicated: function () {
			if (this.inputTimer) {
				clearTimeout(this.inputTimer);
				this.inputTimer = null;
			}
			this.inputTimer = setTimeout(() => {
				if (!this.checkProjectName()) {
					return;
				}
				// [1]
				// this.duplicatedSignal = true;
			}, 300);
		},

		/**
		 * Initialize duplicate project name message and status.
		 * @public
		 */
		onInputProjectname: function () {
			if (this.projectNameErr) {
				this.projectNameErr = false;
				this.projectNameMsg = "";
			}
			if (this.duplicated_button_status !== 'default') {
				this.duplicated_button_name = this.$t("duplicate_check");
				this.duplicated_button_status = "default";
				this.alertMessage = "";
			}
			this.checkDuplicated();
		},

		/**
		 * Close Event (same cancel).
		 * @public
		 */
		onCancel: function () {
      this.projectName = "";
      this.projectNameErr = false;
      this.projectNameMsg = "";
      this.publicAndPrivate = "public";
      this.description = "";
			this.$emit('close');
		},

		/**
		 * Send project data for create project to API.
		 * @public
		 */
		onNewProject: function () {
			if (!this.demand_duplicate) {
        this.onInputProjectname();
				this.focusDuplicate();
				return;
      }
      this.sendData.name = this.projectName;
      if (this.useSelection) {
        if (this.publicAndPrivate === "private") {
          this.sendData.private = true;
        } else {
          this.sendData.private = false;
        }
        this.sendData.description = this.description;
      }
			this.createSignal = true;
    },
    
    /**
     * Animate Duplicated not pass for focus.
     * @public
     */
		focusDuplicate: function () {
			if (this.$refs.duplicatedMessage) {
				var msg = this.$refs.duplicatedMessage;
				if (msg) {
					msg.animate([
						// keyframes
						{ transform: 'translate3d(-1px, 0, 0)' }, 
						{ transform: 'translate3d(2px, 0, 0)' }, 
						{ transform: 'translate3d(-4px, 0, 0)' },
						{ transform: 'translate3d(4px, 0, 0)' },
					], { 
						// timing options
						duration: 200,
						iterations: 3
					});
				}
			}
		}
	},
	created(){
	},
	mounted(){
	},
	beforeDestroy(){
		this.inputData = Object.assign({}, this.initData);
		this.onInputProjectname();
		if (this.inputTimer) {
			clearTimeout(this.inputTimer);
			this.inputTimer = null;
		}
	},
	subscriptions() {
		const $createSignal = this.$watchAsObservable("createSignal", {immediate: true})
    .pluck("newValue")
    .filter(createSignal => createSignal == true) // if signal is true.
    const $duplicatedSignal = this.$watchAsObservable("duplicatedSignal", {immediate: true})
    .pluck("newValue")
    .filter(duplicatedSignal => duplicatedSignal == true) // if signal is true.
    return {
      newProject: Observable.combineLatest($createSignal, createSignal => ({createSignal})).flatMap(({createSignal}) =>  
          this.$api.createProject(this.$store.getters["user/getAccessToken"], this.$store.getters["user/getRefreshToken"], this.sendData.name)
          .do(res => {
						this.$emit("success");
						this.onCancel();
          })
          .catch(error => {
            this.networkErr = true;
            this.duplicated_button_status = "error";
            this.alertMessage = this.$t('create_project.network_error');
						this.$emit("error", error);
						return Observable.of(null);
          })
          .do(() => {
						this.signupSignal = false;
          })
      ),
      duplicatedProject: Observable.combineLatest($duplicatedSignal, duplicatedSignal => ({duplicatedSignal})).flatMap(({duplicatedSignal}) =>  
          this.$api.checkDuplicatedProjectname(this.$store.getters["user/getAccessToken"], this.$store.getters["user/getRefreshToken"], this.projectName)
          .do(res => {
						this.$debug(this.$options.name, "subcriptions::checkDuplicatedProjectName", res);
						if (res.obj) {
							if (res.obj.findProject !== null && res.obj.findProject !== undefined) {
								if (res.obj.findProject) {
									this.duplicated_button_name = this.$t('unavailable');
									this.duplicated_button_status = "error";
									this.alertMessage = this.$t("create_project.duplicated_error");
									this.duplicatedSignal = false;
									if (this.$refs.projectName) {
										this.$refs.projectName.focus();
									}
								} else {
									this.duplicated_button_name = this.$t('available');
									this.duplicated_button_status = "success";
									this.alertMessage = this.$t("create_project.duplicated_success");
								}
							}
						}
          })
          .catch(error => {
						// failed.
            this.networkErr = true;
            this.duplicated_button_status = "error";
            this.alertMessage = this.$t('create_project.network_error');
						return Observable.of(null);
          })
          .do(() => {
            this.duplicatedSignal = false;
          })
      )
    }
  }
}
</script>

<style scoped>
.loadingbar {
	margin: 0px;
	position: absolute;
	top: 0px;
}
.subtitle {
	margin-bottom: 10px;
}
.duplicated-pane {
	padding: 5px;
	margin-bottom: 10px;
}
.duplicated-button__default {
	box-shadow:inset 0px -3px 7px 0px #717171FF;
	background:linear-gradient(to bottom, #888888FF 5%, #919191FF 100%);
	background-color:#888888FF;
	border-radius:3px;
	border:1px solid #0b0e07;
	display:inline-block;
	cursor:pointer;
	font-family:Arial;
	font-size:15px;
	padding:1px 2px;
	text-decoration:none;
	text-shadow:0px 1px 0px #263666;
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-webkit-user-select: none;
	-khtml-user-select: none;
	user-select: none;
}
.duplicated-button__default:hover {
	background:linear-gradient(to bottom, #919191FF 5%, #888888FF 100%);
	background-color:#888888FF;
}
.duplicated-button:active {
	position:relative;
	top:1px;
}
.duplicated-button__success {
	box-shadow:inset 0px -3px 7px 0px rgb(93, 153, 71);
	background:linear-gradient(to bottom, rgb(103, 173, 91) 5%, rgb(123, 193, 111) 100%);
	background-color:rgb(103, 173, 91);
	border-radius:3px;
	border:1px solid #0b0e07;
	display:inline-block;
	cursor:pointer;
	font-family:Arial;
	font-size:15px;
	padding:1px 2px;
	text-decoration:none;
	text-shadow:0px 1px 0px #263666;
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-webkit-user-select: none;
	-khtml-user-select: none;
	user-select: none;
}
.duplicated-button__success:hover {
	background:linear-gradient(to bottom, rgb(123, 193, 111) 5%, rgb(103, 173, 91) 100%);
	background-color:rgb(103, 173, 91);
}
.duplicated-button__error {
	box-shadow:inset 0px -3px 7px 0px rgb(202, 73, 69);
	background:linear-gradient(to bottom, rgb(222, 93, 89) 5%, rgb(242, 113, 109) 100%);
	background-color:rgb(222, 93, 89);
	border-radius:3px;
	border:1px solid #0b0e07;
	display:inline-block;
	cursor:pointer;
	font-family:Arial;
	font-size:15px;
	padding:1px 2px;
	text-decoration:none;
	text-shadow:0px 1px 0px #263666;
	-ms-user-select: none;
	-moz-user-select: -moz-none;
	-webkit-user-select: none;
	-khtml-user-select: none;
	user-select: none;
}
.duplicated-button__error:hover {
	background:linear-gradient(to bottom, rgb(242, 113, 109) 5%, rgb(222, 93, 89) 100%);
	background-color:rgb(222, 93, 89);
}
</style>
