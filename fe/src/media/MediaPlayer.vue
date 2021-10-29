<i18n lang="yaml">
en:
  status:
    loading: "Loading"
    ice_new: "ICE new"
    ice_gathering: "ICE gathering"
    ice_complete: "ICE complete"
    ice_unknown: "ICE unknown error"
    sdp_exchange: "Exchanging SDP ..."
    negotiation_failed: "Negotiation failed"
    disconnected: "Disconnected"
    server_status_error: "Server status error: {0}"
    invalid: "Settings are required"
    unknown: "Unknown status"

ko:
  status:
    loading: "로딩 중 ..."
    ice_new: "ICE 피어 연결 생성됨"
    ice_gathering: "ICE 후보 수집 중..."
    ice_complete: "ICE 후보 수집 완료"
    ice_unknown: "알 수 없는 ICE 상태"
    sdp_exchange: "SDP 교환 중..."
    negotiation_failed: "Negotiation failed"
    disconnected: "연결이 끊어졌습니다"
    server_status_error: "서버가 비정상 상태 입니다: {0}"
    invalid: "설정이 필요합니다"
    unknown: "알 수 없는 상태"
</i18n>

<template>
  <v-hover v-slot="{ hover }">
    <v-card
        outlined
        tile
        class="media-player"
        @contextmenu="contextmenu"
        :style="mediaPlayerStyle"
    >
      <v-system-bar
          class="status-bar"
          v-if="!hideSystemBar"
          v-show="showSystemBar(hover)"
          absolute
          lights-out
      >
        <v-icon :color="statusIconColor">{{ statusIcon }}</v-icon>
        <span>{{ statusLabel }}</span>

        <v-spacer></v-spacer>
        <v-progress-circular
            v-if="loading || loadingStatusCode"
            size="14"
            width="2"
            indeterminate
        ></v-progress-circular>
        <div v-if="online">
          <v-icon v-if="false">mdi-video-4k-box</v-icon>
          <v-icon v-if="false">mdi-video-off</v-icon>
          <v-icon v-if="false" color="red">mdi-record</v-icon>
          <v-icon>mdi-volume-off</v-icon>
          <v-icon>{{ signalIcon }}</v-icon>
        </div>
      </v-system-bar>

      <div class="media-content">
        <canvas
            v-show="!hideCanvasUser"
            class="canvas-user"
            ref="canvas-user"
            :width="videoWidth"
            :height="videoHeight"
        ></canvas>
        <canvas
            v-show="!hideCanvasMeta"
            class="canvas-meta"
            ref="canvas-meta"
            :width="videoWidth"
            :height="videoHeight"
        ></canvas>

        <video
            v-show="online"
            class="video-player"
            ref="rtc-video"
            autoplay
            muted
            playsinline
            preload="auto"
            @pause="onPause"
            @play="onPlay"
            @resize="onResize"
        ></video>

        <v-img
            v-if="!online"
            class="brand-logo"
            src="@/assets/logo/answer-logo-notext.svg"
            min-width="80px"
            max-width="200px"
            min-height="80px"
            max-height="200px"
            contain
        ></v-img>
      </div>

      <div
          v-if="online && !hideController"
          class="controller"
          v-show="showController(hover)"
      >
        <v-btn icon @click="onClickPlay">
          <v-icon>{{ playIcon }}</v-icon>
        </v-btn>
        <v-progress-linear rounded color="grey"></v-progress-linear>
        <v-btn icon @click="onClickMore">
          <v-icon>mdi-dots-horizontal</v-icon>
        </v-btn>
      </div>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import {Component, Prop, Ref, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import type {VmsDeviceA, RtcOfferQ} from '@/packet/vms';
import {
  TRANSCEIVER_KIND_VIDEO,
  TRANSCEIVER_KIND_AUDIO,
  DATA_CHANNEL_LABEL,
  DEFAULT_RTC_CONFIGURATION,
  DEFAULT_VIDEO_TRANSCEIVER_INIT,
  DEFAULT_AUDIO_TRANSCEIVER_INIT,
  DEFAULT_DATA_CHANNEL_INIT,
  createEmptyVmsDeviceA,
} from '@/packet/vms';

const OFFLINE_MEDIA_PLAYER_HEIGHT = "400px";

const STATUS_LOADING = 0;
const STATUS_ICE_NEW = 1;
const STATUS_ICE_GATHERING = 2;
const STATUS_ICE_COMPLETE = 3;
const STATUS_SDP_EXCHANGE = 4;
const STATUS_ONLINE = 10;
const STATUS_NEGOTIATION_FAILED = -1;
const STATUS_ICE_UNKNOWN = -2;
const STATUS_DISCONNECTED = -3;
const STATUS_SERVER_STATUS_ERROR = -4;
const STATUS_INVALID_PARAMETERS = -5;

function gatheringStateCode(state: RTCIceGatheringState) {
  if (state === 'new') {
    return STATUS_ICE_NEW;
  } else if (state === 'gathering') {
    return STATUS_ICE_GATHERING;
  } else if (state === 'complete') {
    return STATUS_ICE_COMPLETE;
  } else {
    return STATUS_ICE_UNKNOWN;
  }
}

@Component
export default class MediaPlayer extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly hideSystemBar!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideCanvasUser!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideCanvasMeta!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideController!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hoverSystemBar!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hoverController!: boolean;

  @Prop({type: Boolean, default: false})
  readonly useColorPicker!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: String})
  readonly group!: string;

  @Prop({type: String})
  readonly project!: string;

  @Prop({type: Number})
  readonly device!: number;

  @Prop({type: Number})
  readonly width!: number;

  @Prop({type: Number})
  readonly height!: number;

  @Prop({type: Object, default: createEmptyVmsDeviceA})
  readonly value!: VmsDeviceA;

  @Ref('canvas-user')
  canvasUser!: HTMLCanvasElement;

  @Ref('canvas-meta')
  canvasMeta!: HTMLCanvasElement;

  @Ref('rtc-video')
  rtcVideo!: HTMLVideoElement;

  paused = true;
  videoWidth = 0;
  videoHeight = 0;

  statusCode = STATUS_LOADING;
  signalLevel = 0;
  connectionState = '';
  channelState = '';

  rtcConfig = DEFAULT_RTC_CONFIGURATION;
  videoTransceiverInit = DEFAULT_VIDEO_TRANSCEIVER_INIT;
  audioTransceiverInit = DEFAULT_AUDIO_TRANSCEIVER_INIT;
  dataChannelInit = DEFAULT_DATA_CHANNEL_INIT;

  pc?: RTCPeerConnection = undefined;
  channel?: RTCDataChannel = undefined;

  channel_message_working = false;

  mounted() {
    this.paused = this.rtcVideo.paused;

    const group = this.group;
    const project = this.project;
    const device = this.device;

    if (!(group && project && device)) {
      this.statusCode = STATUS_INVALID_PARAMETERS;
      return;
    }

    this.statusCode = STATUS_LOADING;
    (async () => {
      await this.doNegotiate();
    })();
  }

  beforeDestroy() {
    if (this.channel) {
      this.channel.close();
      this.channel = undefined;
    } else {
      console.assert(typeof this.channel === 'undefined');
    }

    if (this.pc) {
      this.pc.close();
      this.pc = undefined;
    } else {
      console.assert(typeof this.pc === 'undefined');
    }
  }

  async doNegotiate() {
    try {
      if (this.channel) {
        this.channel.close();
      }
      if (this.pc) {
        this.pc.close();
      }
      await this.createPeerAndMetaChannel();
      this.statusCode = STATUS_ONLINE;
    } catch (error) {
      this.pc = undefined;
      this.channel = undefined;
      this.statusCode = STATUS_NEGOTIATION_FAILED;
      this.toastError(error);
    }
  }

  async createPeerAndMetaChannel() {
    const group = this.group;
    const project = this.project;
    const device = this.device.toString();
    const ices = await this.$api2.getVmsDeviceRtcIces(group, project, device);

    const iceServers = [] as Array<RTCIceServer>;
    for (const ice of ices) {
      let credentialType: undefined | 'password' | 'oauth' = undefined;
      if (typeof ice.credential_type !== 'undefined') {
        if (ice.credential_type === 'password') {
          credentialType = 'password';
        } else if (ice.credential_type === 'oauth') {
          credentialType = 'oauth';
        }
      }
      iceServers.push({
        urls: ice.urls,
        username: ice.username,
        credential: ice.credential,
        credentialType: credentialType,
      });
    }

    const rtcConfig = {
      ...this.rtcConfig,
      iceServers: iceServers,
    } as RTCConfiguration;

    this.pc = new RTCPeerConnection(rtcConfig);
    this.pc.ontrack = this.onTrack;
    this.pc.addTransceiver(TRANSCEIVER_KIND_VIDEO, this.videoTransceiverInit);
    // pc.addTransceiver(TRANSCEIVER_KIND_AUDIO, this.audioTransceiverInit);

    this.channel = this.pc.createDataChannel(DATA_CHANNEL_LABEL, this.dataChannelInit);
    this.channel.onopen = this.onChannelOpen;
    this.channel.onclose = this.onChannelClose;
    this.channel.onmessage = this.onChannelMessage;
    this.channel.onerror = this.onChannelError;

    const offer = await this.pc.createOffer();
    await this.pc.setLocalDescription(offer);

    // ----------------------------------------
    // [IMPORTANT] Do not change the call order
    await this.waitToCompleteIceGathering(this.pc);
    this.pc.onicegatheringstatechange = this.onIceGatheringStateChange;
    this.pc.onconnectionstatechange = this.onConnectionStateChange;
    // ----------------------------------------

    this.statusCode = STATUS_SDP_EXCHANGE;

    const body = {
      type: this.pc.localDescription?.type || '',
      sdp: this.pc.localDescription?.sdp || '',
    } as RtcOfferQ;
    const answer = await this.$api2.postVmsDeviceRtcJsep(group, project, device, body);
    const answerInit = {
      type: answer.type,
      sdp: answer.sdp,
    } as RTCSessionDescriptionInit;
    await this.pc.setRemoteDescription(answerInit);

    // interface RTCPeerConnectionEventMap {
    // "connectionstatechange": Event;
    // "datachannel": RTCDataChannelEvent;
    // "icecandidate": RTCPeerConnectionIceEvent;
    // "icecandidateerror": RTCPeerConnectionIceErrorEvent;
    // "iceconnectionstatechange": Event;
    // "icegatheringstatechange": Event;
    // "negotiationneeded": Event;
    // "signalingstatechange": Event;
    // "statsended": RTCStatsEvent;
  }

  onTrack(event: RTCTrackEvent) {
    if (event.track.kind == TRANSCEIVER_KIND_VIDEO) {
      this.rtcVideo.srcObject = event.streams[0];
    } else if (event.track.kind == TRANSCEIVER_KIND_AUDIO) {
      // this.audio.srcObject = event.streams[0];
    }
  }

  onIceGatheringStateChange(event: Event) {
    const peer = event.target as RTCPeerConnection;
    gatheringStateCode(peer.iceGatheringState);
  }

  onConnectionStateChange(event: Event) {
    const peer = event.target as RTCPeerConnection;
    this.connectionState = peer.connectionState;
  }

  onChannelOpen() {
    console.debug(`Channel opened.`);
    if (typeof this.channel === 'undefined') {
      return;
    }
  }

  onChannelClose() {
    console.debug(`Channel closed.`);
  }

  onChannelMessage(event: MessageEvent) {
    if (this.channel_message_working) {
      return;  // Now working ...
    }

    const canvasWidth = this.canvasMeta.width;
    const canvasHeight = this.canvasMeta.height;
    const context = this.canvasMeta.getContext('2d');
    if (!context) {
      return;
    }

    this.channel_message_working = true;
    (async () => {
      try {
        const content = JSON.parse(event.data);
        context.clearRect(0, 0, canvasWidth, canvasHeight);
        await this.onRenderMetaData(context, canvasWidth, canvasHeight, content);
      } catch (error) {
        context.clearRect(0, 0, canvasWidth, canvasHeight);
        this.predict([]);
      } finally {
        this.channel_message_working = false;
        if (this.channel) {
          this.channel.send(JSON.stringify({code: 0}))
        }
      }
    })();
  }

  async onRenderMetaData(
      context: CanvasRenderingContext2D,
      canvasWidth: number,
      canvasHeight: number,
      content: any,
  ) {
    //   const x1 = canvasWidth * obj.x1;
    //   const y1 = canvasHeight * obj.y1;
    //   const x2 = canvasWidth * obj.x2;
    //   const y2 = canvasHeight * obj.y2;
    //   const w = x2 - x1;
    //   const h = y2 - y1;
    //   const score = obj.score;
    //   const success = obj.success;
    //
    //   if (success) {
    //     context.strokeStyle = 'green';
    //   } else {
    //     context.strokeStyle = 'orange';
    //   }
    //
    //   context.lineWidth = 3;
    //   context.strokeRect(x1, y1, w, h);
    //   context.fillText(`${score}`, x1, y1);
    //
    //   this.predict([obj]);
  }

  onChannelError(event: RTCErrorEvent) {
    console.error(`Data channel error: ${event.error.errorDetail}`);
  }

  waitToCompleteIceGathering(pc: RTCPeerConnection) {
    return new Promise(resolve => {
      this.statusCode = gatheringStateCode(pc.iceGatheringState);
      if (pc.iceGatheringState === 'complete') {
        return resolve();  // DONE !!
      }

      const stateChangeCallback = () => {
        this.statusCode = gatheringStateCode(pc.iceGatheringState);
        if (pc.iceGatheringState === 'complete') {
          pc.removeEventListener('icegatheringstatechange', stateChangeCallback);
          this.statusCode = STATUS_ICE_COMPLETE;
          return resolve();  // DONE !!
        }
      };

      pc.addEventListener('icegatheringstatechange', stateChangeCallback);
    });
  }

  get mediaPlayerStyle() {
    if (this.online) {
      return {};
    } else {
      return {
        height: OFFLINE_MEDIA_PLAYER_HEIGHT,
      };
    }
  }

  requestFullScreen() {
    this.rtcVideo.requestFullscreen();
  }

  showSystemBar(hover?: boolean) {
    if (this.hoverSystemBar) {
      return !!hover;
    }
    return true;
  }

  showController(hover?: boolean) {
    if (this.hoverController) {
      return !!hover;
    }
    return true;
  }

  get online() {
    return this.statusCode === STATUS_ONLINE;
  }

  get loadingStatusCode() {
    switch (this.statusCode) {
      case STATUS_LOADING:
        return true;
      case STATUS_ICE_NEW:
        return true;
      case STATUS_ICE_GATHERING:
        return true;
      case STATUS_ICE_COMPLETE:
        return true;
      case STATUS_SDP_EXCHANGE:
        return true;
      // ----------------------
      case STATUS_ONLINE:
        return false;
      case STATUS_NEGOTIATION_FAILED:
        return false;
      case STATUS_ICE_UNKNOWN:
        return false;
      case STATUS_DISCONNECTED:
        return false;
      case STATUS_SERVER_STATUS_ERROR:
        return false;
      case STATUS_INVALID_PARAMETERS:
        return false;
      default:
        return false;
    }
  }

  get statusIconColor() {
    switch (this.statusCode) {
      case STATUS_LOADING:
        return 'blue';
      case STATUS_ICE_NEW:
        return 'blue accent-1';
      case STATUS_ICE_GATHERING:
        return 'blue accent-2';
      case STATUS_ICE_COMPLETE:
        return 'blue accent-3';
      case STATUS_SDP_EXCHANGE:
        return 'blue accent-4';
      case STATUS_ONLINE:
        if (this.paused) {
          return '';
        } else {
          return 'green';
        }
      case STATUS_NEGOTIATION_FAILED:
        return 'red';
      case STATUS_ICE_UNKNOWN:
        return 'deep-orange';
      case STATUS_DISCONNECTED:
        return '';
      case STATUS_SERVER_STATUS_ERROR:
        return '';
      case STATUS_INVALID_PARAMETERS:
        return '';
      default:
        return 'deep-orange';
    }
  }

  get statusIcon() {
    switch (this.statusCode) {
      case STATUS_LOADING:
        return 'mdi-dots-horizontal';
      case STATUS_ICE_NEW:
        return 'mdi-webrtc';
      case STATUS_ICE_GATHERING:
        return 'mdi-webrtc';
      case STATUS_ICE_COMPLETE:
        return 'mdi-webrtc';
      case STATUS_SDP_EXCHANGE:
        return 'mdi-handshake';
      case STATUS_ONLINE:
        if (this.paused) {
          return 'mdi-pause';
        } else {
          return '';
        }
      case STATUS_NEGOTIATION_FAILED:
        return 'mdi-alert';
      case STATUS_ICE_UNKNOWN:
        return 'mdi-help';
      case STATUS_DISCONNECTED:
        return 'mdi-lan-disconnect';
      case STATUS_SERVER_STATUS_ERROR:
        return 'mdi-lan-disconnect';
      case STATUS_INVALID_PARAMETERS:
        return 'mdi-cog-off';
      default:
        return 'mdi-help';
    }
  }

  get statusLabel() {
    switch (this.statusCode) {
      case STATUS_LOADING:
        return this.$t('status.loading').toString();
      case STATUS_ICE_NEW:
        return this.$t('status.ice_new').toString();
      case STATUS_ICE_GATHERING:
        return this.$t('status.ice_gathering').toString();
      case STATUS_ICE_COMPLETE:
        return this.$t('status.ice_complete').toString();
      case STATUS_SDP_EXCHANGE:
        return this.$t('status.sdp_exchange').toString();
      case STATUS_ONLINE:
        if (this.connectionState) {
          return `${this.value.name} (${this.connectionState})`;
        } else {
          return this.value.name;
        }
      case STATUS_NEGOTIATION_FAILED:
        return this.$t('status.negotiation_failed').toString();
      case STATUS_ICE_UNKNOWN:
        return this.$t('status.ice_unknown').toString();
      case STATUS_DISCONNECTED:
        return this.$t('status.disconnected').toString();
      case STATUS_SERVER_STATUS_ERROR:
        return this.$t(
            'status.server_status_error',
            [this.value.server_status]
        ).toString();
      case STATUS_INVALID_PARAMETERS:
        return this.$t('status.invalid').toString();
      default:
        return this.$t('status.unknown').toString();
    }
  }

  get signalIcon() {
    const level = this.signalLevel;
    if (level >= 3) {
      return 'signal-cellular-3';
    } else if (level == 2) {
      return 'signal-cellular-2';
    } else if (level == 1) {
      return 'signal-cellular-1';
    } else {
      return 'mdi-signal-cellular-outline';
    }
  }

  get playIcon() {
    if (this.paused) {
      return 'mdi-play';
    } else {
      return 'mdi-pause';
    }
  }

  onPause() {
    this.paused = true;
  }

  onPlay() {
    this.paused = false;
    this.videoWidth = this.rtcVideo.videoWidth;
    this.videoHeight = this.rtcVideo.videoHeight;
    console.debug(`onPlay() -> w=${this.videoWidth}, h=${this.videoHeight}`);
  }

  onResize() {
    this.videoWidth = this.rtcVideo.videoWidth;
    this.videoHeight = this.rtcVideo.videoHeight;
    console.debug(`onResize() -> w=${this.videoWidth}, h=${this.videoHeight}`);
  }

  onClickPlay() {
    if (this.paused) {
      this.rtcVideo.play();
    } else {
      this.rtcVideo.pause();
    }
  }

  onClickMore() {
    this.rtcVideo.requestFullscreen();
  }

  @Watch('value.server_running')
  onWatchServerRunning(newVal, oldVal) {
  }

  @Watch('value.server_status')
  onWatchServerStatus(newVal, oldVal) {
  }

  @Emit()
  predict(obj: Array<object>) {
    return obj;
  }

  @Emit()
  contextmenu(event) {
    return event;
  }
}
</script>

<style lang="scss" scoped>
.media-player {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;

  padding: 0;
  border: 0;

  background: gray;

  .controller {
    display: flex;
    flex-direction: row;
    align-items: center;

    position: absolute;
    width: 100%;
    bottom: 0;

    z-index: 60;
  }

  .status-bar {
    z-index: 50;
  }

  .media-content {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;

    object-fit: contain;

    padding: 0;
    border: 0;

    .canvas-user {
      position: absolute;
      width: 100%;
      height: 100%;

      z-index: 40;
    }

    .canvas-meta {
      position: absolute;
      width: 100%;
      height: 100%;

      z-index: 30;
    }

    .brand-logo {
      position: absolute;
      width: 100%;
      height: 100%;

      z-index: 20;
    }

    .rtc-player {
      position: absolute;
      width: 100%;
      height: 100%;

      z-index: 10;
    }

    .video-player {
      width: 100%;
      height: 100%;
    }
  }
}
</style>
