<i18n lang="yaml">
en:
  status:
    loading: 'Loading'
    ice_new: 'ICE new'
    ice_gathering: 'ICE gathering'
    ice_complete: 'ICE complete'
    ice_unknown: 'ICE unknown error'
    sdp_exchange: 'Exchanging SDP ...'
    online: 'Online'
    negotiation_failed: 'Negotiation failed'
    disconnected: 'Disconnected'
    server_error: 'Server status error: {0}'
    invalid: 'Settings are required'
    unknown: 'Unknown status'
  labels:
    reconnect: 'Reconnect'
    active: 'Active'
    fullscreen: 'Fullscreen'
    debugging: 'Debugging'
    information: 'Information'
  hints:
    logo_alt: 'Answer'
  tooltips:
    channel_opened: 'A channel between server and client has been opened'
    debugging_mode: 'Debugging mode is enabled'
    enable_event_detection: 'Event detection is enabled'
    disable_event_detection: 'Event detection is disabled'
    latest_event_time: 'Latest event time: {0}'
  vms_channel_meta:
    filtered: 'Completed successfully, but no event occurred'
    disabled: 'Disabled'
    not_ready_roi: 'Not ready ROI'
    not_ready_filters: 'Not ready filters'
    raise_exception: 'Raise exception'
    unknown_code: 'Unknown code: {0}'
    empty_events: 'Empty events'

ko:
  status:
    loading: '로딩 중 ...'
    ice_new: 'ICE 피어 연결 생성됨'
    ice_gathering: 'ICE 후보 수집 중...'
    ice_complete: 'ICE 후보 수집 완료'
    ice_unknown: '알 수 없는 ICE 상태'
    sdp_exchange: 'SDP 교환 중...'
    online: '온라인'
    negotiation_failed: 'Negotiation failed'
    disconnected: '서버와 연결이 끊어졌습니다'
    server_error: '서버가 비정상 상태 입니다: {0}'
    invalid: '설정이 필요합니다'
    unknown: '알 수 없는 상태'
  labels:
    reconnect: '재접속'
    active: '이벤트 감지'
    fullscreen: '전체 화면'
    debugging: '디버깅'
    information: '정보'
  hints:
    logo_alt: 'Answer'
  tooltips:
    channel_opened: '서버와 클라이언트 사이의 채널이 열렸습니다'
    debugging_mode: '디버깅 모드가 활성화 되었습니다'
    enable_event_detection: '이벤트 감지 중 입니다'
    disable_event_detection: '이벤트 감지가 비활성화 되었습니다'
    latest_event_time: '마지막 이벤트 발생 시간: {0}'
  vms_channel_meta:
    filtered: '성공적으로 완료되었지만 이벤트가 발생하지 않았습니다'
    disabled: '비활성화 되었습니다'
    not_ready_roi: '관심영역(ROI)이 준비되지 않았습니다'
    not_ready_filters: '필터가 준비되지 않았습니다'
    raise_exception: '예외가 발생되었습니다'
    unknown_code: '알 수 없는 에러 코드: {0}'
    empty_events: '감지된 이벤트가 없습니다'
</i18n>

<template>
  <v-hover v-slot="{hover}">
    <div
      class="media-player"
      ref="media-player"
      @contextmenu="contextmenu"
      :style="mediaPlayerStyle"
    >
      <div
        class="status-bar"
        v-if="!hideStatusBar"
        v-show="showStatusBar(hover)"
        :style="statusBarStyle"
      >
        <v-tooltip bottom>
          <template v-slot:activator="{on, attrs}">
            <v-icon
              class="mr-1"
              small
              :color="statusIconColor"
              v-bind="attrs"
              v-on="on"
            >
              {{ statusIcon }}
            </v-icon>
          </template>
          <span>{{ statusTooltip }}</span>
        </v-tooltip>

        <span class="mr-1 text-caption text--secondary">{{ value.name }}</span>

        <v-spacer></v-spacer>
        <v-progress-circular
          v-if="loading || loadingByStatusCode"
          size="14"
          width="2"
          indeterminate
        ></v-progress-circular>

        <div v-if="online">
          <v-icon v-if="false" class="ml-1" small>mdi-video-4k-box</v-icon>
          <v-icon v-if="false" class="ml-1" small>mdi-video-off</v-icon>
          <v-icon v-if="false" class="ml-1" small color="red">mdi-record</v-icon>

          <v-tooltip v-if="lastEventDate" bottom>
            <template v-slot:activator="{on, attrs}">
              <v-icon class="ml-1" small v-bind="attrs" v-on="on">mdi-update</v-icon>
            </template>
            <span>{{ $t('tooltips.latest_event_time', [lastEventDate]) }}</span>
          </v-tooltip>

          <v-tooltip v-if="channelOpened" bottom>
            <template v-slot:activator="{on, attrs}">
              <v-icon class="ml-1" small v-bind="attrs" v-on="on">mdi-broadcast</v-icon>
            </template>
            <span>{{ $t('tooltips.channel_opened') }}</span>
          </v-tooltip>

          <v-tooltip v-if="value.server_debugging" bottom>
            <template v-slot:activator="{on, attrs}">
              <v-icon class="ml-1" color="warning" small v-bind="attrs" v-on="on">
                mdi-bug
              </v-icon>
            </template>
            <span>{{ $t('tooltips.debugging_mode') }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{on, attrs}">
              <v-icon
                class="ml-1"
                small
                :color="activeIconColor"
                v-bind="attrs"
                v-on="on"
              >
                {{ activeIcon }}
              </v-icon>
            </template>
            <span>{{ activeTooltip }}</span>
          </v-tooltip>

          <v-icon v-if="false" class="ml-1" small>mdi-volume-off</v-icon>
          <v-icon v-if="false" class="ml-1" small>{{ signalIcon }}</v-icon>
        </div>
      </div>

      <v-sheet
        v-if="enableInfoPanel"
        rounded
        class="information-panel"
        transition="slide-x-transition"
        :style="`top: ${getInfoPanelTop(hover)};`"
      >
        <div v-for="(event, index) in events" :key="`event-${index}`">
          <v-tooltip bottom>
            <template v-slot:activator="{on, attrs}">
              <div v-bind="attrs" v-on="on">
                <v-icon small :color="eventColor(event)">
                  {{ eventIcon(event) }}
                </v-icon>
                <span class="ml-1 text--secondary text-body-2">
                  {{ eventLabel(event) }}
                </span>
              </div>
            </template>
            <span>{{ eventTooltip(event) }}</span>
          </v-tooltip>
        </div>
      </v-sheet>

      <div
        class="media-placeholder"
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
      </div>

      <div v-show="!online" class="brand-logo-container">
        <img
          class="brand-logo"
          src="@/assets/logos/answer-logo-notext.svg"
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
        <v-progress-linear rounded :color="progressLineColor"></v-progress-linear>

        <v-menu
          top
          left
          offset-y
          transition="slide-x-reverse-transition"
          :close-on-content-click="false"
          v-model="showMoreMenu"
        >
          <template v-slot:activator="{on, attrs}">
            <v-btn icon @click="onClickMore" v-bind="attrs" v-on="on">
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
                <v-icon>mdi-eye</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ $t('labels.active') }}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-switch
                  dense
                  :disabled="disableActiveButton"
                  v-model="activeSwitch"
                  @change="onChangeActive"
                ></v-switch>
              </v-list-item-action>
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
                  v-model="debugSwitch"
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
    </div>
  </v-hover>
</template>

<script lang="ts">
import {Component, Prop, Ref, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import colors from 'vuetify/lib/util/colors';
import {
  TRANSCEIVER_KIND_VIDEO,
  TRANSCEIVER_KIND_AUDIO,
  DATA_CHANNEL_LABEL,
  DEFAULT_RTC_CONFIGURATION,
  DEFAULT_VIDEO_TRANSCEIVER_INIT,
  DEFAULT_AUDIO_TRANSCEIVER_INIT,
  DEFAULT_DATA_CHANNEL_INIT,
  VMS_CHANNEL_META_CONSUME_CODE_SUCCESS,
  VMS_CHANNEL_META_CONSUME_CODE_SKIP,
  VMS_CHANNEL_META_CONSUME_CODE_UNKNOWN,
  EVENT_CATEGORY_TO_ICON,
  VmsChannelMetaCode,
  VmsChannelEventCode,
} from '@/packet/vms';
import type {VmsChannelEvent, VmsEventConfigExtra} from '@/packet/vms';
import type {
  VmsDeviceA,
  RtcOfferQ,
  VmsChannelMeta,
  VmsChannelMetaConsume,
  VmsUpdateDeviceQ,
} from '@/packet/vms';
import {
  ContextException,
  UndefinedException,
  IllegalStateException,
  IllegalArgumentException,
  InaccessibleAreaException,
} from '@/exceptions';
import {createMoment} from '@/chrono/date';

export enum Status {
  // --[[ Loading
  Loading,
  IceNew,
  IceGathering,
  IceComplete,
  SdpExchange,
  // ]]--

  Online,

  // --[[ Errors
  NegotiationFailed,
  IceUnknown,
  Disconnected,
  ServerError,
  InvalidParameters,
  Closed,
  // ]]--
}

export interface PixelRgb {
  r: number;
  g: number;
  b: number;
}

export interface Roi {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
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
  readonly hideStatusBar!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideCanvasUser!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideCanvasMeta!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideController!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hoverStatusBar!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hoverController!: boolean;

  @Prop({type: Boolean, default: false})
  readonly useColorPicker!: boolean;

  @Prop({type: Boolean, default: false})
  readonly useAnnotationTools!: boolean;

  @Prop({type: Boolean, default: false})
  readonly useRoiAbsolutePosition!: boolean;

  @Prop({type: Number, default: 5})
  readonly lineWidth!: number;

  @Prop({type: String, default: 'red'})
  readonly strokeStyle!: string;

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
  readonly statusBarHeight!: string | number;

  @Prop({type: Boolean, default: false})
  readonly disableAspectRatio!: boolean;

  @Prop({type: Object, default: () => new Object()})
  readonly value!: VmsDeviceA;

  @Prop({type: Object})
  readonly eventConfig?: VmsEventConfigExtra;

  @Ref('media-player')
  readonly mediaPlayer!: HTMLDivElement;

  @Ref('canvas-user')
  readonly canvasUser!: HTMLCanvasElement;

  @Ref('canvas-meta')
  readonly canvasMeta!: HTMLCanvasElement;

  @Ref('canvas-snap')
  readonly canvasSnap!: HTMLCanvasElement;

  @Ref('rtc-video')
  readonly rtcVideo!: HTMLVideoElement;

  editRoi = false;
  roiLeft = 0;
  roiRight = 0;
  roiTop = 0;
  roiBottom = 0;

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

  workingChannelProcessing = false;

  showInformationPanel = true;
  events = [] as Array<VmsChannelEvent>;
  lastEventCode = VmsChannelMetaCode.Unknown;
  lastEventDate = '';
  informationText = '';

  showMoreMenu = false;
  disableActiveButton = false;
  disableDebugButton = false;
  disableInfoButton = false;

  activeSwitch = false;
  debugSwitch = false;

  mounted() {
    this.activeSwitch = this.value.active ?? false;
    this.debugSwitch = this.value.server_debugging ?? false;
    this.updateEventConfig(this.eventConfig);

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

  get mediaPlayerStyle() {
    let style = '';
    if (typeof this.width !== 'undefined') {
      style += `width: ${this.width};`;
    }
    if (typeof this.height !== 'undefined') {
      style += `height: ${this.height};`;
    }
    if (typeof this.minWidth !== 'undefined') {
      style += `min-width: ${this.minWidth};`;
    }
    if (typeof this.minHeight !== 'undefined') {
      style += `min-height: ${this.minHeight};`;
    }
    if (typeof this.maxWidth !== 'undefined') {
      style += `max-width: ${this.maxWidth};`;
    }
    if (typeof this.maxHeight !== 'undefined') {
      style += `max-height: ${this.maxHeight};`;
    }
    if (!this.disableAspectRatio && this.videoWidth && this.videoHeight) {
      style += `aspect-ratio: ${this.videoWidth}/${this.videoHeight};`;
    }
    return style;
  }

  get statusBarStyle() {
    return `height: ${this.statusBarHeight};`;
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
      this.$api2
        .deleteVmsDeviceRtcJsep(group, project, device, peer)
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
      let credentialType: undefined | 'password' = undefined;
      if (typeof ice.credential_type !== 'undefined') {
        if (ice.credential_type === 'password') {
          credentialType = 'password';
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
    this.channel.onerror = event => {
      console.error(`Data channel error: ${event}`);
    };

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
    // console.debug(`Channel opened.`);
    if (typeof this.channel === 'undefined') {
      return;
    }
  }

  onChannelClose() {
    // console.debug(`Channel closed.`);
  }

  sendChannelResponse(code: number) {
    if (!this.channel) {
      throw new UndefinedException('Channel is not opened');
    }

    const body = {
      code: code,
    } as VmsChannelMetaConsume;

    this.channel.send(JSON.stringify(body));
  }

  sendChannelResponseSuccessful() {
    this.sendChannelResponse(VMS_CHANNEL_META_CONSUME_CODE_SUCCESS);
  }

  sendChannelResponseSkip() {
    this.sendChannelResponse(VMS_CHANNEL_META_CONSUME_CODE_SKIP);
  }

  sendChannelResponseError() {
    this.sendChannelResponse(VMS_CHANNEL_META_CONSUME_CODE_UNKNOWN);
  }

  onChannelMessage(event: MessageEvent) {
    const canvasWidth = this.canvasMeta.width;
    const canvasHeight = this.canvasMeta.height;
    const context = this.canvasMeta.getContext('2d');
    if (!context) {
      throw new ContextException('Unable to get context for 2D canvas');
    }

    if (this.workingChannelProcessing) {
      return;
    } else {
      this.workingChannelProcessing = true;
    }

    (async () => {
      context.clearRect(0, 0, canvasWidth, canvasHeight);

      try {
        const meta = JSON.parse(event.data) as VmsChannelMeta;
        // console.debug("onChannelMessage", meta);
        this.renderMetaData(context, canvasWidth, canvasHeight, meta);

        this.lastEventCode = meta.code;
        this.lastEventDate = createMoment().format('LL, LTS');

        switch (meta.code) {
          case VmsChannelMetaCode.Success:
            this.events = meta.events;
            break;
          case VmsChannelMetaCode.ChannelOpened:
            this.channelOpened = true;
            this.events = [];
            return;
          case VmsChannelMetaCode.Unknown:
            this.events = [];
            throw new IllegalStateException(
              'An unknown error occurred in the `VmsChannelMeta` packet',
            );
          default:
            throw new InaccessibleAreaException();
        }

        this.sendChannelResponseSuccessful();
      } catch (error) {
        console.error(error);
        this.events = [];
        this.sendChannelResponseError();
      } finally {
        this.workingChannelProcessing = false;
      }
    })();
  }

  renderMetaData(
    context: CanvasRenderingContext2D,
    canvasWidth: number,
    canvasHeight: number,
    content: VmsChannelMeta,
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
  }

  // onChannelError(channel: RTCDataChannel, event: Event): any {
  //   console.error(`Data channel error: ${event}`);
  // }

  waitToCompleteIceGathering(pc: RTCPeerConnection) {
    return new Promise(resolve => {
      this.statusCode = gatheringStatus(pc.iceGatheringState);
      if (pc.iceGatheringState === 'complete') {
        return resolve('complete'); // DONE !!
      }

      const stateChangeCallback = () => {
        this.statusCode = gatheringStatus(pc.iceGatheringState);
        if (pc.iceGatheringState === 'complete') {
          pc.removeEventListener('icegatheringstatechange', stateChangeCallback);
          this.statusCode = Status.IceComplete;
          return resolve('complete'); // DONE !!
        }
      };

      pc.addEventListener('icegatheringstatechange', stateChangeCallback);
    });
  }

  showStatusBar(hover?: boolean) {
    if (this.hoverStatusBar) {
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

  getInfoPanelTop(hover: boolean) {
    if (this.hideStatusBar) {
      return 0;
    }
    if (this.hoverStatusBar && !hover) {
      return 0;
    }
    return this.statusBarHeight;
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

  get activeIconColor() {
    if (this.value.active) {
      return 'success';
    } else {
      return '';
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

  get enableInfoPanel() {
    if (!this.showInformationPanel) {
      return false;
    }
    if (!this.online) {
      return false;
    }
    if (!this.channelOpened) {
      return false;
    }

    // if (this.value.server_debugging) {
    //   return true;
    // } else {
    //   return this.value.active;
    // }

    return true;
  }

  eventColor(event: VmsChannelEvent) {
    switch (event.code) {
      case VmsChannelEventCode.Emit:
        return this.$vuetify.theme.currentTheme.primary;
      case VmsChannelEventCode.Skip:
        return this.$vuetify.theme.currentTheme.secondary;
      case VmsChannelEventCode.Disabled:
        return this.$vuetify.theme.currentTheme.secondary;
      case VmsChannelEventCode.NotReadyRoi:
        return this.$vuetify.theme.currentTheme.warning;
      case VmsChannelEventCode.NotReadyFilters:
        return this.$vuetify.theme.currentTheme.warning;
      case VmsChannelEventCode.RaiseException:
        return this.$vuetify.theme.currentTheme.error;
      default:
        return this.$vuetify.theme.currentTheme.error;
    }
  }

  eventIcon(event: VmsChannelEvent) {
    return EVENT_CATEGORY_TO_ICON[event.category];
  }

  eventLabel(event: VmsChannelEvent) {
    switch (event.code) {
      case VmsChannelEventCode.Emit:
        return event.message;
      case VmsChannelEventCode.Skip:
        return event.message;
      case VmsChannelEventCode.Disabled:
        return this.$t('vms_channel_meta.disabled').toString();
      case VmsChannelEventCode.NotReadyRoi:
        return this.$t('vms_channel_meta.not_ready_roi').toString();
      case VmsChannelEventCode.NotReadyFilters:
        return this.$t('vms_channel_meta.not_ready_filters').toString();
      case VmsChannelEventCode.RaiseException:
        return this.$t('vms_channel_meta.raise_exception').toString();
      default:
        return this.$t('vms_channel_meta.unknown_code', [event.code]).toString();
    }
  }

  eventTooltip(event: VmsChannelEvent) {
    if (event.items) {
      return JSON.stringify(event.items);
    } else {
      return this.$t('vms_channel_meta.empty_events').toString();
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

  onPause() {
    this.paused = true;
  }

  onPlay() {
    this.paused = false;
  }

  onResize() {
    this.videoWidth = this.rtcVideo.videoWidth;
    this.videoHeight = this.rtcVideo.videoHeight;
  }

  onClickPlay() {
    if (this.paused) {
      this.rtcVideo.play();
    } else {
      this.rtcVideo.pause();
    }
  }

  onClickMore() {
    this.showMoreMenu = true;
  }

  onClickReconnect() {
    this.showMoreMenu = false;
    this.close();
    this.open();
  }

  onChangeActive() {
    const group = this.group;
    const project = this.project;
    const device = this.deviceText;
    this.disableActiveButton = true;

    const updateActiveFlag = !this.value.active;
    const body = {
      active: updateActiveFlag,
    } as VmsUpdateDeviceQ;

    this.$api2
      .patchVmsDevice(group, project, device, body)
      .then(() => {
        this.$set(this.value, 'active', updateActiveFlag);
        this.input();

        this.disableActiveButton = false;
      })
      .catch(error => {
        this.disableActiveButton = false;
        console.error(error);
      });
  }

  onChangeDebugging() {
    const group = this.group;
    const project = this.project;
    const device = this.deviceText;
    this.disableDebugButton = true;

    const updateDebugFlag = !this.value.server_debugging;
    const thenCallback = () => {
      this.$set(this.value, 'server_debugging', updateDebugFlag);
      this.input();

      this.disableDebugButton = false;
    };
    const catchCallback = error => {
      this.disableDebugButton = false;
      console.error(error);
    };

    if (updateDebugFlag) {
      this.$api2
        .postVmsDeviceProcessDebugStart(group, project, device)
        .then(thenCallback)
        .catch(catchCallback);
    } else {
      this.$api2
        .postVmsDeviceProcessDebugStop(group, project, device)
        .then(thenCallback)
        .catch(catchCallback);
    }
  }

  onClickFullscreen() {
    this.showMoreMenu = false;
    this.rtcVideo.requestFullscreen();
  }

  updateEventConfig(config?: VmsEventConfigExtra) {
    if (!config) {
      return;
    }
    if (!(config.x1 && config.y1 && config.x2 && config.y2)) {
      return;
    }
    const context = this.canvasUser.getContext('2d');
    if (!context) {
      return;
    }
    const width = this.canvasUser.width;
    const height = this.canvasUser.height;
    if (!(width && height)) {
      return;
    }

    this.roiLeft = config.x1 * width;
    this.roiRight = config.x2 * width;
    this.roiTop = config.y1 * height;
    this.roiBottom = config.y2 * height;

    const roiWidth = this.roiRight - this.roiLeft;
    const roiHeight = this.roiBottom - this.roiTop;

    context.lineWidth = this.lineWidth;
    context.strokeStyle = this.strokeStyle;
    context.clearRect(0, 0, width, height);
    context.strokeRect(this.roiLeft, this.roiTop, roiWidth, roiHeight);
  }

  @Watch('value', {deep: true})
  onWatchValue() {
    this.activeSwitch = this.value.active ?? false;
    this.debugSwitch = this.value.server_debugging ?? false;
  }

  @Watch('eventConfig')
  onWatchEventConfig(newVal?: VmsEventConfigExtra) {
    this.updateEventConfig(newVal);
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
    this.$nextTick(() => {
      this.updateEventConfig(this.eventConfig);
    });

    return {width: this.videoWidth, height: this.videoHeight};
  }

  @Emit()
  input() {
    return this.value;
  }

  @Emit()
  contextmenu(event) {
    return event;
  }

  @Emit('pipette')
  pipette(color: PixelRgb) {
    return color;
  }

  @Emit('roi')
  roi(left: number, right: number, top: number, bottom: number) {
    return {
      x1: left,
      y1: top,
      x2: right,
      y2: bottom,
    } as Roi;
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
      this.editRoi = true;
    }
  }

  onMouseMoveMediaContent(event) {
    if (this.useAnnotationTools && this.editRoi) {
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
      context.lineWidth = this.lineWidth;
      context.strokeStyle = this.strokeStyle;
      context.clearRect(0, 0, width, height);
      context.strokeRect(this.roiLeft, this.roiTop, roiWidth, roiHeight);
    }
  }

  onMouseUpMediaContent(event) {
    if (this.useAnnotationTools && this.editRoi) {
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
      context.lineWidth = this.lineWidth;
      context.strokeStyle = this.strokeStyle;
      context.clearRect(0, 0, width, height);
      context.strokeRect(this.roiLeft, this.roiTop, roiWidth, roiHeight);
      this.roiRight = imageX;
      this.roiBottom = imageY;
      this.editRoi = false;
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

  snapshotAsImageData(clear = true) {
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

  snapshotAsDataUrl(contentType = 'image/png', clear = true) {
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
      throw new Error("Not exists 2d context from user's canvas.");
    }

    const image = this.snapshotAsImageData(true);
    const pixels = image.data;

    const i = (x + y * width) * 4;
    const r = pixels[i];
    const g = pixels[i + 1];
    const b = pixels[i + 2];
    return {r, g, b} as PixelRgb;
  }

  clearAnnotations() {
    this.roiLeft = 0;
    this.roiRight = 0;
    this.roiTop = 0;
    this.roiBottom = 0;
    this.editRoi = false;

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

$status-bar-transparent: 0.6;
$information-panel-transparent: 0.4;

.theme--light.v-application {
  .media-player {
    background-color: $color-grey-lighten-1;

    .status-bar {
      background-color: rgba(map-get($shades, 'white'), $status-bar-transparent);
    }

    .information-panel {
      background-color: rgba(map-get($shades, 'white'), $information-panel-transparent);
    }
  }
}

.theme--dark.v-application {
  .media-player {
    background-color: $color-grey-darken-3;

    .status-bar {
      background-color: rgba(map-get($shades, 'black'), $status-bar-transparent);
    }

    .information-panel {
      background-color: rgba(map-get($shades, 'black'), $information-panel-transparent);
    }
  }
}

@mixin media-block {
  position: absolute;

  padding: 0;
  margin: 0;

  width: 100%;
  height: 100%;

  object-fit: contain;
  object-position: center;

  //left: 0;
  //top: 0;
  //left: 50%;
  //top: 50%;
  //transform: translate(-50%, -50%);
}

.media-player {
  // Important:
  // Required to fix the position of the 'absolute block' among the child elements.
  // https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block
  position: relative;

  display: flex;

  padding: 0;
  margin: 0;

  min-width: 64px;
  min-height: 64px;

  .status-bar {
    position: absolute;
    width: 100%;
    top: 0;

    display: flex;
    flex-direction: row;
    align-items: center;

    padding: 0 4px;
    margin: 0;

    z-index: 50;
  }

  .information-panel {
    position: absolute;

    display: flex;
    flex-direction: column;

    padding: 0 4px 0 4px;
    margin: 4px 4px 0 4px;

    z-index: 60;
  }

  .controller {
    position: absolute;
    width: 100%;
    bottom: 0;

    display: flex;
    flex-direction: row;
    align-items: center;

    padding: 0;
    margin: 0;

    z-index: 70;
  }

  .media-placeholder {
    padding: 0;
    margin: 0;

    .canvas-user {
      @include media-block;
      z-index: 40;
    }

    .canvas-meta {
      @include media-block;
      z-index: 30;
    }

    .canvas-snap {
      @include media-block;
      z-index: 10;
    }

    .video-player {
      @include media-block;
    }
  }

  .brand-logo-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;

    width: 100%;
    height: 100%;

    padding: 0;
    margin: 0;

    .brand-logo {
      min-width: 8px;
      min-height: 8px;

      max-width: 256px;
      max-height: 256px;
    }
  }
}
</style>
