<i18n lang="yaml">
en:
  hints:
    logo_alt: "Answer"
  tooltips:
    latest_event_time: "Latest event time: {0}"

ko:
  hints:
    logo_alt: "Answer"
  tooltips:
    latest_event_time: "마지막 이벤트 발생 시간: {0}"
</i18n>

<template>
  <v-hover v-slot="{ hover }">
    <div
        class="hls-player"
        @contextmenu="contextmenu"
        :style="hlsPlayerStyle"
    >
      <v-sheet
          v-if="showInformationPanel && online"
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
            v-show="online"
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

      <div v-show="!online" class="brand-logo-container">
        <img
            class="brand-logo"
            src="@/assets/logo/answer-logo-notext.svg"
            :alt="$t('hints.logo_alt')"
        />
      </div>
    </div>
  </v-hover>
</template>

<script lang="ts">
import {Component, Emit, Prop, Ref, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import RecordController from '@/media/RecordController.vue';
import {UnsupportedException} from '@/exceptions';
import colors from 'vuetify/lib/util/colors'
import Hls from 'hls.js';
import type {HlsConfig} from 'hls.js';
import {
  VMS_CHANNEL_META_CODE_BAD_ARGUMENT,
  VMS_CHANNEL_META_CODE_FILTERED,
  VMS_CHANNEL_META_CODE_NOT_READY_ROI,
  VMS_CHANNEL_META_CODE_OPENED,
  VMS_CHANNEL_META_CODE_SUCCESS
} from '@/packet/vms';

@Component({
  components: {
    RecordController,
  },
})
export default class HlsPlayer extends VueBase {
  @Prop({type: String, default: ''})
  readonly src!: string;

  @Prop({type: Object, default: () => new Object()})
  readonly options!: HlsConfig;

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

  @Prop({type: Boolean, default: false})
  readonly online!: boolean;

  @Prop({type: Number, default: 1000})
  readonly refreshMilliseconds!: number;

  @Ref('video')
  readonly video!: HTMLVideoElement;

  hls?: Hls;

  paused = true;
  videoWidth = 0;
  videoHeight = 0;

  showInformationPanel = true;
  informationCode = VMS_CHANNEL_META_CODE_SUCCESS;
  informationText = '';
  informationDate = '';

  bufferIntervalHandle = -1;

  mounted() {
    this.updateHls(this.src, this.options);

    this.bufferIntervalHandle = window.setInterval(() => {
      this.onBufferInterval();
    }, this.refreshMilliseconds);

  }

  beforeDestroy() {
    if (this.bufferIntervalHandle != -1) {
      window.clearInterval(this.bufferIntervalHandle);
    }

    this.close();
  }

  onBufferInterval() {
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

  @Watch('src')
  watchSrc(newVal: string) {
    this.updateHls(newVal, this.options);
  }

  @Watch('options')
  watchOptions(newVal: HlsConfig) {
    this.updateHls(this.src, newVal);
  }

  updateHls(src: string, options: HlsConfig) {
    if (!Hls.isSupported()) {
      this.hls = undefined;
      throw new UnsupportedException('Unsupported HLS.js component');
    }

    try {
      const hls = new Hls(options);
      hls.loadSource(src);
      hls.attachMedia(this.video);
      this.hls = hls;
    } catch (error) {
      this.hls = undefined;
      console.error(error);
    }
  }

  close() {
    if (this.hls) {
      this.hls.destroy();
      this.hls = undefined;
    }
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

  @Emit()
  contextmenu(event) {
    return event;
  }

  play() {
    this.video.play();
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
</style>
