<i18n lang="yaml">
en:
  labels:
    today: 'Today'
  hints:
    logo_alt: 'Answer'
  tooltips:
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
  labels:
    today: '오늘'
  hints:
    logo_alt: 'Answer'
  tooltips:
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
  <div class="d-flex flex-column">
    <v-hover v-slot="{hover}">
      <div class="hls-player" @contextmenu="contextmenu" :style="hlsPlayerStyle">
        <v-sheet
          v-if="showInformationPanel && hlsUrl"
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

        <div class="hls-placeholder">
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
            v-show="hlsUrl"
            class="video"
            ref="video"
            muted
            playsinline
            preload="auto"
            @pause="onPause"
            @play="onPlay"
            @resize="onResize"
          ></video>
        </div>

        <div v-show="!hlsUrl" class="brand-logo-container">
          <img
            class="brand-logo"
            src="@/assets/logo/answer-logo-notext.svg"
            :alt="$t('hints.logo_alt')"
          />
        </div>
      </div>
    </v-hover>

    <div class="hls-controllers">
      <div class="hls-controller-left">
        <v-menu
          offset-y
          transition="scale-transition"
          min-width="auto"
          v-model="showDateMenu"
          :disabled="loading"
          :nudge-right="datePickerSize"
          :close-on-content-click="false"
        >
          <template v-slot:activator="{on, attrs}">
            <v-btn icon v-bind="attrs" v-on="on">
              <v-icon>mdi-calendar</v-icon>
            </v-btn>
          </template>
          <v-date-picker
            no-title
            scrollable
            v-model="date"
            :min="begin"
            :max="end"
            :disabled="loading"
            :allowed-dates="allowedDates"
            @change="onChangeDate"
          ></v-date-picker>
        </v-menu>
        <span class="mr-2 text--secondary text-caption">{{ date }}</span>
        <v-btn
          color="secondary"
          outlined
          rounded
          x-small
          :disabled="loading"
          @click="onClickToday"
        >
          {{ $t('labels.today') }}
        </v-btn>
      </div>

      <div class="hls-controller-center">
        <v-btn
          class="mr-2"
          icon
          outlined
          small
          :disabled="disabled || disablePrevious || loading"
          @click="onClickFirst"
        >
          <v-icon small>mdi-skip-backward</v-icon>
        </v-btn>
        <v-btn
          class="mr-2"
          icon
          outlined
          :disabled="disabled || disablePrevious || loading"
          @click="onClickPrevious"
        >
          <v-icon>mdi-skip-previous</v-icon>
        </v-btn>
        <v-btn
          class="mr-2"
          icon
          large
          outlined
          :disabled="disabled"
          @click="onClickPlay"
        >
          <v-icon large>{{ playIcon }}</v-icon>
        </v-btn>
        <v-btn
          class="mr-2"
          icon
          outlined
          :disabled="disabled || disableNext || loading"
          @click="onClickNext"
        >
          <v-icon>mdi-skip-next</v-icon>
        </v-btn>
        <v-btn
          icon
          outlined
          small
          :disabled="disabled || disableNext || loading"
          @click="onClickLast"
        >
          <v-icon small>mdi-skip-forward</v-icon>
        </v-btn>
      </div>

      <div class="hls-controller-right"></div>
    </div>

    <record-controller
      class="mt-2"
      :disabled="disabled"
      :record-ranges="recordRanges"
      :event-offsets="eventOffsets"
      :cursor-position="cursorPosition"
      @click="onClickRecordController"
    ></record-controller>

    <div class="d-flex flex-row">
      <span class="text--secondary text-overline">00:00:00</span>
      <v-spacer></v-spacer>
      <span class="text--secondary text-overline">23:59:59</span>
    </div>

    <div v-if="false" class="d-flex flex-column">
      <span>{{ `cursorPos: ${cursorPosition}` }}</span>
      <span>{{ `sn: ${sn}` }}</span>
      <span>{{ `relurl: ${relurl}` }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Emit, Prop, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import RecordController, {
  RatioRange,
  MILLISECONDS_TO_DAY,
} from '@/media/RecordController.vue';
import {
  EmptyException,
  IllegalStateException,
  InaccessibleAreaException,
  InvalidRangeException,
  UndefinedException,
  UnsupportedException,
} from '@/exceptions';
import colors from 'vuetify/lib/util/colors';
import Hls from 'hls.js';
import type {HlsConfig, Fragment} from 'hls.js';
import {
  ANY_DEVICE_UID,
  EVENT_CATEGORY_TO_ICON,
  VMS_CHANNEL_META_CODE_BAD_ARGUMENT,
  VMS_CHANNEL_META_CODE_FILTERED,
  VMS_CHANNEL_META_CODE_NOT_READY_ROI,
  VMS_CHANNEL_META_CODE_OPENED,
  VMS_CHANNEL_META_CODE_SUCCESS,
  VmsChannelEvent,
  VmsChannelEventCode,
  VmsEventA,
  VmsFilterEventQ,
} from '@/packet/vms';
import {todayString} from '@/chrono/date';
import moment from 'moment';
import {VmsRecordRangeA} from '@/packet/vms/record_range';

const ONE_SECOND_TO_MILLISECONDS = 1000;
const FRAGMENT_DATETIME_REGEX = /(\d+)-(\d+)-(\d+)\/(\d+)_(\d+)_(\d+)\.(\d+)\.ts$/;

function parseFragmentDateTime(url: string) {
  const match = FRAGMENT_DATETIME_REGEX.exec(url);
  if (!match) {
    throw new IllegalStateException('The URL `Fragment` is malformed');
  }

  const year = match[1];
  const month = match[2];
  const day = match[3];
  const hour = match[4];
  const minute = match[5];
  const second = match[6];
  const micro = match[7];
  const time = `${year}-${month}-${day}T${hour}:${minute}:${second}.${micro}`;
  return moment(time);
}

@Component({
  components: {
    RecordController,
  },
})
export default class HlsPlayer extends VueBase {
  @Prop({type: Number, default: 40})
  readonly datePickerSize!: number;

  @Prop({type: String, default: ''})
  readonly group!: string;

  @Prop({type: String, default: ''})
  readonly project!: string;

  @Prop({type: [String, Number]})
  readonly device?: string | number;

  @Prop({type: Boolean, default: false})
  readonly hideCanvasUser!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideCanvasMeta!: boolean;

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

  @Prop({type: Boolean, default: false})
  readonly disableAspectRatio!: boolean;

  @Prop({type: Number, default: 100})
  readonly refreshMilliseconds!: number;

  @Ref('video')
  readonly video!: HTMLVideoElement;

  loading = false;

  hlsOptions = {} as HlsConfig;
  hls?: Hls;
  hlsUrl = '';

  paused = true;
  videoWidth = 0;
  videoHeight = 0;

  showInformationPanel = true;
  informationCode = VMS_CHANNEL_META_CODE_SUCCESS;
  informationText = '';
  informationDate = '';

  currentFragment?: Fragment;
  currentFragmentMoment?: moment.Moment;
  currentFragmentVideoTime = 0;
  cursorPosition = 0;
  fragments = [] as Array<Fragment>;
  totalDuration = 0;

  skipNextRefresh = false;
  refreshIntervalHandle = -1;

  recordDates = [] as Array<string>;

  showDateMenu = false;
  begin = '';
  end = '';
  date = '';

  recordRanges = [] as Array<RatioRange>;
  eventOffsets = [] as Array<number>;

  loadingEvent = false;
  eventsBuffer = new Map<number, VmsEventA>();
  eventsIndexes = [] as Array<number>;
  eventsDownloadQueue = [] as Array<number>;
  nextEventIndex?: number = undefined;
  prevRefreshMilliseconds = 0;
  events = [] as Array<VmsChannelEvent>;

  mounted() {
    this.hlsOptions = {
      debug: false,
      enableWorker: true,
      lowLatencyMode: true,
      backBufferLength: 60 * 1.5,
      xhrSetup: this._xhrSetup,
      licenseXhrSetup: this._licenseXhrSetup,
    } as HlsConfig;

    if (typeof this.$route.params.date !== 'undefined') {
      this.date = this.$route.params.date;
    } else {
      this.date = todayString();
    }

    this.$api2
      .getVmsRecordsPdeviceDates(this.group, this.project, this.deviceText)
      .then(items => {
        this.recordDates = items;
        if (items) {
          this.begin = items[0];
          this.end = items[items.length - 1];
          this.updateHls(this.date);
        }
      })
      .catch(error => {
        this.toastRequestFailure(error);
      });

    this.refreshIntervalHandle = window.setInterval(() => {
      this.onRefresh();
    }, this.refreshMilliseconds);
  }

  _xhrSetup(xhr: XMLHttpRequest, url: string) {
    const bearerToken = `Bearer ${this.$localStore.access}`;
    xhr.setRequestHeader('Authorization', bearerToken);
  }

  _licenseXhrSetup(xhr: XMLHttpRequest, url: string) {
    const bearerToken = `Bearer ${this.$localStore.access}`;
    xhr.setRequestHeader('Authorization', bearerToken);
  }

  beforeDestroy() {
    if (this.refreshIntervalHandle != -1) {
      window.clearInterval(this.refreshIntervalHandle);
    }
    this.closeHls();
  }

  closeHls() {
    if (this.hls) {
      this.hls.destroy();
      this.hls = undefined;
    }
  }

  get hlsPlayerStyle() {
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

  get informationIconColor() {
    switch (this.informationCode) {
      case VMS_CHANNEL_META_CODE_SUCCESS: // TODO: Replace to enum.
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
      case VMS_CHANNEL_META_CODE_SUCCESS: // TODO: Replace to enum.
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

  get playIcon() {
    if (this.paused) {
      return 'mdi-play';
    } else {
      return 'mdi-pause';
    }
  }

  get dateStart() {
    return `${this.date}T00:00:00.000`;
  }

  get dateLast() {
    return `${this.date}T23:59:59.999`;
  }

  get disabled() {
    return !this.hlsUrl;
  }

  get disablePrevious() {
    if (this.recordDates.length === 0) {
      return true;
    }
    const index = this.recordDates.findIndex(x => x === this.date);
    if (index === -1) {
      return true;
    }
    return index === 0;
  }

  get disableNext() {
    if (this.recordDates.length === 0) {
      return true;
    }
    const index = this.recordDates.findIndex(x => x === this.date);
    if (index === -1) {
      return true;
    }
    return index === this.recordDates.length - 1;
  }

  updateHls(date: string) {
    if (!Hls.isSupported()) {
      this.hls = undefined;
      throw new UnsupportedException('Unsupported HLS.js component');
    }

    if (this.hls) {
      this.hls.destroy();
      this.hls = undefined;
    }

    if (!this.recordDates.includes(date)) {
      return;
    }

    try {
      const url = this.$api2.urlVmsRecordsPdevicePlaylistMaster(
        this.group,
        this.project,
        this.deviceText,
        this.dateStart,
        this.dateLast,
      );

      const hls = new Hls(this.hlsOptions);
      hls.on(Hls.Events.MANIFEST_PARSED, this.onManifestParsed);
      hls.on(Hls.Events.FRAG_CHANGED, this.onFragChanged);
      hls.on(Hls.Events.ERROR, this.onError);
      hls.loadSource(url);
      hls.attachMedia(this.video);
      this.hls = hls;
      this.hlsUrl = url;
    } catch (error) {
      this.toastError(`Update HLS failure: ${error}`);
    }
  }

  onManifestParsed(event, data) {
    // console.debug(event, data);
    // index of first quality level appearing in Manifest.
    const firstLevel = data.firstLevel;
    if (firstLevel >= data.levels.length) {
      const msg1 = `Overflow firstLevel(${firstLevel}) index, `;
      const msg2 = `levels.length(${data.levels.length})`;
      throw new IllegalStateException(msg1 + msg2);
    }

    const level = data.levels[firstLevel];
    const levelDetails = level.details;
    if (!levelDetails) {
      return;
    }

    this.fragments = levelDetails.fragments;
    this.totalDuration = levelDetails.totalduration;
    const count = this.fragments.length;
    console.debug(`Total fragments count=${count},totalDuration=${this.totalDuration}`);

    this.loading = true;
    (async () => {
      await this.setupPrerequisiteDatas();
    })();
  }

  sn: any = 0;
  relurl = '';

  onFragChanged(event, data) {
    // console.debug(event, data);
    this.currentFragment = data.frag;
    if (!this.currentFragment) {
      throw new UndefinedException('Current fragment is undefined or null');
    }

    if (!this.currentFragment.relurl) {
      throw new EmptyException('Not exists fragment url');
    }

    this.sn = this.currentFragment.sn;
    this.relurl = this.currentFragment.relurl;
  }

  onError(event, data) {
    console.debug(event, data);
  }

  async setupPrerequisiteDatas() {
    const begin = moment(this.dateStart);
    const beginValue = begin.valueOf();

    try {
      const ranges = await this.$api2.getVmsRecordsPdeviceRangesPdate(
        this.group,
        this.project,
        this.deviceText,
        this.date,
      );
      const ratioRanges = ranges.map(x => {
        const startTime = moment(x.start);
        const lastTime = moment(x.last);
        return {
          startTime: startTime,
          lastTime: lastTime,
          start: (startTime.valueOf() - beginValue) / MILLISECONDS_TO_DAY,
          last: (lastTime.valueOf() - beginValue) / MILLISECONDS_TO_DAY,
        };
      });
      const ratioOfDay = ratioRanges
        .map(x => x.last - x.start)
        .reduce((total, x) => total + x);
      this.recordRanges = ratioRanges.map(x => {
        return {
          startTime: x.startTime,
          lastTime: x.lastTime,
          start: x.start,
          last: x.last,
          ratio: (x.last - x.start) / ratioOfDay,
        };
      });

      const offsets = await this.$api2.getVmsDeviceEventsTimesPdateOffset(
        this.group,
        this.project,
        this.deviceText,
        this.date,
      );
      this.eventOffsets = offsets.map(x => {
        return (x * ONE_SECOND_TO_MILLISECONDS) / MILLISECONDS_TO_DAY;
      });
      this.cursorPosition = this.eventOffsets[0];

      const begin = moment(`${this.date}T00:00:00`);
      const offsetMilliseconds = this.cursorPosition * MILLISECONDS_TO_DAY;
      const cursorTime = begin.clone().add(offsetMilliseconds, 'milliseconds');
      const cursorHour = cursorTime.hour();

      const hours = [...Array(24).keys()];
      this.eventsIndexes = [];
      this.nextEventIndex = undefined;
      this.eventsBuffer.clear();
      this.eventsDownloadQueue = [cursorHour, ...hours.filter(x => x != cursorHour)];
      this.events = [];
      // console.debug(`Enqueue event hours: ${this.eventsDownloadQueue}`);
    } catch (error) {
      this.recordRanges = [];
      this.eventOffsets = [];
      this.cursorPosition = 0;
      this.eventsIndexes = [];
      this.nextEventIndex = undefined;
      this.eventsBuffer.clear();
      this.eventsDownloadQueue = [];
      this.events = [];
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  findNearestRatioRangeIndex(time: moment.Moment) {
    if (!this.recordRanges) {
      throw new IllegalStateException('`recordRanges` does not exist.');
    }

    const firstRange = this.recordRanges[0];
    if (this.recordRanges.length === 1) {
      return 0;
    }

    const timeValue = time.valueOf();
    const startValue = firstRange.startTime.valueOf();
    const lastValue = firstRange.lastTime.valueOf();

    let nearestIndex = 0;
    let nearestDistance;
    if (timeValue < startValue) {
      nearestDistance = startValue - timeValue;
    } else if (lastValue < timeValue) {
      nearestDistance = timeValue - lastValue;
    } else {
      console.assert(startValue <= timeValue && timeValue <= lastValue);
      return 0;
    }

    for (let i = 1; i < this.recordRanges.length; ++i) {
      const range = this.recordRanges[i];
      const startValue = range.startTime.valueOf();
      const lastValue = range.lastTime.valueOf();

      let currentDistance;
      if (timeValue < startValue) {
        currentDistance = startValue - timeValue;
      } else if (lastValue < timeValue) {
        currentDistance = timeValue - lastValue;
      } else {
        console.assert(startValue <= timeValue && timeValue <= lastValue);
        return i;
      }

      if (currentDistance < nearestDistance) {
        nearestDistance = currentDistance;
        nearestIndex = i;
      }
    }

    return nearestIndex;
  }

  absTimeToCurrentMilliseconds(time: moment.Moment) {
    const findIndex = this.findNearestRatioRangeIndex(time);
    let totalMilliseconds = 0.0;
    for (let i = 0; i < findIndex; ++i) {
      const range = this.recordRanges[i];
      const startValue = range.startTime.valueOf();
      const lastValue = range.lastTime.valueOf();
      console.assert(lastValue >= startValue);
      totalMilliseconds += lastValue - startValue;
    }

    const timeValue = time.valueOf();
    const range = this.recordRanges[findIndex];
    const startValue = range.startTime.valueOf();
    const lastValue = range.lastTime.valueOf();
    if (timeValue < startValue) {
      return totalMilliseconds;
    } else if (lastValue < timeValue) {
      return totalMilliseconds + (lastValue - startValue);
    } else {
      console.assert(startValue <= timeValue && timeValue <= lastValue);
      return totalMilliseconds + (timeValue - startValue);
    }
  }

  currentMillisecondsToAbsTime(currentMilliseconds: number) {
    if (this.recordRanges.length === 0) {
      throw new IllegalStateException('`recordRanges` is not ready');
    }

    let remainMilliseconds = currentMilliseconds;
    let findIndex = 0;
    for (; findIndex < this.recordRanges.length; ++findIndex) {
      const range = this.recordRanges[findIndex];
      const startValue = range.startTime.valueOf();
      const lastValue = range.lastTime.valueOf();
      console.assert(lastValue >= startValue);
      const durationMilliseconds = lastValue - startValue;

      if (durationMilliseconds >= remainMilliseconds) {
        break;
      }
      remainMilliseconds -= durationMilliseconds;
    }

    const range = this.recordRanges[findIndex];
    const start = range.startTime;
    const result = start.clone();
    result.add(remainMilliseconds, 'milliseconds');
    return result;
  }

  absTimeToVideoRatio(time: moment.Moment) {
    const findIndex = this.findNearestRatioRangeIndex(time);
    let totalRatio = 0.0;
    for (let i = 0; i < findIndex; ++i) {
      const range = this.recordRanges[i];
      totalRatio += range.ratio;
    }

    const timeValue = time.valueOf();
    const range = this.recordRanges[findIndex];
    const startValue = range.startTime.valueOf();
    const lastValue = range.lastTime.valueOf();
    if (timeValue < startValue) {
      return totalRatio;
    } else if (lastValue < timeValue) {
      return totalRatio + range.ratio;
    } else {
      console.assert(startValue <= timeValue && timeValue <= lastValue);
      const timeRatio = (timeValue - startValue) / (lastValue - startValue);
      return totalRatio + timeRatio * range.ratio;
    }
  }

  videoRatioToAbsTime(ratio: number) {
    let remainRatio = ratio;
    let findIndex = 0;
    for (; findIndex < this.recordRanges.length; ++findIndex) {
      const range = this.recordRanges[findIndex];
      const startValue = range.startTime.valueOf();
      const lastValue = range.lastTime.valueOf();
      console.assert(lastValue >= startValue);

      if (range.ratio >= remainRatio) {
        break;
      }
      remainRatio -= range.ratio;
    }

    const range = this.recordRanges[findIndex];
    const timeRatio = remainRatio / range.ratio;
    console.assert(0 <= timeRatio && timeRatio <= 1);

    const start = range.startTime;
    const last = range.lastTime;
    const rangeDuration = last.diff(start, 'milliseconds');
    const offsetMilliseconds = rangeDuration * timeRatio;

    const result = start.clone();
    result.add(offsetMilliseconds, 'milliseconds');
    return result;
  }

  allowedDates(value: string) {
    return this.recordDates.includes(value);
  }

  getSeekableEnd() {
    if (isFinite(this.video.duration)) {
      return this.video.duration;
    }
    if (this.video.seekable.length) {
      return this.video.seekable.end(this.video.seekable.length - 1);
    }
    return 0;
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

  @Emit()
  contextmenu(event) {
    return event;
  }

  onRefresh() {
    // if (!this.currentFragmentMoment) {
    //   return;
    // }
    // if (this.skipNextRefresh) {
    //   this.skipNextRefresh = false;
    //   return;
    // }

    // const begin = moment(`${this.date}T00:00:00`);
    // const pivotMilliseconds = this.currentFragmentMoment.diff(begin, 'milliseconds');
    // const offsetVideoTime = this.video.currentTime - this.currentFragmentVideoTime;
    // const offsetMilliseconds = Math.round(offsetVideoTime * ONE_SECOND_TO_MILLISECONDS);
    // const currentMilliseconds = pivotMilliseconds + offsetMilliseconds;
    //
    // this.cursorPosition = currentMilliseconds / MILLISECONDS_TO_DAY;
    // console.debug(`onRefresh: cursorPosition=${this.cursorPosition},duration=${this.video.duration},totalDuration=${this.totalDuration}`);

    this.bufferingEvents();

    // if (this.video.paused) {
    //   return;
    // }

    const videoCurrentMilliseconds =
      this.video.currentTime * ONE_SECOND_TO_MILLISECONDS;
    const currentTime = this.currentMillisecondsToAbsTime(videoCurrentMilliseconds);
    const currentTimeValue = currentTime.valueOf();
    // console.debug(`onRefresh(currentTime=${currentTime})`);

    if (this.eventsIndexes.length >= 1) {
      if (typeof this.nextEventIndex === 'undefined') {
        this.nextEventIndex = this.eventsIndexes.findIndex(x => x > currentTimeValue);
      }

      if (this.nextEventIndex !== -1) {
        const nextEventTimeValue = this.eventsIndexes[this.nextEventIndex];
        if (currentTimeValue >= nextEventTimeValue) {
          const event = this.eventsBuffer.get(nextEventTimeValue);
          if (!event) {
            throw new UndefinedException(`Not found event key: ${nextEventTimeValue}`);
          }

          // console.debug(`Found event:`, event);

          if (event.extra) {
            this.events = [event.extra];
          } else {
            this.events = [];
          }

          if (this.nextEventIndex + 1 >= this.eventsIndexes.length) {
            this.nextEventIndex = -1; // EOF Events
          } else {
            this.nextEventIndex += 1;
          }
        } else {
          const leftMilliseconds = nextEventTimeValue - currentTimeValue;
          const leftSeconds = leftMilliseconds / ONE_SECOND_TO_MILLISECONDS;
          // console.debug(`Next event left time: ${leftSeconds}s`);
        }
      }
    }

    this.prevRefreshMilliseconds = currentTimeValue;

    const begin = moment(`${this.date}T00:00:00`).valueOf();
    const pos = (currentTime.valueOf() - begin.valueOf()) / MILLISECONDS_TO_DAY;
    console.assert(0 <= pos && pos <= 1);
    this.cursorPosition = pos;
    // console.debug(`onRefresh(pos=${pos},currentTime=${this.video.currentTime})`);

    // const begin = moment(`${this.date}T00:00:00`);
    // const offsetMilliseconds = (pos * MILLISECONDS_TO_DAY)
    // const cursorTime = begin.clone().add(offsetMilliseconds, 'milliseconds');
  }

  bufferingEvents() {
    if (this.loadingEvent) {
      return;
    } else if (this.eventsDownloadQueue.length >= 1) {
      this.loadingEvent = true;

      const cursor = this.eventsDownloadQueue.splice(0, 1);
      console.assert(cursor.length === 1);
      const hour = cursor[0];
      const last = this.eventsDownloadQueue.length === 0;

      (async () => {
        try {
          await this.onBufferingEvents(this.date, hour, last);
        } finally {
          this.loadingEvent = false;
        }
      })();
    }
  }

  async onBufferingEvents(date: string, hour: number, last = false) {
    const hourText = hour.toString().padStart(2, '0');
    // console.debug(`Buffering events: ${date}T${hourText} ...`);

    const body = {
      time_left: `${date}T${hourText}:00:00.000`,
      time_right: `${date}T${hourText}:59:59.999`,
      device_uid: this.deviceNumber,
    } as VmsFilterEventQ;

    const events = await this.$api2.postVmsEventsFilter(this.group, this.project, body);
    if (this.date != date) {
      throw new IllegalStateException('`date` changed while event buffering');
    }

    for (const e of events) {
      this.eventsBuffer.set(moment(e.time).valueOf(), e);
    }

    // console.debug(`Total events size: ${this.eventsBuffer.size}`);
    this.eventsIndexes = [...this.eventsBuffer.keys()];
    this.nextEventIndex = undefined;
    if (last) {
      console.debug(`Total events: ${this.eventsIndexes.length}`);
    }
  }

  // drawBuffered() {
  //   const seekableEnd = this.getSeekableEnd();
  //   const r = this.video.buffered;
  //   if (r) {
  //     const pos = this.video.currentTime;
  //     let bufferLen = 0;
  //     ctx.fillStyle = 'gray';
  //     for (let i = 0; i < r.length; i++) {
  //       const start = (r.start(i) / seekableEnd) * canvas.width;
  //       const end = (r.end(i) / seekableEnd) * canvas.width;
  //       ctx.fillRect(start, 2, Math.max(2, end - start), 11);
  //       if (pos >= r.start(i) && pos < r.end(i)) {
  //         // play position is inside this buffer TimeRange,
  //         // retrieve end of buffer position and buffer length
  //         bufferLen = r.end(i) - pos;
  //       }
  //     }
  //   }
  // }

  onChangeDate(event: string) {
    this.showDateMenu = false;
    this.updateHls(event);
  }

  onClickToday() {
    this.date = todayString();
    this.updateHls(this.date);
  }

  onClickFirst() {
    this.date = this.recordDates[0];
    this.updateHls(this.date);
  }

  onClickPrevious() {
    const index = this.recordDates.findIndex(x => x === this.date);
    this.date = this.recordDates[index - 1];
    this.updateHls(this.date);
  }

  onClickPlay() {
    if (this.video.paused) {
      this.video.play();
    } else {
      this.video.pause();
    }
  }

  onClickNext() {
    const index = this.recordDates.findIndex(x => x === this.date);
    this.date = this.recordDates[index + 1];
    this.updateHls(this.date);
  }

  onClickLast() {
    this.date = this.recordDates[this.recordDates.length - 1];
    this.updateHls(this.date);
  }

  // findNearestFragment(time: moment.Moment) {
  //   if (this.fragments.length === 0) {
  //     return;
  //   }
  //
  //   const cursorValue = time.valueOf();
  //   let nearestFragment: undefined | Fragment = undefined;
  //   let nearestDistance: undefined | number = undefined;
  //
  //   for (let i = 0; i < this.fragments.length; ++i) {
  //     const f = this.fragments[i];
  //     if (!f.relurl) {
  //       throw new EmptyException('Not exists fragment url');
  //     }
  //     const start = parseFragmentDateTime(f.relurl);
  //     const duration = f.duration > 0 ? f.duration : 10;
  //     const durationMilliseconds = Math.round(duration * ONE_SECOND_TO_MILLISECONDS);
  //     const last = start.clone().add(durationMilliseconds, 'milliseconds');
  //
  //     const startValue = start.valueOf();
  //     const lastValue = last.valueOf();
  //     // console.debug(`findNearestFragment-> start: ${start.format('LLLL')}`)
  //     // console.debug(`findNearestFragment-> durationMilliseconds: ${durationMilliseconds}`)
  //     // console.debug(`findNearestFragment-> last: ${last.format('LLLL')}`)
  //     console.assert(startValue <= lastValue, `startValue(${startValue}) <= lastValue(${lastValue}), duration(${durationMilliseconds})`);
  //
  //     let distance;
  //     if (cursorValue < startValue) {
  //       distance = startValue - cursorValue;
  //     } else if (startValue <= cursorValue && cursorValue <= lastValue) {
  //       return f;  // Excellent correct!
  //     } else if (lastValue < cursorValue) {
  //       distance = cursorValue - lastValue;
  //     } else {
  //       throw new InaccessibleAreaException();
  //     }
  //
  //     if (nearestFragment && typeof nearestDistance !== 'undefined') {
  //       if (distance < nearestDistance) {
  //         nearestFragment = f;
  //         nearestDistance = distance;
  //       }
  //     } else {
  //       // First beginning.
  //       nearestFragment = f;
  //       nearestDistance = distance;
  //     }
  //   }
  //
  //   return nearestFragment;
  // }

  onClickRecordController(pos: number) {
    console.assert(0 <= pos && pos <= 1);

    const begin = moment(`${this.date}T00:00:00`);
    const offsetMilliseconds = pos * MILLISECONDS_TO_DAY;
    const cursorTime = begin.clone().add(offsetMilliseconds, 'milliseconds');

    const currentMilliseconds = this.absTimeToCurrentMilliseconds(cursorTime);
    // this.cursorPosition = pos;  // [IMPORTANT] Don't change cursorPosition
    this.video.currentTime = currentMilliseconds / ONE_SECOND_TO_MILLISECONDS;
    this.events = [];
    this.nextEventIndex = undefined;
    console.debug(
      `onClickRecordController(pos=${pos},currentTime=${this.video.currentTime})`,
    );

    // const videoRatio = this.absTimeToVideoRatio(cursorTime);
    // this.cursorPosition = pos;
    // this.video.currentTime = videoRatio * this.getSeekableEnd();
    // console.debug(`onClickRecordController(pos=${pos},cursorTime=${cursorTime},videoRatio=${videoRatio},currentTime=${this.video.currentTime})`);

    // // console.debug(`pos=${pos} -> ${cursorTime.format('LLLL')}`)
    //
    // const nearestFragment = this.findNearestFragment(cursorTime);
    // if (!nearestFragment) {
    //   return;
    // }
    // if (!nearestFragment.relurl) {
    //   throw new EmptyException('Not exists fragment url');
    // }
    //
    // console.debug(`Nearest fragment: #${nearestFragment.sn}`);
    //
    // const start = parseFragmentDateTime(nearestFragment.relurl);
    // const durationMilliseconds = Math.round(nearestFragment.duration * ONE_SECOND_TO_MILLISECONDS);
    // const last = start.clone().add(durationMilliseconds, 'milliseconds');
    // const startValue = start.valueOf();
    // const lastValue = last.valueOf();
    // console.assert(startValue <= lastValue);
    //
    // const cursorValue = cursorTime.valueOf();
    // let currentTime;
    // if (cursorValue < startValue) {
    //   // Start Position
    //   currentTime = nearestFragment.start;
    // } else if (startValue <= cursorValue && cursorValue <= lastValue) {
    //   // Middle Position
    //   const diffSeconds = (cursorValue - startValue) / ONE_SECOND_TO_MILLISECONDS;
    //   console.assert(diffSeconds < nearestFragment.duration);
    //   currentTime = nearestFragment.start + diffSeconds;
    // } else if (lastValue < cursorValue) {
    //   // Last Position
    //   currentTime = nearestFragment.start + nearestFragment.duration;
    // } else {
    //   throw new InaccessibleAreaException();
    // }
    //
    // this.video.currentTime = currentTime;
    // this.currentFragmentMoment = start;
    // this.currentFragmentVideoTime = currentTime;
    // this.skipNextRefresh = true;
    // this.cursorPosition = pos;
  }

  getInfoPanelTop(hover: boolean) {
    return 0;
  }

  onPause() {
    this.paused = true;
  }

  onPlay() {
    this.paused = false;
  }

  onResize() {
    this.videoWidth = this.video.videoWidth;
    this.videoHeight = this.video.videoHeight;
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

$information-panel-transparent: 0.4;

.theme--light.v-application {
  .hls-player {
    background-color: $color-grey-lighten-1;

    .information-panel {
      background-color: rgba(map-get($shades, 'white'), $information-panel-transparent);
    }
  }
}

.theme--dark.v-application {
  .hls-player {
    background-color: $color-grey-darken-3;

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

.hls-player {
  // Important:
  // Required to fix the position of the 'absolute block' among the child elements.
  // https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block
  position: relative;

  display: flex;
  flex-direction: column;

  padding: 0;
  margin: 0;

  min-width: 64px;
  min-height: 64px;

  .information-panel {
    position: absolute;

    display: flex;
    flex-direction: row;
    align-items: center;

    padding: 0 4px 0 4px;
    margin: 4px 4px 0 4px;

    z-index: 60;
  }

  .hls-placeholder {
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

    .video {
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

.hls-controllers {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;

  padding: 4px;
  margin: 8px 0 0 0;

  width: 100%;

  .hls-controller-left {
    position: absolute;
    left: 0;
  }

  .hls-controller-center {
  }

  .hls-controller-right {
    position: absolute;
    right: 0;
  }
}
</style>
