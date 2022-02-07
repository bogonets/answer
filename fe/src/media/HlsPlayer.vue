<i18n lang="yaml">
en:
  labels:
    today: "Today"
  hints:
    logo_alt: "Answer"
  tooltips:
    latest_event_time: "Latest event time: {0}"

ko:
  labels:
    today: "오늘"
  hints:
    logo_alt: "Answer"
  tooltips:
    latest_event_time: "마지막 이벤트 발생 시간: {0}"
</i18n>

<template>
  <div class="d-flex flex-column">
    <v-hover v-slot="{ hover }">
      <div
          class="hls-player"
          @contextmenu="contextmenu"
          :style="hlsPlayerStyle"
      >
        <v-sheet
            v-if="showInformationPanel && hlsUrl"
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
            :nudge-right="datePickerSize"
            :close-on-content-click="false"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
                icon
                v-bind="attrs"
                v-on="on"
            >
              <v-icon>mdi-calendar</v-icon>
            </v-btn>
          </template>
          <v-date-picker
              no-title
              scrollable
              v-model="date"
              :min="begin"
              :max="end"
              :allowed-dates="allowedDates"
              @change="onChangeDate"
          ></v-date-picker>
        </v-menu>
        <span class="mr-2 text--secondary text-caption">{{ date }}</span>
        <v-btn color="secondary" outlined rounded x-small @click="onClickToday">
          {{ $t('labels.today') }}
        </v-btn>
      </div>

      <div class="hls-controller-center">
        <v-btn
            class="mr-2"
            icon
            outlined
            small
            :disabled="disabled || disablePrevious"
            @click="onClickFirst"
        >
          <v-icon small>mdi-skip-backward</v-icon>
        </v-btn>
        <v-btn
            class="mr-2"
            icon
            outlined
            :disabled="disabled || disablePrevious"
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
            :disabled="disabled || disableNext"
            @click="onClickNext"
        >
          <v-icon>mdi-skip-next</v-icon>
        </v-btn>
        <v-btn
            icon
            outlined
            small
            :disabled="disabled || disableNext"
            @click="onClickLast"
        >
          <v-icon small>mdi-skip-forward</v-icon>
        </v-btn>
      </div>

      <div class="hls-controller-right">
      </div>
    </div>

    <record-controller
        class="mt-2"
        :disabled="disabled"
        :record-ranges="recordRanges"
        :event-ranges="eventRanges"
        :cursor-position="cursorPosition"
        @click="onClickRecordController"
    ></record-controller>

    <div class="d-flex flex-row">
      <span class="text--secondary text-overline">00:00:00</span>
      <v-spacer></v-spacer>
      <span class="text--secondary text-overline">23:59:59</span>
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
  IllegalStateException, InaccessibleAreaException,
  UnsupportedException
} from '@/exceptions';
import colors from 'vuetify/lib/util/colors'
import Hls from 'hls.js';
import type {HlsConfig, Fragment} from 'hls.js';
import {
  ANY_DEVICE_UID,
  VMS_CHANNEL_META_CODE_BAD_ARGUMENT,
  VMS_CHANNEL_META_CODE_FILTERED,
  VMS_CHANNEL_META_CODE_NOT_READY_ROI,
  VMS_CHANNEL_META_CODE_OPENED,
  VMS_CHANNEL_META_CODE_SUCCESS,
  VmsEventA, VmsFilterEventQ,
} from '@/packet/vms';
import {todayString} from '@/chrono/date';
import moment from 'moment';

const ONE_SECOND_TO_MILLISECONDS = 1000;
const FRAGMENT_DATETIME_REGEX = /(\d+)-(\d+)-(\d+)_(\d+)-(\d+)-(\d+)\.ts$/;

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
  return moment(`${year}-${month}-${day}T${hour}:${minute}:${second}`);
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

  hls?: Hls;
  hlsOptions = {} as HlsConfig;
  hlsUrl = '';

  events = [] as Array<VmsEventA>;

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
  eventRanges = [] as Array<RatioRange>;

  mounted() {
    if (typeof this.$route.params.date !== 'undefined') {
      this.date = this.$route.params.date;
    } else {
      this.date = todayString();
    }

    this.hlsOptions = {
      xhrSetup: this._xhrSetup,
      licenseXhrSetup: this._licenseXhrSetup,
    } as HlsConfig;

    this.$api2.getVmsRecordsPdeviceDates(this.group, this.project, this.deviceText)
        .then(items => {
          this.recordDates = items;
          if (items) {
            this.begin = items[0];
            this.end = items[items.length - 1];
            this.updateHlsByDate(this.date);
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
    this.close();
  }

  close() {
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
      case VMS_CHANNEL_META_CODE_SUCCESS:  // TODO: Replace to enum.
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
      case VMS_CHANNEL_META_CODE_SUCCESS:  // TODO: Replace to enum.
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
    return index === (this.recordDates.length - 1);
  }

  changeVideo() {
  }

  updateHlsByDate(date: string) {
    let url;
    if (this.recordDates.includes(date)) {
      url = this.$api2.urlVmsRecordsPdevicePlaylistMaster(
          this.group, this.project, this.deviceText, this.dateStart, this.dateLast
      );
    } else {
      url = '';
    }
    this.updateHls(url);
  }

  updateHls(hlsUrl: string) {
    if (!Hls.isSupported()) {
      this.hls = undefined;
      throw new UnsupportedException('Unsupported HLS.js component');
    }

    if (!hlsUrl) {
      if (this.hls) {
        this.hls.destroy();
        this.hls = undefined;
      }
      return;
    }

    try {
      const hls = new Hls(this.hlsOptions);
      hls.loadSource(hlsUrl);
      hls.attachMedia(this.video);

      // hls.on(Hls.Events.ERROR, (e,d) => {console.debug(e,d);});
      // hls.on(Hls.Events.FRAG_BUFFERED, (e,d) => {console.debug(e,d);});
      // hls.on(Hls.Events.FRAG_LOADING, (e,d) => {console.debug(e,d);});
      // hls.on(Hls.Events.FRAG_LOADED, (e,d) => {console.debug(e,d);});
      // hls.on(Hls.Events.FRAG_PARSED, (e,d) => {console.debug(e,d);});
      // hls.on(Hls.Events.BUFFER_APPENDED, (e,d) => {console.debug(e,d);});
      // hls.on(Hls.Events.BUFFER_EOS, (e,d) => {console.debug(e,d);});
      // hls.on(Hls.Events.LEVEL_PTS_UPDATED, (e,d) => {console.debug(e,d);});

      // fired after manifest has been parsed.
      hls.on(Hls.Events.MANIFEST_PARSED, (event, data) => {
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
        console.debug(`Total fragments count=${this.fragments.length},totalDuration=${this.totalDuration}`);
        this.updateRecordRanges(this.fragments);

        const body = {
          date: this.date,
          device_uid: this.deviceNumber,
        } as VmsFilterEventQ;

        this.$api2.postVmsEventsFilter(this.group, this.project, body)
            .then(items => {
              this.events = items;
              console.debug(`Total events count: ${this.events.length}`);
              this.updateEventRanges(this.events);
            })
            .catch(error => {
              this.events = [];
            });
      });

      // fired when fragment matching with current video position is changing.
      hls.on(Hls.Events.FRAG_CHANGED, (event, data) => {
        this.currentFragment = data.frag;
        const sn = this.currentFragment.sn;
        console.debug(`Change current fragment: #${sn}`);

        if (!this.currentFragment.relurl) {
          throw new EmptyException('Not exists fragment url');
        }

        // this.currentFragmentMoment = parseFragmentDateTime(this.currentFragment.relurl);
        // this.currentFragmentVideoTime = this.video.currentTime;

        // const ct = this.video.currentTime;
        // const d = this.video.duration;
        // console.debug(`Video information: ct=${ct},d=${d}`);
      });

      this.hls = hls;
      this.hlsUrl = hlsUrl;
    } catch (error) {
      this.hls = undefined;
      console.error(error);
    }
  }

  updateRecordRanges(fragments: Array<Fragment>) {
    if (fragments.length === 0) {
      throw new EmptyException('Not exists fragments');
    }

    const resolution = 2 * ONE_SECOND_TO_MILLISECONDS;

    const result = [] as Array<RatioRange>;
    let prevStart: undefined | moment.Moment;
    let prevLast: undefined | moment.Moment;
    let mergedCount = 0;

    for (let i = 0; i < fragments.length; ++i) {
      const f = fragments[i];
      if (!f.relurl) {
        throw new EmptyException('Not exists fragment url');
      }

      const start = parseFragmentDateTime(f.relurl);
      const durationMilliseconds = Math.round(f.duration * ONE_SECOND_TO_MILLISECONDS);
      const last = start.clone().add(durationMilliseconds, 'milliseconds');

      if (prevStart && prevLast) {
        const diff = start.diff(prevLast, 'milliseconds')
        const absDiff = Math.abs(diff);
        if (absDiff < resolution) {
          // This is a `continuous` fragment.
          prevLast = last;
          mergedCount++;
        } else {
          // Flush the previous `range`.
          result.push({
            start: prevStart.valueOf(),
            last: prevLast.valueOf(),
            count: mergedCount,
          } as RatioRange);

          // New beginning.
          prevStart = start;
          prevLast = last;
          mergedCount = 1;
        }
      } else {
        // First beginning.
        prevStart = start;
        prevLast = last;
        mergedCount = 1;
      }
    }

    // Last flush.
    if (prevStart && prevLast) {
      result.push({
        start: prevStart.valueOf(),
        last: prevLast.valueOf(),
        count: mergedCount,
      } as RatioRange);
    }

    const beginDateText = `${this.date}T00:00:00`;
    const begin = moment(beginDateText).valueOf();
    this.recordRanges = result.map(x => {
      return {
        start: (x.start - begin) / MILLISECONDS_TO_DAY,
        last: (x.last - begin) / MILLISECONDS_TO_DAY,
        count: x.count,
      };
    })
  }

  updateEventRanges(events: Array<VmsEventA>) {
    if (events.length === 0) {
      this.eventRanges = [];
      return;
    }

    const resolution = 2 * ONE_SECOND_TO_MILLISECONDS;
    const durationMilliseconds = 1000;

    const result = [] as Array<RatioRange>;
    let prevStart: undefined | moment.Moment;
    let prevLast: undefined | moment.Moment;
    let mergedCount = 0;

    for (let i = 0; i < events.length; ++i) {
      const e = events[i];
      const start = moment(e.time);
      const last = start.clone().add(durationMilliseconds, 'milliseconds');

      if (prevStart && prevLast) {
        const diff = start.diff(prevLast, 'milliseconds')
        const absDiff = Math.abs(diff);
        if (absDiff < resolution) {
          // This is a `continuous` fragment.
          prevLast = last;
          mergedCount++;
        } else {
          // Flush the previous `range`.
          result.push({
            start: prevStart.valueOf(),
            last: prevLast.valueOf(),
            count: mergedCount,
          } as RatioRange);

          // New beginning.
          prevStart = start;
          prevLast = last;
          mergedCount = 1;
        }
      } else {
        // First beginning.
        prevStart = start;
        prevLast = last;
        mergedCount = 1;
      }
    }

    // Last flush.
    if (prevStart && prevLast) {
      result.push({
        start: prevStart.valueOf(),
        last: prevLast.valueOf(),
        count: mergedCount,
      } as RatioRange);
    }

    const beginDateText = `${this.date}T00:00:00`;
    const begin = moment(beginDateText).valueOf();
    this.eventRanges = result.map(x => {
      return {
        start: (x.start - begin) / MILLISECONDS_TO_DAY,
        last: (x.last - begin) / MILLISECONDS_TO_DAY,
        count: x.count,
      };
    })
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

  @Emit()
  contextmenu(event) {
    return event;
  }

  onRefresh() {
    if (!this.currentFragmentMoment) {
      return;
    }
    if (this.skipNextRefresh) {
      this.skipNextRefresh = false;
      return;
    }

    const begin = moment(`${this.date}T00:00:00`);
    const pivotMilliseconds = this.currentFragmentMoment.diff(begin, 'milliseconds');
    const offsetVideoTime = this.video.currentTime - this.currentFragmentVideoTime;
    const offsetMilliseconds = Math.round(offsetVideoTime * ONE_SECOND_TO_MILLISECONDS);
    const currentMilliseconds = pivotMilliseconds + offsetMilliseconds;

    this.cursorPosition = currentMilliseconds / MILLISECONDS_TO_DAY;
    // console.debug(`onRefresh: cursorPosition=${this.cursorPosition},duration=${this.video.duration},totalDuration=${this.totalDuration}`);
  }

  drawBuffered() {
    const seekableEnd = this.getSeekableEnd();
    const r = this.video.buffered;
    if (r) {
      // const pos = this.video.currentTime;
      // let bufferLen = 0;
      // ctx.fillStyle = 'gray';
      // for (let i = 0; i < r.length; i++) {
      //   const start = (r.start(i) / seekableEnd) * canvas.width;
      //   const end = (r.end(i) / seekableEnd) * canvas.width;
      //   ctx.fillRect(start, 2, Math.max(2, end - start), 11);
      //   if (pos >= r.start(i) && pos < r.end(i)) {
      //     // play position is inside this buffer TimeRange,
      //     // retrieve end of buffer position and buffer length
      //     bufferLen = r.end(i) - pos;
      //   }
      // }
    }
  }

  onChangeDate(event: string) {
    this.showDateMenu = false;
    this.updateHlsByDate(event);
  }

  onClickToday() {
    this.date = todayString();
    this.updateHlsByDate(this.date);
  }

  onClickFirst() {
    this.date = this.recordDates[0];
    this.updateHlsByDate(this.date);
  }

  onClickPrevious() {
    const index = this.recordDates.findIndex(x => x === this.date);
    this.date = this.recordDates[index - 1];
    this.updateHlsByDate(this.date);
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
    this.updateHlsByDate(this.date);
  }

  onClickLast() {
    this.date = this.recordDates[this.recordDates.length - 1];
    this.updateHlsByDate(this.date);
  }

  findNearestFragment(time: moment.Moment) {
    if (this.fragments.length === 0) {
      return;
    }

    const cursorValue = time.valueOf();
    let nearestFragment: undefined | Fragment = undefined;
    let nearestDistance: undefined | number = undefined;

    for (let i = 0; i < this.fragments.length; ++i) {
      const f = this.fragments[i];
      if (!f.relurl) {
        throw new EmptyException('Not exists fragment url');
      }
      const start = parseFragmentDateTime(f.relurl);
      const duration = f.duration > 0 ? f.duration : 10;
      const durationMilliseconds = Math.round(duration * ONE_SECOND_TO_MILLISECONDS);
      const last = start.clone().add(durationMilliseconds, 'milliseconds');

      const startValue = start.valueOf();
      const lastValue = last.valueOf();
      // console.debug(`findNearestFragment-> start: ${start.format('LLLL')}`)
      // console.debug(`findNearestFragment-> durationMilliseconds: ${durationMilliseconds}`)
      // console.debug(`findNearestFragment-> last: ${last.format('LLLL')}`)
      console.assert(startValue <= lastValue, `startValue(${startValue}) <= lastValue(${lastValue}), duration(${durationMilliseconds})`);

      let distance;
      if (cursorValue < startValue) {
        distance = startValue - cursorValue;
      } else if (startValue <= cursorValue && cursorValue <= lastValue) {
        return f;  // Excellent correct!
      } else if (lastValue < cursorValue) {
        distance = cursorValue - lastValue;
      } else {
        throw new InaccessibleAreaException();
      }

      if (nearestFragment && typeof nearestDistance !== 'undefined') {
        if (distance < nearestDistance) {
          nearestFragment = f;
          nearestDistance = distance;
        }
      } else {
        // First beginning.
        nearestFragment = f;
        nearestDistance = distance;
      }
    }

    return nearestFragment;
  }

  onClickRecordController(pos: number) {
    console.assert(0 <= pos && pos <= 1);
    const begin = moment(`${this.date}T00:00:00`);
    const offsetMilliseconds = (pos * MILLISECONDS_TO_DAY)
    const cursorTime = begin.clone().add(offsetMilliseconds, 'milliseconds');

    // console.debug(`pos=${pos} -> ${cursorTime.format('LLLL')}`)

    const nearestFragment = this.findNearestFragment(cursorTime);
    if (!nearestFragment) {
      return;
    }
    if (!nearestFragment.relurl) {
      throw new EmptyException('Not exists fragment url');
    }

    console.debug(`Nearest fragment: #${nearestFragment.sn}`);

    const start = parseFragmentDateTime(nearestFragment.relurl);
    const durationMilliseconds = Math.round(nearestFragment.duration * ONE_SECOND_TO_MILLISECONDS);
    const last = start.clone().add(durationMilliseconds, 'milliseconds');
    const startValue = start.valueOf();
    const lastValue = last.valueOf();
    console.assert(startValue <= lastValue);

    const cursorValue = cursorTime.valueOf();
    let currentTime;
    if (cursorValue < startValue) {
      // Start Position
      currentTime = nearestFragment.start;
    } else if (startValue <= cursorValue && cursorValue <= lastValue) {
      // Middle Position
      const diffSeconds = (cursorValue - startValue) / ONE_SECOND_TO_MILLISECONDS;
      console.assert(diffSeconds < nearestFragment.duration);
      currentTime = nearestFragment.start + diffSeconds;
    } else if (lastValue < cursorValue) {
      // Last Position
      currentTime = nearestFragment.start + nearestFragment.duration;
    } else {
      throw new InaccessibleAreaException();
    }

    this.video.currentTime = currentTime;
    this.currentFragmentMoment = start;
    this.currentFragmentVideoTime = currentTime;
    this.skipNextRefresh = true;
    this.cursorPosition = pos;
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
