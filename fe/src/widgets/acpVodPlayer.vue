<template>
	<v-card class="main">
		<v-toolbar dense height="30px">
			<v-spacer />
			<v-tooltip bottom open-delay="0" v-model="retry_tooltip">
				<template v-slot:activator="{ on }">
					<v-btn
						v-on="on"
						:disabled="open_retry_setting || open_rtc_setting"
						small
						icon
						style="width: 30px; height: 30px; margin: 0 0 0 0;"
						@click="openRetrySetting"
					>
						<v-icon size="20">av_timer</v-icon>
					</v-btn>
				</template>
        <span>{{$t('reconnect_setting')}}</span>문
      </v-tooltip>
			
			<v-tooltip bottom open-delay="0" v-model="rtc_tooltip">
				<template v-slot:activator="{ on }">
					<v-btn
					  v-on="on"
						:disabled="open_retry_setting || open_rtc_setting"
						small
						icon
						style="width: 30px; height: 30px; margin: 0 0 0 0"
						@click="openRtcSetting"
					>
						<v-icon size="20">settings</v-icon>
					</v-btn>
				</template>
        <span>{{$t('video_setting')}}</span>
      </v-tooltip>
		</v-toolbar>

		<div ref="canvas_parent" class="canvas_parent" style="top: 30px">
			<div style="position: absolute; width: 100%; top: 50%" class="text-center">
				<span>{{$t("please_select_camera")}}</span>
			</div>
			<div class="full-size" :style="style">
				<acv-vod-player ref="answer_player" :video="video" :draw_type="draw_type" :label_setting="label_setting"></acv-vod-player>
				<slot name="videoExpantion">
					<acv-painter ref="answer_painter" :edit="edit" :hide_event="hide_event"></acv-painter>
				</slot>
			</div>
			<v-snackbar v-model="alarm" bottom absolute :timeout="5000" style="opacity: .8;">
				<span :style="'color: ' + alarm_color">{{ alarm_msg }}</span>
				<v-btn flat @click="alarm = !alarm">{{$t('close')}}</v-btn>
			</v-snackbar>
		</div>

		<transition name="fade">
			<div v-if="open_rtc_setting" class="page-dialog">
				<v-card class="page-dialog__content">
					<v-card-title>{{$t('video_setting')}}</v-card-title>
					<v-divider></v-divider>
					<v-card-text>
						<v-checkbox dense class="checkbox" :label="$t('manual') + ' ' + $t('setting') " v-model="isManual"></v-checkbox>
						<v-select
							v-if="isManual === false"
							:items="rtcUrls"
							v-model="rtc_cache_src"
							:label="'url'"
							@change="onSrcChange"
							dense
							outlined
						></v-select>
						<v-text-field
							v-else
							:label="'url'"
							type="text"
							append-outer-icon="send"
							v-model="rtc_cache_src"
							@click:append="onSrcChange"
							dense
							outlined
						></v-text-field>
						<v-select
							v-if="rtc_cache_medias !== null && rtc_cache_medias !== undefined && rtc_cache_medias.length !== 0"
							:items="rtc_cache_medias.audios"
							v-model="rtc_cache_media_audio"
							:label="'audios'"
							dense
							outlined
						></v-select>
						<v-select
							v-if="rtc_cache_medias !== null && rtc_cache_medias !== undefined && rtc_cache_medias.length !== 0"
							:items="rtc_cache_medias.videos"
							v-model="rtc_cache_media_video"
							:label="'videos'"
							dense
							outlined
						></v-select>
						<v-select
							v-if="rtc_cache_medias !== null && rtc_cache_medias !== undefined && rtc_cache_medias.length !== 0"
							:items="rtc_cache_medias.datas"
							v-model="rtc_cache_media_data"
							:label="'datas'"
							dense
							outlined
						></v-select>
						<v-select
						  v-if="rtc_cache_media_data"
							:items="[$t('only_bbox'), $t('only_points'), $t('both_all_see'), $t('none_see')]"
							v-model="rtc_cache_draw_type"
							:label="$t('object_draw_type')"
							dense
							outlined
						></v-select>
					</v-card-text>
					<v-card-actions>
						<v-btn small text @click="onCancelRtcSetting">{{$t('cancel')}}</v-btn>
						<v-spacer></v-spacer>
						<v-btn small text @click="onOkRtcSetting">{{$t('ok')}}</v-btn>
					</v-card-actions>
				</v-card>
			</div>
		</transition>

		<transition name="fade">
			<div v-if="open_retry_setting" class="page-dialog">
				<v-card class="page-dialog__content">
					<v-card-title>{{$t('reconnect_setting')}}</v-card-title>
					<v-divider></v-divider>
						<v-container grid-list-xs>
							<v-layout row wrap>
								<v-flex xs12>
									<v-text-field
										type="number"
										:label="$t('reconnect_interval') + '(millisecond)'"
										v-model.number="retry_interval"
										dense
										outlined
									></v-text-field>
								</v-flex>
								<v-flex xs12>
									<v-text-field
										:disabled="retry_unlimit"
										type="number"
										:label="$t('reconnect_number')"
										v-model.number="retry_number"
										dense
										outlined
									></v-text-field>
									<v-checkbox :label="$t('unlimited')" dense v-model="retry_unlimit"></v-checkbox>
								</v-flex>
							</v-layout>
						</v-container>
					<v-divider></v-divider>
					<v-card-actions>
						<v-spacer></v-spacer>
						<v-btn @click="onOkRetrySetting">{{$t('ok')}}</v-btn>
					</v-card-actions>
				</v-card>
			</div>
		</transition>

		<transition name="fade">
			<div v-if="open_label_setting" class="page-dialog">
				<v-card class="page-dialog__content">
					<v-card-title>
						{{$t('label_setting')}}
					</v-card-title>
					<v-divider></v-divider>
					<v-card-text style="max-height: 300px; overflow: auto">
					<span style="font-size: 13px; margin-top: 20px;">{{$t("label_number") + "(" + label_setting_cache.length + ")"}}</span>
						<template v-if="label_setting_cache.length === 0">
							<v-layout row wrap justify-center align-center>
								<v-btn icon outline @click="label_setting_cache.push({label: null, color: null})"><v-icon>add</v-icon></v-btn>
							</v-layout>
						</template>
						<template v-else>
							<template v-for="(label, index) in label_setting_cache">
								<v-layout row wrap :key="index" align-center>
									<v-flex xs4>
										<v-text-field
											name="name"
											:label="$t('label')"
											id="id"
											v-model="label.label"
											box
										></v-text-field>
									</v-flex>
									<v-flex offset-xs1 xs4>
										<v-text-field
											name="name"
											:label="$t('color')"
											id="id"
											v-model="label.color"
											box
										></v-text-field>
									</v-flex>
									<v-flex xs1>
										<v-btn icon small outline @click="label_setting_cache.splice(index,1)"><v-icon>remove</v-icon></v-btn>
									</v-flex>
									<v-flex xs1>
										<v-btn v-if="index === label_setting_cache.length - 1" icon small outline @click="label_setting_cache.push({label: null, color: null})"><v-icon>add</v-icon></v-btn>
									</v-flex>
								</v-layout>
							</template>
						</template>
					</v-card-text>
					<v-divider></v-divider>
					<v-card-actions>
						<v-btn @click="onCancelLabelSetting">{{$t('cancel')}}</v-btn>
						<v-spacer></v-spacer>
						<v-btn @click="onOkLabelSeting">{{$t('ok')}}</v-btn>
					</v-card-actions>
				</v-card>
			</div>
		</transition>
	</v-card>
</template>

<script>
import acvVodPlayer from "@/components/Canvas/acvVodPlayer.vue";
import acvPainter from "@/components/Canvas/acvPainter.vue";

import * as video_util from "@/services/videoToCanvas";

import { RTCMediaClient } from "@/services/mediaclient.js";
import { setInterval, clearInterval } from "timers";
import { Observable } from "rxjs"
import axios from "axios";

// import * as TEST from "@/components/Test/javascript/test";
export default {
	name: "acpVodPlayer",
	props: {
		/**
		 * Painter on off.
		 */
		edit: {
			type: Boolean,
			default: false
		},
		/**
		 * UI Style options.
		 */
		style_options: {
			type: String,
			default: ""
		},
		/**
		 * Canvas Width.
		 */
		width: {
			type: Number,
			default: 100
		},
		/**
		 * Canvas Width Type [px, %, vw ....].
		 */
		width_type: {
			type: String,
			default: "%"
		},
		/**
		 * Canvas Height.
		 */
		height: {
			type: Number,
			default: 100
		},
		/**
		 * Canvas Height Type [px, %, vw ....].
		 */
		height_type: {
			type: String,
			default: "%"
		},
		/**
		 * Event and Area Drawing all Hide on off.
		 */
		hide_all: {
			type: Boolean,
			default: false
		},
		/**
		 * Init Save data from API.
		 */
		component_data: {
			default: null,
		}
	},
	components: {
		acvVodPlayer,
		acvPainter,
	},
	data() {
		return {
			player: null,
			painter: null,
			video: null, // video element.
			state_paused: false,

			rtc_client: null,
			draw_type: null,
			hide_event: false,

			getRtcSignal: false,

			open_reconnect_setting: false,
			timer: null,
			reconnect_date: null,
			reconnect_state: false,
			reconnect_hour: 0,
			reconnect_minute: 0,

			open_rtc_setting: false,
			isManual: false,
			rtcUrls: [null, "127.0.0.1:8080"],
			src: "",
			medias: null,
			media_audio: null,
			media_video: null,
			media_data: null,
			rtc_tooltip: false,
			rtc_cache_src: null,
			rtc_cache_medias: null,
			rtc_cache_media_audio: null,
			rtc_cache_media_video: null,
			rtc_cache_media_data : null,
			rtc_cache_draw_type: null,

			open_retry_setting: false,
			retry: null,
			retry_interval: 5000,
			retry_count: 0,
			retry_number: 10,
			retry_unlimit: true,
			retry_tooltip: false,

			alarm: false,
			alarm_color: "white",
			alarm_msg: "",

			open_label_setting: false,
			label_setting: [],
			label_tooltip: false,
			label_setting_cache: [],
		};
	},
	computed: {
		style() {
			if (this.style_options == "") {
				return (
					"width:" +
					String(this.width) +
					this.width_type +
					";" +
					"height:" +
					String(this.height) +
					this.height_type +
					";"
				);
			} else {
				return (
					"width:" +
					String(this.width) +
					this.width_type +
					";" +
					"height:" +
					String(this.height) +
					this.height_type +
					";" +
					style_options
				);
			}
		}
	},
	watch: {
		/*
		rtc_cache_src() {
			this.start(this.rtc_cache_src);
		},
		*/
		/*
		src() {
			this.destroy();
			if (this.src != "" && this.src !== null && this.src !== undefined) {
				this.initialize(this.src);
				if (this.media_video) {
					this.onSettingOk();
				} else {
					this.start(this.src);
				}
			} else {
				this.alarmError(this.$t("empty_url"));
			}
		},
		*/
		retry_interval() {
			this.retry_interval = parseInt(this.retry_interval);
		},
		retry_number() {
			this.retry_number = parseInt(this.retry_number);
		},
		open_retry_setting() {
			if (this.open_retry_setting && this.retry_tooltip) {
				this.retry_tooltip = false;
			}
		},
		open_rtc_setting() {
			if (this.open_rtc_setting && this.rtc_tooltip) {
				this.rtc_tooltip = false;
			}
		},
		open_label_setting() {
			if (this.open_label_setting && this.label_tooltip) {
				this.label_tooltip = false;
			}
		}
	},
	methods: {
		/**
		 * Initialize this component. Set ref pointer.
		 * @public
		 */
		initialize: function() {
			this.player = this.$refs.answer_player;
			this.painter = this.$refs.answer_painter;
		},

		/**
		 * Destroy this component.
		 * @public
		 */
		destroy: function() {
			this.video = null;
			this.player = null;
			this.painter = null;
			if (this.rtc_client) {
				this.rtc_client.disconnect();
				this.rtc_client = null;
			}
			if (this.video) {
				this.video.remove();
				this.video = null;
			}
		},

		/**
		 * This not play. Settings for webrtc.
		 * @public
		 * @param {string} - RTC server url.
		 */
		start: function(src) {
			var getter = axios.create({
				baseURL: "http://" + src,
				headers: {},
				timeout: 10000
				});
			getter
				.get("/medias")
				.then(res => {
					// console.log("Get Media response:", res.data);
					this.rtc_cache_medias = res.data;
					return res;
				})
				.catch(err => {
					// console.error("Get Medias Error:", err);
					this.alarmError("Get Medias Error: " + err);
					this.rtc_cache_medias = null;
					this.rtc_cache_media_audio = null;
					this.rtc_cache_media_video = null;
					this.rtc_cache_media_data  = null;
					return err;
				});
		},

		/**
		 * Make rtc configure.
		 * @public
		 * @param {string} - audio value.
		 * @param {string} - video value.
		 * @param {string} - data value.
		 * @param {string} - RTC url.
		 */
		ready: function (audio, video, media_data, src) {
			this.video = video_util.make_virtual_video();
			var config = Object();
			config.video = video;
			config.audio = audio;
			config.data = media_data;
			config.host = src;
			config.verbose = false;
			config.player = this;
			// config.video_element = this.video;
			// config.dynamic_drawer = this.player;
			// config.static_drawer = this.painter;

			return config;
		},

		/**
		 * This play method. connect and play.
		 * @public
		 * @param {config} - read method return value.
		 */
		startRtc: function(config) {
			this.rtc_client = RTCMediaClient(config);
			this.rtc_client.connect();
		},

		/**
		 * Get data from painter. (Shapes)
		 * @public
		 */
		getData: function() {
			var object = this.$refs.answer_painter.getData();
			var width = this.$refs.answer_painter.width;
			var height = this.$refs.answer_painter.height;
			this.convertLineRate(object.lines, width, height);
			this.convertRectRate(object.rects, width, height);
			this.convertPolyRate(object.polys, width, height);
			this.convertArcRate(object.arcs, width, height);
			return object;
		},

		/**
		 * Convert lines origin value to rate value.
		 * @public
		 * @param {array} - lines data.
		 * @param {number} - width of canvas.
		 * @param {number} - height of canvas.
		 */
		convertLineRate: function(lines, width, height) {
			if (!lines) {
				return;
			}
			for (var index = 0; index < lines.length; ++index) {
				lines[index].first_point.x = lines[index].first_point.x / width;
				lines[index].first_point.y = lines[index].first_point.y / height;

				lines[index].second_point.x = lines[index].second_point.x / width;
				lines[index].second_point.y = lines[index].second_point.y / height;
			}
		},

		/**
		 * Convert rectangles origin value to rate value.
		 * @public
		 * @param {array} - rectangles data.
		 * @param {number} - width of canvas.
		 * @param {number} - height of canvas.
		 */
		convertRectRate: function(rects, width, height) {
			if (!rects) {
				return;
			}
			for (var index = 0; index < rects.length; ++index) {
				rects[index].start_point.x = rects[index].start_point.x / width;
				rects[index].start_point.y = rects[index].start_point.y / height;
				rects[index].width = rects[index].width / width;
				rects[index].height = rects[index].height / height;
			}
		},

		/**
		 * Convert polygons origin value to rate value.
		 * @public
		 * @param {array} - polygons data.
		 * @param {number} - width of canvas.
		 * @param {number} - height of canvas.
		 */
		convertPolyRate: function(polys, width, height) {
			if (!polys) {
				return;
			}
			for (var index = 0; index < polys.length; ++index) {
				var poly = polys[index];
				for (var i = 0; i < poly.length; ++i) {
					poly[i].x = poly[i].x / width;
					poly[i].y = poly[i].y / height;
				}
			}
		},

		/**
		 * Convert circles origin value to rate value.
		 * @public
		 * @param {array} - circles data.
		 * @param {number} - width of canvas.
		 * @param {number} - height of canvas.
		 */
		convertArcRate: function(arcs, width, height) {
			if (!arcs) {
				return;
			}
			for (var index = 0; index < arcs.length; ++index) {
				var arc = arcs[index];
				arc.center_point.x = arc.center_point.x / width;
				arc.center_point.y = arc.center_point.y / height;
				arc.radius = arc.radius / width;
			}
		},

		/**
		 * Transfer saved data to painter.
		 * @public
		 * @param {object}
		 */
		setEventAreaToPainter: function (presave_data) {
      this.$nextTick(() => {
        if (this.$refs.answer_painter) {
          this.$refs.answer_painter.loadPresetData(presave_data);
        } else {
          this.$warn(this.name, "setEventAreaToPainter", "Painter is ", this.$refs.answer_painter);
        }
      })
		},

		/**
		 * Painter all clear event.
		 * @public
		 */
		clearAllToPainter: function () {
			this.$refs.answer_painter.clearAll();
		},

		/**
		 * Get painter drwaing data.
		 * @public
		 */
		getAreaData: function () {
			return this.$refs.answer_painter.getData();
		},

		/**
		 * ConvertLines Data for API and Transfer lines data to painter.
		 * @param {list} - Lines info list.
		 * @public
		 */
		convertLinesForAPI: function (lines) {
			return this.$refs.answer_painter.convertLinesForAPI(lines);
		},

		/**
		 * Convert Rectangles Data for API and Transfer rectangles data to painter.
		 * @param {list} - Rectagles info list.
		 * @public
		 */
		convertRectsForAPI: function (rects) {
			return this.$refs.answer_painter.convertRectsForAPI(rects);
		},

		/**
		 * Convert Polygons Data for API and Transfer polygons data to painter.
		 * @param {list} - Polygons info list.
		 * @public
		 */
		convertPolysForAPI: function (polys) {
			return this.$refs.answer_painter.convertPolysForAPI(polys);
		},

		/**
		 * Convert Circles Data for API and Transfer circles data to painter.
		 * @param {list} - Circles info list.
		 * @public
		 */
		convertArcsForAPI: function (arcs) {
			return this.$refs.answer_painter.convertArcsForAPI(arcs);
		},

		/**
		 * Timer event (repeat) for reconnect.
		 * @public
		 */
		onTimer: function () {
			this.reconnect_date = new Date();
			if (this.reconnect_date.getHours() === Number(this.reconnect_hour) && this.reconnect_date.getMinutes() === Number(this.reconnect_minute)) {
				if (this.reconnect_date.getSeconds() > 0 && this.reconnect_date.getSeconds() <= 1) {
					if (!this.reconnect_state) {
						this.reconnect();
					}
				}
			}
			this.timer = setTimeout(this.onTimer, 1000);
		},

		/**
		 * Clear(Destroy) timer.
		 * @public
		 */
		closeTimer: function () {
			if (this.timer) {
				clearTimeout(this.timer);
				this.timer = null;
			}
		},

		/**
		 * Reconnect event.
		 * @public
		 */
		reconnect: function () {
			this.reconnect_state = true;
			// if (!this.reconnect_date) {
			this.reconnect_date = new Date();
			// }
			this.$debug(this.name, "reconect", "RTC Server:", this.src, this.media_video, this.media_audio, this.media_data);
			this.destroy();
			this.initialize();
			this.onSettingOk();
		},

		/**
		 * Save this component data to API.
		 * @public
		 */
		saveApi: function () {
			var component_data = {};
			component_data.draw_type = this.draw_type;
			component_data.audio = this.media_audio;
			component_data.video = this.media_video;
			component_data.data  = this.media_data;
			component_data.src   = this.src;
			component_data.retry_interval = this.retry_interval;
			component_data.retry_number   = this.retry_number;
			component_data.retry_unlimit  = this.retry_unlimit;
			component_data.label_setting  = this.label_setting;
			component_data.isManual       = this.isManual;
			this.$emit("component_data", component_data);
		},

		/**
		 * Clear retry repeat timer.
		 * @public
		 */
		deleteRetry: function () {
			if (this.retry) {
				clearTimeout(this.retry);
				this.retry = null;
			}
		},

		/**
		 * Alarm message level: info.
		 * @public
		 * @param {string} - Message.
		 */
		alarmInfo: function (msg) {
			this.alarm = false;
			setTimeout(()=>{
				this.alarm_color = "white";
				this.alarm_msg = "[" + this.$t("info") + "] " + msg;
				this.alarm = true;
			}, 250);
		},

		/**
		 * Alarm message level: warning.
		 * @public
		 * @param {string} - Message.
		 */
		alarmWarn: function (msg) {
			this.alarm = false;
			setTimeout(()=>{
				this.alarm_color = "yellow";
				this.alarm_msg = "[" + this.$t("warning") + "] " + msg;
				this.alarm = true;
				this.$warn(this.name, "alarmWarn", this.alarm_msg);
			}, 250);
		},

		/**
		 * Alarm message level: error.
		 * @public
		 * @param {string} - Message.
		 */
		alarmError: function (msg) {
			this.alarm = false;
			setTimeout(()=>{
				this.alarm_color = "red";
				this.alarm_msg = msg;
				this.alarm = true;
				this.$error(this.name, "alarmError", this.alarm_msg);
			}, 250);
		},

		/**
		 * Open retry setting dialog.
		 * @public
		 */
		openRetrySetting: function () {
			this.open_retry_setting = true;
		},

		/**
		 * Open RTC setting dialog.
		 */
		openRtcSetting: function () {
			this.rtc_cache_src = this.src;
			var temp_str = JSON.stringify(this.medias);
			var cache = JSON.parse(temp_str);
			this.rtc_cache_medias = cache;
			this.rtc_cache_media_audio = this.media_audio;
			this.rtc_cache_media_video = this.media_video;
			this.rtc_cache_media_data  = this.media_data;
			this.rtc_cache_draw_type   = this.draw_type;
			this.open_rtc_setting = true;
		},

		/**
		 * Open label setting dialog.
		 * @public
		 */
		openLabelSetting: function () {
			this.label_setting_cache.length = 0;
			this.label_setting_cache = this.label_setting.slice();
			this.open_label_setting = true;
		},

		/**
		 * Apply retry setting value.
		 * @public
		 */
		onOkRetrySetting: function () {
			this.saveApi();
			this.open_retry_setting = false;
		},

		/**
		 * Apply RTC setting value.
		 * @public
		 */
		onOkRtcSetting: function () {
			this.src = this.rtc_cache_src;
			var temp_str = JSON.stringify(this.rtc_cache_medias);
			var cache_data = JSON.parse(temp_str);
			this.medias = cache_data;
			this.media_audio = this.rtc_cache_media_audio;
			this.media_video = this.rtc_cache_media_video;
			this.media_data  = this.rtc_cache_media_data;
			this.draw_type   = this.rtc_cache_draw_type;
			this.open_rtc_setting = false;
			this.reconnect();
		},

		/**
		 * Close RTC setting dialog.
		 * @public
		 */
		onCancelRtcSetting: function () {
			this.open_rtc_setting = false;
		},

		/**
		 * Apply label setting value.
		 * @public
		 */
		onOkLabelSeting: function () {
			this.label_setting.length = 0;
			this.label_setting = this.label_setting_cache.slice();
			this.saveApi();
			this.open_label_setting = false;
		},

		/**
		 * Close label setting dialog.
		 * @public
		 */
		onCancelLabelSetting: function () {
			this.open_label_setting = false;
		},

		/**
		 * Apply RTC setting value.
		 * @public
		 */
		onSettingOk: function () {
			var config = this.ready(this.media_audio, this.media_video, this.media_data, "http://" + this.src);
			this.saveApi();
			this.startRtc(config);
		},

		/**
		 * Disconnect event when disconnect RTC server.
		 * @public
		 */
		onDisconnected: function () {
			this.reconnect();
			++this.retry_count;
			this.alarmInfo(this.$t("try_reconnect") + " (" + String(this.retry_count) + ")");
			if (!this.retry_unlimit) {
				if (this.retry_count >= this.retry_number) {
					this.deleteRetry();
					this.alarmWarn(this.$t("check_rtcserver_try_again"));
					return;
				}
			}
			this.retry = setTimeout(this.onDisconnected, this.retry_interval);
		},

		/**
		 * Try Connect event when try connect RTC server.
		 * @public
		 */
		onConnected: function () {
			this.deleteRetry();
			this.retry_count = 0;
			this.alarmInfo(this.$t("start_playing_video"));
		},

		/**
		 * Change event when changed source value. start -> ready -> startRTC
		 * @public
		 */
		onSrcChange: function () {
			this.start(this.rtc_cache_src);
		},
	},
	created() {
	},
	mounted() {
		if (this.hide_all) {
			this.draw_type = "not_both";
			this.hide_event = true;
		}
		if (this.component_data) {
			var copy_data = this.$util.cloneObject(this.component_data);
			var src = null;
			this.medias = {};
			for (var key in copy_data) {
				switch (key) {
					case "src": {
						src = copy_data[key];
						if (!this.rtcUrls.includes(copy_data[key])) {
							this.rtcUrls.push(copy_data[key]);
						}
						break;
					}
					case "audio": {
						this.media_audio = copy_data[key];
						this.medias.audios = [this.media_audio];
						break;
					}
					case "video": {
						this.media_video = copy_data[key];
						this.medias.videos = [this.media_video];
						break;
					}
					case "data": {
						this.media_data = copy_data[key];
						this.medias_datas = [this.media_data];
						break;
					}
					case "retry_interval": {
						this.retry_interval = copy_data[key];
						break;
					}
					case "retry_number": {
						this.retry_number = copy_data[key];
						break;
					}
					case "retry_unlimit": {
						this.retry_unlimit = copy_data[key];
						break;
					}
					case "draw_type": {
						this.draw_type = copy_data[key];
						break;
					}
					case "label_setting": {
						this.label_setting = copy_data[key];
						break;
					}
					case "isManual": {
						this.isManual = copy_data[key];
						break;
					}
					default: {
						this.$warn(this.name, "mounted", "The key(", key, ") is not used.");
						break;
					}
				}
			}
			if (src) {
				this.src = src;
				this.reconnect();
			}
			if (!this.draw_type) {
				this.draw_type = this.$t("both_all_see");
			}
		}
		this.getRtcSignal = true;
	},
	beforeDestroy() {
		this.destroy();
		this.deleteRetry();
		this.closeTimer();
	},
	subscriptions() {
		const $getRtcSignal = this.$watchAsObservable("getRtcSignal", {
			immediate: true
		})
			.pluck("newValue")
			.filter(getRtcSignal => getRtcSignal == true) // if signal is true.
			.debounceTime(1000); // delay 1s.
		return {
			main_result: Observable.combineLatest($getRtcSignal, getRtcSignal => ({
				getRtcSignal
			})).flatMap(({ getRtcSignal }) =>
				this.$api.getRtcHost(this.$store.getters["user/getAccessToken"])
					.do(res => {
						this.$debug(this.name, "subscriptions::main_result", "Response:", res);
						this.rtcUrls = res.result.obj.urls;
						this.rtcUrls.push(null);
						// this.rtcUrls = res.cameras;
					})
					.catch(err => {
						this.$error(this.name, "subscriptions::main_result", err);
						return Observable.of(null);
					})
					.do(() => {
						this.getRtcSignal = false;
					})
			),
		};
	}
};
</script>

<style scoped>
.main {
	width: 100%;
	height: 100%;
}
.v-toolbar:hover {
	cursor: move;
}
.v-toolbar >>> .v-toolbar__content {
	padding: 0 5px !important;
}
.full-size {
	position: absolute;
	/* background-image: url('../../assets/bogonet_logo.png');
	background-size: contain;
	background-position: center center; */
}
.canvas_parent {
	position: absolute;
	width: 100%;
	height: calc(100% - 30px);
}
.dialog-btn {
	margin-top: 0;
	margin-left: 0;
	margin-right: 0;
	margin-bottom: 10;
	width: 100%;
}
.dialog-select {
	border: 1px solid black;
}

.page-dialog {
	position: absolute;
	display: flex;
	flex-wrap: wrap;
	width: 100%;
	height: calc(100% - 30px);
	padding: 15px 15px 15px 15px;
	background-color: rgba(25,25,25,0.7);
	overflow: auto;
	justify-content: center;
	align-content: center;
}
.page-dialog__content {
	width: auto;
	max-width: 95%;
	max-height: 80%;
}
.v-input--selection-controls {
	margin: 0 0 !important;
	padding: 0 0 !important;
}
.v-input >>> .v-messages {
	min-height: 0px !important;
	height: 0px !important;
}
.v-input >>> .v-input__slot {
	margin-bottom: 0px !important;
}
.v-text-field {
	margin-top: 10px;
}
.v-text-field >>> .v-text-field__details {
	margin: 0 0 !important;
	padding: 0 0 !important;
	height: 0 !important;
	max-height: 0 !important;
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