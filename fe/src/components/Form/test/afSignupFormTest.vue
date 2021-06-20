<template>
	<v-card class="elevation-24">
		<v-progress-linear v-if="duplicatedSignal || signupSignal" :indeterminate="true" height="5" class="loadingbar"></v-progress-linear>
		<v-card-title v-if="useTitle">
			<span class="headline">{{ title ? '' : $t('sign_up') }}</span>
		</v-card-title>
		<v-divider v-if="useTitle"></v-divider>
		<v-card-text class="pa-5">
			<v-form>
				<div class="subtitle">
					<i class="fas fa-star"></i><span>{{ ' ' + $t('demand') }}</span>
					<hr>
				</div>
				<v-text-field
				outlined
				:hide-details="!usernameErr"
				:error="usernameErr"
				:error-messages="usernameMsg"
				type="text"
				ref="user_name"
				v-model="inputData.user_name"
				:label="$t('user_name')"
				@input="onInputUsername"
				tabindex="1"
				></v-text-field>
				<div class="duplicated-pane" ref="duplicatedMessage">
					<span v-if="alertMessage" :style="'color: ' + COLORS[duplicated_button_status]">{{ alertMessage }}</span>
				</div>
				<v-text-field
					ref="password"
					v-model="inputData.password"
					:label="$t('password')"
					:error="passwordErr"
					:error-messages="passwordMsg"
					:counter="passwordShow"
					:type="passwordShow ? 'text' : 'password'"
					autocomplete="off"
					:hint="$t('min_greater_4')"
					outlined
					persistent-hint
					@input="onInputPassword"
					:append-icon="passwordShow ? 'visibility' : 'visibility_off'"
					@click:append="passwordShow = !passwordShow"
					tabindex="2"
				></v-text-field>
				<v-text-field
					ref="confirm"
					v-model="inputData.password_confirm"
					:label="$t('password_confirm')"
					:error="confirmErr"
					:error-messages="confirmMsg"
					:counter="confirmShow"
					:type="confirmShow ? 'text' : 'password'"
					:hint="$t('same_password')"
					autocomplete="off"
					outlined
					persistent-hint
					@input="onInputConfirm"
					:append-icon="confirmShow ? 'visibility' : 'visibility_off'"
					@click:append="confirmShow = !confirmShow"
					tabindex="3"
				></v-text-field>
				<div class="subtitle">
					<i class="fas fa-check"></i><span>{{ ' ' + $t('selection') }}</span>
					<hr>
				</div>
				<v-text-field outlined v-model="inputData.email" :label="$t('email')" :rules="[rules.email]" tabindex="4"></v-text-field>
				<v-text-field outlined v-model="inputData.phone" :label="$t('phone_number')" mask="(###) #### - ####" tabindex="5"></v-text-field>
			</v-form>
		</v-card-text>
		<v-divider></v-divider>
		<v-card-actions>
			<v-btn text @click="onCancel" tabindex="7">{{ $t(cancelText) }}</v-btn>
			<v-spacer></v-spacer>
			<v-btn text color="info" @click="onSignup" tabindex="6">{{ $t('sign_up') }}</v-btn>
		</v-card-actions>
		<v-snackbar
			v-model="networkErr"
			:timeout="5000"
			top right
		>
			<span :style="'color: ' + COLORS.error">{{ $t('join_error_message.networkerror') }}</span>
			<v-btn text icon @click.native="networkErr = false"><v-icon>close</v-icon></v-btn>
		</v-snackbar>
	</v-card>
</template>

<script>
import { Observable } from "rxjs";
export default {
	props:{
		useTitle: {
			type: Boolean,
			default: true
		},
		title: {
			type: String,
			default: undefined
		},
		cancelText: {
			type: String,
			default: "close"
		}
	},
	components:{

	},
	data(){
		return {
			inputTimer: null,
			initData: {
				user_name: '',
				password: '',
				password_confirm: '',
				email: '',
				phone: ''
			},
			inputData: {
				user_name: '',
				password: '',
				password_confirm: '',
				email: '',
				phone: ''
			},
			sendData: {
				id: '',
				password: '',
				email: '',
				telephone: ''
			},
			sendData_init: {
				id: '',
				password: '',
				email: '',
				telephone: ''
			},
			usernameErr: false,
			usernameMsg: '',
			passwordErr: false,
			passwordMsg: '',
			passwordShow: false,
			confirmErr: false,
			confirmMsg: '',
			confirmShow: false,
			duplicated_button_name: this.$t('duplicate_check'),
			duplicated_button_status: 'default',
			alertMessage: "",
			alertColor: '#888888FF',
			COLORS: {
				default: "#888888FF",
				success: "rgb(103, 173, 91)",
				error: "rgb(222, 93, 89)"
			},
			duplicatedSignal: false,
			signupSignal: false,
			networkErr: false,
			rules: {
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || this.$t('join_error_message.email_format_error')
        }
      }
		}
	},
	computed:{
		demand_duplicate () { // Make sure that you have duplicate checked.
			if (this.duplicated_button_status === 'success') {
				return true;
			} else {
				return false;
			}
		}
	},
	methods:{
		/**
		 * Check usernmae funciton.
		 * @public
		 */
		checkEmptyUsername: function () {
			if (!this.inputData.user_name) { // username empty.
				this.usernameErr = true;
				this.usernameMsg = this.$t("join_error_message.empty_id");
				if (this.$refs.user_name) {
					this.$refs.user_name.focus();
				}
				return false;
			}
			if (this.inputData.user_name.length < 3) { // username length is less 4.
				this.usernameErr = true;
				this.usernameMsg = this.$t('min_greater_3');
				if (this.$refs.user_name) {
					this.$refs.user_name.focus();
				}
				return false;
			}
			return true;
		},

		/**
		 * Check duplicated username (Send to API).
		 * @public
		 */
		checkDuplicated: function () {
			if (this.inputTimer) {
				clearTimeout(this.inputTimer);
				this.inputTimer = null;
			}
			this.inputTimer = setTimeout(() => {
				if (!this.checkEmptyUsername()) {
					return;
				}
				this.duplicatedSignal = true;
			}, 400);
		},

		/**
		 * Check user password.
		 * @public
		 */
		checkPassword: function () {
			if (!this.inputData.password || this.inputData.password === '') {
				this.passwordErr = true;
				this.passwordMsg = this.$t("join_error_message.empty_password");
				if (this.$refs.password) {
					this.$refs.password.focus();
				}
				return false;
			}
			if (!this.inputData.password_confirm || this.inputData.password_confirm === '') {
				this.confirmErr = true;
				this.confirmMsg = this.$t("join_error_message.empty_password");
				if (this.$refs.confirm) {
					this.$refs.confirm.focus();
				}
				return false;
			}
			if (this.inputData.password.length < 4) {
				this.passwordErr = true;
				this.passwordMsg = this.$t("min_greater_4");
				if (this.$refs.password) {
					this.$refs.password.focus();
				}
				return false;
			}
			if (this.inputData.password !== this.inputData.password_confirm) {
				this.confirmErr = true;
				this.confirmMsg = this.$t('join_error_message.not_match_password');
				if (this.$refs.confirm) {
					this.$refs.confirm.focus();
				}
				return false;
			}
			return true;
		},

		/**
		 * Initialize duplicate username message and status.
		 * @public
		 */
		onInputUsername: function () {
			if (this.usernameErr) {
				this.usernameErr = false;
				this.usernameMsg = "";
			}
			if (this.duplicated_button_status !== 'default') {
				this.duplicated_button_name = this.$t("duplicate_check");
				this.duplicated_button_status = "default";
				this.alertMessage = "";
			}
			this.checkDuplicated();
		},

		/**
		 * Initialize password error message.
		 * @public
		 */
		onInputPassword: function () {
			if (this.passwordErr) {
				this.passwordErr = false;
				this.passwordMsg = "";
			}
		},

		/**
		 * Initialize password confirm error message.
		 * @public
		 */
		onInputConfirm: function () {
			if (this.confirmErr) {
				this.confirmErr = false;
				this.confirmMsg = "";
			}
		},

		/**
		 * Close Event (same cancel).
		 * @public
		 */
		onCancel: function () {
			this.inputData = Object.assign({}, this.initData);
			this.sendData = Object.assign({}, this.sendData_init);
			this.$emit('close');
		},

		/**
		 * Send user data for signup to API.
		 * @public
		 */
		onSignup: function () {
			if (!this.demand_duplicate) {
				this.focusDuplicate();
				return;
			}
			if (!this.checkPassword()) {
				return;
			}
			this.sendData.id = this.inputData.user_name;
			this.sendData.password = this.$util.makeHash(this.inputData.password);
			this.sendData.email = this.inputData.email;
			this.sendData.telephone = this.inputData.phone;
			this.signupSignal = true;
		},
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
		this.onInputUsername();
		this.onInputPassword();
		this.onInputConfirm();
		if (this.inputTimer) {
			clearTimeout(this.inputTimer);
			this.inputTimer = null;
		}
	},
	subscriptions() {
		const $signupSignal = this.$watchAsObservable("signupSignal", {immediate: true})
    .pluck("newValue")
    .filter(signupSignal => signupSignal == true) // if signal is true.
    const $duplicatedSignal = this.$watchAsObservable("duplicatedSignal", {immediate: true})
    .pluck("newValue")
    .filter(duplicatedSignal => duplicatedSignal == true) // if signal is true.
    return {
      signupUser: Observable.combineLatest($signupSignal, signupSignal => ({signupSignal})).flatMap(({signupSignal}) =>  
          this.$api.signupMember(this.$store.getters["user/getAccessToken"], this.$store.getters["user/getRefreshToken"], JSON.stringify(this.sendData))
          .do(res => {
						this.$emit("success");
						this.onCancel();
          })
          .catch(error => {
						this.networkErr = true;
						this.$emit("signupError", error);
						return Observable.of(null);
          })
          .do(() => {
						this.signupSignal = false;
          })
      ),
      duplicatedUser: Observable.combineLatest($duplicatedSignal, duplicatedSignal => ({duplicatedSignal})).flatMap(({duplicatedSignal}) =>  
          this.$api.checkDuplicatedUsername(this.$store.getters["user/getAccessToken"], this.$store.getters["user/getRefreshToken"], this.inputData.user_name)
          .do(res => {
						this.$debug(this.$options.name, "subcriptions::checkDuplicatedUsername", res);
						if (res.obj) {
							if (res.obj.findId !== null && res.obj.findId !== undefined) {
								if (res.obj.findId) {
									this.duplicated_button_name = this.$t('unavailable');
									this.duplicated_button_status = "error";
									this.alertMessage = this.$t("duplicated_username.error");
									this.duplicatedSignal = false;
									if (this.$refs.user_name) {
										this.$refs.user_name.focus();
									}
								} else {
									this.duplicated_button_name = this.$t('available');
									this.duplicated_button_status = "success";
									this.alertMessage = this.$t("duplicated_username.success");
								}
							}
						}
          })
          .catch(error => {
						// failed.
						this.networkErr = true;
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
