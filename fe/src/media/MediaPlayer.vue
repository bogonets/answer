<i18n lang="yaml">
en:
  status:
    loading: "Loading"
    ice_new: "ICE new"
    ice_gathering: "ICE gathering"
    ice_complete: "ICE complete"
    ice_unknown: "ICE unknown error"
    sdp_exchange: "Exchanging SDP ..."
    online: "Online"
    negotiation_failed: "Negotiation failed"
    disconnected: "Disconnected"
    server_error: "Server status error: {0}"
    invalid: "Settings are required"
    unknown: "Unknown status"
  labels:
    reconnect: "Reconnect"
    fullscreen: "Fullscreen"
    debugging: "Debugging"
    information: "Information"
  hints:
    logo_alt: "Answer"
  tooltips:
    debugging_mode: "Debugging mode is enabled"
    enable_event_detection: "Event detection is enabled"
    disable_event_detection: "Event detection is disabled"
    latest_event_time: "Latest event time: {0}"
  vms_channel_meta:
    opened: "A channel between server and client has been opened"
    filtered: "Completed successfully, but no event occurred"
    not_ready_roi: "Not ready ROI"
    bad_argument: "Bad arguments"
    unknown_code: "Unknown code: {0}"

ko:
  status:
    loading: "로딩 중 ..."
    ice_new: "ICE 피어 연결 생성됨"
    ice_gathering: "ICE 후보 수집 중..."
    ice_complete: "ICE 후보 수집 완료"
    ice_unknown: "알 수 없는 ICE 상태"
    sdp_exchange: "SDP 교환 중..."
    online: "온라인"
    negotiation_failed: "Negotiation failed"
    disconnected: "서버와 연결이 끊어졌습니다"
    server_error: "서버가 비정상 상태 입니다: {0}"
    invalid: "설정이 필요합니다"
    unknown: "알 수 없는 상태"
  labels:
    reconnect: "재접속"
    fullscreen: "전체 화면"
    debugging: "디버깅"
    information: "정보"
  hints:
    logo_alt: "Answer"
  tooltips:
    debugging_mode: "디버깅 모드가 활성화 되었습니다"
    enable_event_detection: "이벤트 감지 중 입니다"
    disable_event_detection: "이벤트 감지가 비활성화 되었습니다"
    latest_event_time: "마지막 이벤트 발생 시간: {0}"
  vms_channel_meta:
    opened: "서버와 클라이언트 사이의 채널이 열렸습니다"
    filtered: "성공적으로 완료되었지만 이벤트가 발생하지 않았습니다"
    not_ready_roi: "관심영역(ROI)이 준비되지 않았습니다"
    bad_argument: "잘못된 인수"
    unknown_code: "알 수 없는 에러 코드: {0}"
</i18n>

<template>
  <v-hover v-slot="{ hover }">
    <v-card
        outlined
        tile
        class="media-player"
        @contextmenu="contextmenu"
        :width="width"
        :height="height"
        :min-width="minWidth"
        :min-height="minHeight"
        :max-width="maxWidth"
        :max-height="maxHeight"
    >
      <v-system-bar
          class="status-bar"
          v-if="!hideSystemBar"
          v-show="showSystemBar(hover)"
          absolute
          lights-out
          :height="systemBarHeight"
      >
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon
                :color="statusIconColor"
                v-bind="attrs"
                v-on="on"
            >
              {{ statusIcon }}
            </v-icon>
          </template>
          <span>{{ statusTooltip }}</span>
        </v-tooltip>

        <span>{{ value.name }}</span>

        <v-spacer></v-spacer>
        <v-progress-circular
            v-if="loading || loadingByStatusCode"
            size="14"
            width="2"
            indeterminate
        ></v-progress-circular>
        <div v-if="online">
          <v-icon v-if="false">mdi-video-4k-box</v-icon>
          <v-icon v-if="false">mdi-video-off</v-icon>
          <v-icon v-if="false" color="red">mdi-record</v-icon>

          <v-tooltip v-if="value.server_debugging" bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon v-bind="attrs" v-on="on">mdi-bug</v-icon>
            </template>
            <span>{{ $t('tooltips.debugging_mode') }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-icon v-bind="attrs" v-on="on">
                {{ activeIcon }}
              </v-icon>
            </template>
            <span>{{ activeTooltip }}</span>
          </v-tooltip>

          <v-icon v-if="false">mdi-volume-off</v-icon>
          <v-icon v-if="false">{{ signalIcon }}</v-icon>
        </div>
      </v-system-bar>

      <v-sheet
          v-if="showInformationPanel && online && channelOpened"
          rounded
          class="information-panel"
          transition="slide-x-transition"
          :style="`top: ${getInfoPanelTop(hover)};`"
      >
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-icon small :color="informationIconColor">
              {{ informationIcon }}
            </v-icon>
            <div v-bind="attrs" v-on="on">
              <span class="ml-1 text--secondary text-body-2">
                {{ informationText }}
              </span>
            </div>
          </template>
          <span>
            {{ $t('tooltips.latest_event_time', [informationDate]) }}
          </span>
        </v-tooltip>
      </v-sheet>

      <div
          class="media-content"
          @mousedown="onMouseDownMediaContent"
          @mousemove="onMouseMoveMediaContent"
          @mouseup="onMouseUpMediaContent"
      >
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

        <!-- Canvas for real-time snapshots -->
        <canvas
            v-show="online"
            class="canvas-snap"
            ref="canvas-snap"
            :width="videoWidth"
            :height="videoHeight"
        ></canvas>

        <img
            v-show="!online"
            class="brand-logo"
            src="@/assets/logo/answer-logo-notext.svg"
            :alt="$t('hints.logo_alt')"
        />
      </div>

      <div
          v-if="online && !hideController"
          class="controller"
          v-show="showController(hover)"
      >
        <v-btn icon @click="onClickPlay">
          <v-icon>{{ playButtonIcon }}</v-icon>
        </v-btn>
        <v-progress-linear
            rounded
            :color="progressLineColor"
        ></v-progress-linear>

        <v-btn icon :disabled="disableActiveButton" @click="onClickActive">
          <v-icon>{{ activeButtonIcon }}</v-icon>
        </v-btn>

        <v-menu
            top
            left
            offset-y
            transition="slide-x-reverse-transition"
            :close-on-content-click="false"
            v-model="showMoreMenu"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
                icon
                @click="onClickMore"
                v-bind="attrs"
                v-on="on"
            >
              <v-icon>mdi-dots-horizontal</v-icon>
            </v-btn>
          </template>

          <v-list dense>
            <v-list-item :disabled="loadingByStatusCode" @click="onClickReconnect">
              <v-list-item-icon>
                <v-icon>mdi-reload</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ $t('labels.reconnect') }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-bug</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ $t('labels.debugging') }}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-switch
                    dense
                    :disabled="disableDebugButton"
                    :value="value.server_debugging"
                    @change="onChangeDebugging"
                ></v-switch>
              </v-list-item-action>
            </v-list-item>

            <v-list-item>
              <v-list-item-icon>
                <v-icon>mdi-information</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ $t('labels.information') }}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-switch
                    dense
                    :disabled="disableInfoButton"
                    v-model="showInformationPanel"
                ></v-switch>
              </v-list-item-action>
            </v-list-item>

            <v-list-item @click="onClickFullscreen">
              <v-list-item-icon>
                <v-icon>mdi-fullscreen</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ $t('labels.fullscreen') }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </v-card>
  </v-hover>
</template>

<script lang="ts">
import {Component, Prop, Ref, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {createMoment} from '@/chrono/date';
import colors from 'vuetify/lib/util/colors'
import type {
  VmsDeviceA,
  RtcOfferQ,
  VmsChannelMeta,
  VmsChannelMetaConsume,
  VmsUpdateDeviceQ,
} from '@/packet/vms';
import {
  TRANSCEIVER_KIND_VIDEO,
  TRANSCEIVER_KIND_AUDIO,
  DATA_CHANNEL_LABEL,
  DEFAULT_RTC_CONFIGURATION,
  DEFAULT_VIDEO_TRANSCEIVER_INIT,
  DEFAULT_AUDIO_TRANSCEIVER_INIT,
  DEFAULT_DATA_CHANNEL_INIT,
  VMS_CHANNEL_META_CODE_SUCCESS,
  VMS_CHANNEL_META_CODE_OPENED,
  VMS_CHANNEL_META_CODE_BAD_ARGUMENT,
  VMS_CHANNEL_META_CODE_NOT_READY_ROI,
  VMS_CHANNEL_META_CONSUME_CODE_SUCCESS,
  VMS_CHANNEL_META_CONSUME_CODE_UNKNOWN_ERRORS,
  VMS_CHANNEL_META_CODE_FILTERED,
} from '@/packet/vms';
import {
  IllegalStateException,
  IllegalArgumentException,
} from "@/exceptions";

enum Status {
  Loading,
  IceNew,
  IceGathering,
  IceComplete,
  SdpExchange,
  Online,
  NegotiationFailed,
  IceUnknown,
  Disconnected,
  ServerError,
  InvalidParameters,
  Closed,
}

function loadingStatus(status: Status) {
  switch (status) {
    case Status.Loading:
    case Status.IceNew:
    case Status.IceGathering:
    case Status.IceComplete:
    case Status.SdpExchange:
      return true;
    default:
      return false;
  }
}

function gatheringStatus(state: RTCIceGatheringState) {
  if (state === 'new') {
    return Status.IceNew;
  } else if (state === 'gathering') {
    return Status.IceGathering;
  } else if (state === 'complete') {
    return Status.IceComplete;
  } else {
    return Status.IceUnknown;
  }
}

@Component
export default class MediaPlayer extends VueBase {
  @Prop({type: String, default: ''})
  readonly group!: string;

  @Prop({type: String, default: ''})
  readonly project!: string;

  @Prop({type: [String, Number]})
  readonly device?: string | number;

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
  readonly useAnnotationTools!: boolean;

  @Prop({type: Boolean, default: false})
  readonly useRoiAbsolutePosition!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: [String, Number]})
  readonly width?: string | number;

  @Prop({type: [String, Number]})
  readonly height?: string | number;

  @Prop({type: [String, Number]})
  readonly minWidth?: string | number;

  @Prop({type: [String, Number]})
  readonly minHeight?: string | number;

  @Prop({type: [String, Number]})
  readonly maxWidth?: string | number;

  @Prop({type: [String, Number]})
  readonly maxHeight?: string | number;

  @Prop({type: [String, Number], default: '24px'})
  readonly systemBarHeight?: string | number;

  @Prop({type: Object, default: () => new Object()})
  readonly value!: VmsDeviceA;

  @Ref('canvas-user')
  readonly canvasUser!: HTMLCanvasElement;

  @Ref('canvas-meta')
  readonly canvasMeta!: HTMLCanvasElement;

  @Ref('canvas-snap')
  readonly canvasSnap!: HTMLCanvasElement;

  @Ref('rtc-video')
  readonly rtcVideo!: HTMLVideoElement;

  roiLeft = 0;
  roiRight = 0;
  roiTop = 0;
  roiBottom = 0;
  roiButtonPressed = false;

  paused = true;
  videoWidth = 0;
  videoHeight = 0;

  statusCode = Status.Closed;
  channelOpened = false;
  signalLevel = 0;
  connectionState = '';
  channelState = '';

  rtcConfig = DEFAULT_RTC_CONFIGURATION;
  videoTransceiverInit = DEFAULT_VIDEO_TRANSCEIVER_INIT;
  audioTransceiverInit = DEFAULT_AUDIO_TRANSCEIVER_INIT;
  dataChannelInit = DEFAULT_DATA_CHANNEL_INIT;

  peer_id?: number = undefined;
  channel?: RTCDataChannel = undefined;
  pc?: RTCPeerConnection = undefined;

  channel_message_working = false;

  showInformationPanel = true;
  informationCode = VMS_CHANNEL_META_CODE_SUCCESS;
  informationText = '';
  informationDate = '';

  showMoreMenu = false;
  disableActiveButton = false;
  disableDebugButton = false;
  disableInfoButton = false;

  mounted() {
    this.paused = this.rtcVideo.paused;
    try {
      this.open();
    } catch (error) {
      if (error instanceof IllegalArgumentException) {
        // Nothing to do.
      } else {
        throw error;
      }
    }
  }

  beforeDestroy() {
    this.close();
  }

  get deviceNumber() {
    if (typeof this.device === 'undefined') {
      return 0;
    } else if (typeof this.device === 'string') {
      return Number.parseInt(this.device);
    } else {
      return this.device;
    }
  }

  get deviceText() {
    if (typeof this.device === 'undefined') {
      return '';
    } else if (typeof this.device === 'string') {
      return this.device;
    } else {
      return this.device.toString();
    }
  }

  open() {
    if (loadingStatus(this.statusCode)) {
      throw new IllegalStateException('Now loading ...');
    }

    if (!(this.group && this.project && this.device)) {
      this.statusCode = Status.InvalidParameters;
      throw new IllegalArgumentException();
    }

    this.statusCode = Status.Loading;
    this.channelOpened = false;
    (async () => {
      await this.doNegotiate();
    })();
  }

  close() {
    if (typeof this.peer_id !== 'undefined') {
      const group = this.group;
      const project = this.project;
      const device = this.deviceText;
      const peer = this.peer_id.toString();
      this.$api2.deleteVmsDeviceRtcJsep(group, project, device, peer)
          .then(() => {
            // EMPTY.
          })
          .catch(error => {
            this.toastRequestFailure(error);
          });
      this.peer_id = undefined;
    }

    if (this.channel) {
      this.channel.close();
      this.channel = undefined;
    }
    if (this.pc) {
      this.pc.close();
      this.pc = undefined;
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
      this.statusCode = Status.Online;
    } catch (error) {
      this.pc = undefined;
      this.channel = undefined;
      this.statusCode = Status.NegotiationFailed;
      this.toastError(error);
    }
  }

  async createPeerAndMetaChannel() {
    const group = this.group;
    const project = this.project;
    const device = this.deviceText;
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

    this.statusCode = Status.SdpExchange;

    const body = {
      type: this.pc.localDescription?.type || '',
      sdp: this.pc.localDescription?.sdp || '',
    } as RtcOfferQ;
    const answer = await this.$api2.postVmsDeviceRtcJsep(group, project, device, body);
    this.peer_id = answer.peer_id;
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
    gatheringStatus(peer.iceGatheringState);
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

  sendChannelResponse(body: VmsChannelMetaConsume) {
    if (this.channel) {
      this.channel.send(JSON.stringify(body))
    }
  }

  sendChannelResponseSuccessful() {
    const body = {
      code: VMS_CHANNEL_META_CONSUME_CODE_SUCCESS,
    } as VmsChannelMetaConsume;
    this.sendChannelResponse(body);
  }

  sendChannelResponseError() {
    const body = {
      code: VMS_CHANNEL_META_CONSUME_CODE_UNKNOWN_ERRORS,
    } as VmsChannelMetaConsume;
    this.sendChannelResponse(body);
  }

  onChannelMessage(event: MessageEvent) {
    if (this.channel_message_working) {
      this.sendChannelResponseSuccessful();
      return;  // Now working ...
    }

    const canvasWidth = this.canvasMeta.width;
    const canvasHeight = this.canvasMeta.height;
    const context = this.canvasMeta.getContext('2d');
    if (!context) {
      this.sendChannelResponseSuccessful();
      return;
    }

    this.channel_message_working = true;
    (async () => {
      try {
        const content = JSON.parse(event.data) as VmsChannelMeta;
        context.clearRect(0, 0, canvasWidth, canvasHeight);
        await this.onRenderMetaData(context, canvasWidth, canvasHeight, content);
        this.sendChannelResponseSuccessful();
      } catch (error) {
        context.clearRect(0, 0, canvasWidth, canvasHeight);
        this.predict([]);
        this.sendChannelResponseError();
      } finally {
        this.channel_message_working = false;
      }
    })();
  }

  async onRenderMetaData(
      context: CanvasRenderingContext2D,
      canvasWidth: number,
      canvasHeight: number,
      content: VmsChannelMeta,
  ) {
    this.informationCode = content.code;
    this.informationDate = createMoment().format('LL, LTS');
    // console.debug(`content.code: ${content.code}`);

    switch (content.code) {
      // Successful cases
      case VMS_CHANNEL_META_CODE_SUCCESS:
        this.informationText = content.message.trim();
        break;
      case VMS_CHANNEL_META_CODE_OPENED:
        this.informationText = this.$t('vms_channel_meta.opened').toString();
        this.channelOpened = true;
        break;
      case VMS_CHANNEL_META_CODE_FILTERED:
        this.informationText = content.message.trim();
        break;

      // Failed cases
      case VMS_CHANNEL_META_CODE_NOT_READY_ROI:
        this.informationText = this.$t('vms_channel_meta.not_ready_roi').toString();
        break;
      case VMS_CHANNEL_META_CODE_BAD_ARGUMENT:
        this.informationText = this.$t('vms_channel_meta.bad_argument').toString();
        break;
      default:
        this.informationText = this.$t(
            'vms_channel_meta.unknown_code',
            [content.code]
        ).toString();
        break;
    }

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
      this.statusCode = gatheringStatus(pc.iceGatheringState);
      if (pc.iceGatheringState === 'complete') {
        return resolve();  // DONE !!
      }

      const stateChangeCallback = () => {
        this.statusCode = gatheringStatus(pc.iceGatheringState);
        if (pc.iceGatheringState === 'complete') {
          pc.removeEventListener('icegatheringstatechange', stateChangeCallback);
          this.statusCode = Status.IceComplete;
          return resolve();  // DONE !!
        }
      };

      pc.addEventListener('icegatheringstatechange', stateChangeCallback);
    });
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
    return this.statusCode === Status.Online;
  }

  get loadingByStatusCode() {
    return loadingStatus(this.statusCode);
  }

  get statusIconColor() {
    switch (this.statusCode) {
      case Status.Loading:
        return colors.blue.base;
      case Status.IceNew:
        return colors.blue.accent1;
      case Status.IceGathering:
        return colors.blue.accent2;
      case Status.IceComplete:
        return colors.blue.accent3;
      case Status.SdpExchange:
        return colors.blue.accent4;
      case Status.Online:
        if (this.paused) {
          return '';
        } else {
          return colors.green.base;
        }
      case Status.NegotiationFailed:
        return colors.red.base;
      case Status.IceUnknown:
        return colors.deepOrange.base;
      case Status.Disconnected:
        return '';
      case Status.ServerError:
        return '';
      case Status.InvalidParameters:
        return '';
      default:
        return colors.deepOrange.base;
    }
  }

  get statusIcon() {
    switch (this.statusCode) {
      case Status.Loading:
        return 'mdi-dots-horizontal';
      case Status.IceNew:
        return 'mdi-webrtc';
      case Status.IceGathering:
        return 'mdi-webrtc';
      case Status.IceComplete:
        return 'mdi-webrtc';
      case Status.SdpExchange:
        return 'mdi-handshake';
      case Status.Online:
        if (this.paused) {
          return 'mdi-pause';
        } else {
          return 'mdi-play';
        }
      case Status.NegotiationFailed:
        return 'mdi-alert';
      case Status.IceUnknown:
        return 'mdi-help';
      case Status.Disconnected:
        return 'mdi-lan-disconnect';
      case Status.ServerError:
        return 'mdi-lan-disconnect';
      case Status.InvalidParameters:
        return 'mdi-cog-off';
      default:
        return 'mdi-help';
    }
  }

  get statusTooltip() {
    switch (this.statusCode) {
      case Status.Loading:
        return this.$t('status.loading');
      case Status.IceNew:
        return this.$t('status.ice_new');
      case Status.IceGathering:
        return this.$t('status.ice_gathering');
      case Status.IceComplete:
        return this.$t('status.ice_complete');
      case Status.SdpExchange:
        return this.$t('status.sdp_exchange');
      case Status.Online:
        return this.$t('status.online');
      case Status.NegotiationFailed:
        return this.$t('status.negotiation_failed');
      case Status.IceUnknown:
        return this.$t('status.ice_unknown');
      case Status.Disconnected:
        return this.$t('status.disconnected');
      case Status.ServerError:
        return this.$t('status.server_error', [this.value.server_status]);
      case Status.InvalidParameters:
        return this.$t('status.invalid');
      default:
        return this.$t('status.unknown');
    }
  }

  get activeIcon() {
    if (this.value.active) {
      return 'mdi-eye';
    } else {
      return 'mdi-eye-off';
    }
  }

  get activeTooltip() {
    if (this.value.active) {
      return this.$t('tooltips.enable_event_detection');
    } else {
      return this.$t('tooltips.disable_event_detection');
    }
  }

  get signalIcon() {
    const level = this.signalLevel;
    if (level >= 3) {
      return 'mdi-signal-cellular-3';
    } else if (level == 2) {
      return 'mdi-signal-cellular-2';
    } else if (level == 1) {
      return 'mdi-signal-cellular-1';
    } else {
      return 'mdi-signal-cellular-outline';
    }
  }

  getInfoPanelTop(hover: boolean) {
    if (this.hideSystemBar) {
      return 0;
    }
    if (this.hoverSystemBar && !hover) {
      return 0;
    }
    return this.systemBarHeight;
  }

  get informationIconColor() {
    switch (this.informationCode) {
      case VMS_CHANNEL_META_CODE_SUCCESS:
        return this.$vuetify.theme.currentTheme.secondary;
      case VMS_CHANNEL_META_CODE_OPENED:
        return this.$vuetify.theme.currentTheme.secondary;
      case VMS_CHANNEL_META_CODE_FILTERED:
        return this.$vuetify.theme.currentTheme.secondary;
      case VMS_CHANNEL_META_CODE_NOT_READY_ROI:
        return colors.deepOrange.base;
      case VMS_CHANNEL_META_CODE_BAD_ARGUMENT:
        return colors.deepOrange.base;
      default:
        return colors.red.base;
    }
  }

  get informationIcon() {
    switch (this.informationCode) {
      case VMS_CHANNEL_META_CODE_SUCCESS:
        return 'mdi-chat-processing-outline';
      case VMS_CHANNEL_META_CODE_OPENED:
        return 'mdi-chat-outline';
      case VMS_CHANNEL_META_CODE_FILTERED:
        return 'mdi-chat-outline';
      case VMS_CHANNEL_META_CODE_NOT_READY_ROI:
        return 'mdi-alert-octagram-outline';
      case VMS_CHANNEL_META_CODE_BAD_ARGUMENT:
        return 'mdi-alert-octagram-outline';
      default:
        return 'mdi-help-circle-outline';
    }
  }

  get playButtonIcon() {
    if (this.paused) {
      return 'mdi-play';
    } else {
      return 'mdi-pause';
    }
  }

  get progressLineColor() {
    return colors.grey.base;
  }

  get activeButtonIcon() {
    if (this.value.active) {
      return 'mdi-eye-off';
    } else {
      return 'mdi-eye';
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

  @Watch('videoWidth')
  onWatchVideoWidth() {
    this.resizeVideo();
  }

  @Watch('videoHeight')
  onWatchVideoHeight() {
    this.resizeVideo();
  }

  @Emit('video:resize')
  resizeVideo() {
    return {width: this.videoWidth, height: this.videoHeight};
  }

  onClickPlay() {
    if (this.paused) {
      this.rtcVideo.play();
    } else {
      this.rtcVideo.pause();
    }
  }

  onClickActive() {
    const updateActiveFlag = !this.value.active;
    const body = {
      active: updateActiveFlag,
    } as VmsUpdateDeviceQ;

    const group = this.group;
    const project = this.project;
    const device = this.deviceText;
    this.disableActiveButton = true;
    this.$api2.patchVmsDevice(group, project, device, body)
        .then(() => {
          this.value.active = updateActiveFlag;
          this.disableActiveButton = false;
        })
        .catch(error => {
          this.disableActiveButton = false;
          console.error(error);
        });
  }

  onClickMore() {
    this.showMoreMenu = true;
  }

  onClickReconnect() {
    this.showMoreMenu = false;
    this.close();
    this.open();
  }

  onChangeDebugging() {
    const group = this.group;
    const project = this.project;
    const device = this.deviceText;
    this.disableDebugButton = true;

    const updateDebugFlag = !this.value.server_debugging;
    const thenCallback = () => {
      this.value.server_debugging = updateDebugFlag;
      this.disableDebugButton = false;
    };
    const catchCallback = error => {
      this.disableDebugButton = false;
      console.error(error);
    };

    if (updateDebugFlag) {
      this.$api2.postVmsDeviceProcessDebugStart(group, project, device)
          .then(thenCallback).catch(catchCallback);
    } else {
      this.$api2.postVmsDeviceProcessDebugStop(group, project, device)
          .then(thenCallback).catch(catchCallback);
    }
  }

  onClickFullscreen() {
    this.showMoreMenu = false;
    this.rtcVideo.requestFullscreen();
  }

  @Watch('value.server_running')
  onWatchServerRunning() {
  }

  @Watch('value.server_status')
  onWatchServerStatus() {
  }

  @Watch('useColorPicker')
  onWatchUseColorPicker() {
  }

  @Watch('useAnnotationTools')
  onWatchUseAnnotationTools() {
  }

  onMouseDownMediaContent(event: MouseEvent) {
    if (this.useColorPicker) {
      const clientRect = this.canvasSnap.getBoundingClientRect();
      const x = Math.round(event.clientX - clientRect.left);
      const y = Math.round(event.clientY - clientRect.top);
      const ratioX = x / clientRect.width;
      const ratioY = y / clientRect.height;
      const imageX = Math.round(ratioX * this.canvasSnap.width);
      const imageY = Math.round(ratioY * this.canvasSnap.height);
      this.pipette(this.getVideoPixelRgb(imageX, imageY));
    }

    if (this.useAnnotationTools) {
      const clientRect = this.canvasUser.getBoundingClientRect();
      const x = Math.round(event.clientX - clientRect.left);
      const y = Math.round(event.clientY - clientRect.top);
      const ratioX = x / clientRect.width;
      const ratioY = y / clientRect.height;
      const imageX = Math.round(ratioX * this.canvasUser.width);
      const imageY = Math.round(ratioY * this.canvasUser.height);
      this.roiLeft = imageX;
      this.roiTop = imageY;
      this.roiButtonPressed = true;
    }
  }

  onMouseMoveMediaContent(event) {
    if (this.useAnnotationTools && this.roiButtonPressed) {
      const clientRect = this.canvasUser.getBoundingClientRect();
      const x = Math.round(event.clientX - clientRect.left);
      const y = Math.round(event.clientY - clientRect.top);
      const ratioX = x / clientRect.width;
      const ratioY = y / clientRect.height;
      const imageX = Math.round(ratioX * this.canvasUser.width);
      const imageY = Math.round(ratioY * this.canvasUser.height);

      const context = this.canvasUser.getContext('2d');
      const width = this.canvasUser.width;
      const height = this.canvasUser.height;
      if (!context) {
        throw new Error('Not exists 2d context from user-canvas.');
      }
      const roiWidth = imageX - this.roiLeft;
      const roiHeight = imageY - this.roiTop;
      context.lineWidth = 5;
      context.strokeStyle = 'red';
      context.clearRect(0, 0, width, height);
      context.strokeRect(this.roiLeft, this.roiTop, roiWidth, roiHeight);
    }
  }

  onMouseUpMediaContent(event) {
    if (this.useAnnotationTools && this.roiButtonPressed) {
      const clientRect = this.canvasUser.getBoundingClientRect();
      const x = Math.round(event.clientX - clientRect.left);
      const y = Math.round(event.clientY - clientRect.top);
      const ratioX = x / clientRect.width;
      const ratioY = y / clientRect.height;
      const imageX = Math.round(ratioX * this.canvasUser.width);
      const imageY = Math.round(ratioY * this.canvasUser.height);

      const context = this.canvasUser.getContext('2d');
      const width = this.canvasUser.width;
      const height = this.canvasUser.height;
      if (!context) {
        throw new Error('Not exists 2d context from user-canvas.');
      }
      const roiWidth = imageX - this.roiLeft;
      const roiHeight = imageY - this.roiTop;
      context.lineWidth = 5;
      context.clearRect(0, 0, width, height);
      context.strokeRect(this.roiLeft, this.roiTop, roiWidth, roiHeight);
      this.roiRight = imageX;
      this.roiBottom = imageY;
      this.roiButtonPressed = false;
      if (this.useRoiAbsolutePosition) {
        this.roi(this.roiLeft, this.roiRight, this.roiTop, this.roiBottom);
      } else {
        this.roi(
            this.roiLeft / width,
            this.roiRight / width,
            this.roiTop / height,
            this.roiBottom / height,
        );
      }
    }
  }

  @Emit()
  predict(obj: Array<object>) {
    return obj;
  }

  @Emit()
  contextmenu(event) {
    return event;
  }

  @Emit('pipette')
  pipette(color) {
    return color;
  }

  snapshotVideoAsImageData(clear = true) {
    const context = this.canvasSnap.getContext('2d');
    const width = this.canvasSnap.width;
    const height = this.canvasSnap.height;
    if (!context) {
      throw new Error('Not exists 2d context from snap-canvas');
    }
    context.drawImage(this.rtcVideo, 0, 0, width, height);
    const image = context.getImageData(0, 0, width, height);
    if (clear) {
      context.clearRect(0, 0, width, height);
    }
    return image;
  }

  snapshotVideoAsDataUrl(contentType = 'image/png', clear = true) {
    const context = this.canvasSnap.getContext('2d');
    const width = this.canvasSnap.width;
    const height = this.canvasSnap.height;
    if (!context) {
      throw new Error('Not exists 2d context from snap-canvas');
    }
    context.drawImage(this.rtcVideo, 0, 0, width, height);
    const result = this.canvasSnap.toDataURL(contentType);
    if (clear) {
      context.clearRect(0, 0, width, height);
    }
    return result;
  }

  getVideoPixelRgb(x: number, y: number) {
    const context = this.canvasSnap.getContext('2d');
    const width = this.canvasSnap.width;
    if (!context) {
      throw new Error('Not exists 2d context from user\'s canvas.');
    }

    const image = this.snapshotVideoAsImageData(true);
    const pixels = image.data;

    const i = (x + (y * width)) * 4;
    const r = pixels[i];
    const g = pixels[i + 1];
    const b = pixels[i + 2];
    return {r, g, b};
  }

  @Emit('roi')
  roi(left, right, top, bottom) {
    return {
      x1: left,
      y1: top,
      x2: right,
      y2: bottom,
    };
  }

  clearAnnotations() {
    this.roiLeft = 0;
    this.roiRight = 0;
    this.roiTop = 0;
    this.roiBottom = 0;
    this.roiButtonPressed = false;

    const context = this.canvasUser.getContext('2d');
    const width = this.canvasUser.width;
    const height = this.canvasUser.height;
    if (!context) {
      throw new Error('Not exists 2d context from user-canvas.');
    }
    context.clearRect(0, 0, width, height);
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

$color-grey: map-get($colors, 'grey');
$color-grey-base: map-get($color-grey, 'base');
$color-grey-lighten-5: map-get($color-grey, 'lighten-5');
$color-grey-lighten-4: map-get($color-grey, 'lighten-4');
$color-grey-lighten-3: map-get($color-grey, 'lighten-3');
$color-grey-lighten-2: map-get($color-grey, 'lighten-2');
$color-grey-lighten-1: map-get($color-grey, 'lighten-1');
$color-grey-darken-1: map-get($color-grey, 'darken-1');
$color-grey-darken-2: map-get($color-grey, 'darken-2');
$color-grey-darken-3: map-get($color-grey, 'darken-3');
$color-grey-darken-4: map-get($color-grey, 'darken-4');

$ghost-transparent: 0.4;

@mixin common-media {
  position: absolute;

  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);

  object-fit: contain;
  object-position: center;

  max-width: 100%;
  max-height: 100%;

  padding: 0;
  margin: 0;
}

.theme--light.v-application {
  .media-player {
    background-color: $color-grey-lighten-1;

    .information-panel {
      background-color: rgba(map-get($shades, 'white'), $ghost-transparent);
    }
  }
}

.theme--dark.v-application {
  .media-player {
    background-color: $color-grey-darken-3;

    .information-panel {
      background-color: rgba(map-get($shades, 'black'), $ghost-transparent);
    }
  }
}

.media-player {
  display: flex;

  padding: 0;
  margin: 0;

  min-width: 100px;
  min-height: 100px;

  .status-bar {
    z-index: 60;
  }

  .information-panel {
    display: flex;
    flex-direction: row;
    align-items: center;

    padding: 0 4px 0 4px;
    margin: 4px 4px 0 4px;

    position: absolute;

    z-index: 50;
  }

  .media-content {
    flex: 1;

    padding: 0;
    margin: 0;

    .canvas-user {
      @include common-media;
      z-index: 40;
    }

    .canvas-meta {
      @include common-media;
      z-index: 30;
    }

    .brand-logo {
      @include common-media;

      min-width: 16px;
      min-height: 16px;

      max-width: 256px;
      max-height: 256px;
    }

    .canvas-snap {
      @include common-media;
      z-index: 10;
    }

    .video-player {
      @include common-media;
    }
  }

  .controller {
    display: flex;
    flex-direction: row;
    align-items: center;

    padding: 0;
    margin: 0;

    position: absolute;
    width: 100%;
    bottom: 0;

    z-index: 70;
  }
}
</style>
