<i18n lang="yaml">
en:
  unknown: "Unknown Media"
  disconnected: "Disconnected"

ko:
  unknown: "알 수 없는 미디어"
  disconnected: "연결이 끊어졌습니다"
</i18n>

<template>
  <v-hover v-slot="{ hover }">
    <v-card
        outlined
        tile
        class="media-player"
        @contextmenu="contextmenu"
    >
      <v-system-bar
          class="status-bar"
          v-if="!hideSystemBar"
          v-show="showSystemBar(hover)"
          absolute
          lights-out
      >
        <v-icon v-if="recoding" color="red">mdi-record</v-icon>
        <span>{{ displayName }}</span>
        <v-spacer></v-spacer>
        <v-icon v-if="video4K">mdi-video-4k-box</v-icon>
        <v-icon v-if="enableVideo">mdi-video-off</v-icon>
        <v-icon v-if="enableAudio">mdi-volume-off</v-icon>
        <v-icon>{{ signalIcon }}</v-icon>
      </v-system-bar>

      <canvas
          v-show="!hideCanvasUser"
          class="canvas-user"
          ref="canvas-user"
          :width="canvasWidth"
          :height="canvasHeight"
      ></canvas>
      <canvas
          v-show="!hideCanvasMeta"
          class="canvas-meta"
          ref="canvas-meta"
          :width="canvasWidth"
          :height="canvasHeight"
      ></canvas>

      <v-img
          class="brand-logo"
          v-if="disconnected"
          src="@/assets/logo/answer-logo-notext.svg"
          min-width="80px"
          max-width="200px"
          min-height="80px"
          max-height="200px"
          contain
      ></v-img>
      <rtc-player
          class="rtc-player"
          ref="rtc-player"
          v-else
      ></rtc-player>

      <div
          class="controller"
          v-if="!disconnected"
          v-show="!hideController"
      >
        <v-btn icon>
          <v-icon>mdi-play</v-icon>
        </v-btn>
        <v-progress-linear></v-progress-linear>
        <v-btn icon>
          <v-icon>mdi-dots-horizontal</v-icon>
        </v-btn>
      </div>

    </v-card>
  </v-hover>
</template>

<script lang="ts">
import {Component, Prop, Ref, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import RtcPlayer from '@/media/RtcPlayer.vue';
import * as Pixi from 'pixi.js';

interface MediaPlayerOptions {
  index: number;
}

interface MediaPlayerStatus {
  name?: string;

  mediaRecoding?: boolean;

  videoWidth?: number;
  videoHeight?: number;

  enableVideo?: boolean;
  enableAudio?: boolean;

  volumeLevel?: number;
}

function createEmptyMediaPlayerOptions() {
  return {
    index: -1,
  } as MediaPlayerOptions;
}

const UNKNOWN_ID = -1;
const DEFAULT_CANVAS_WIDTH = 1024;
const DEFAULT_CANVAS_HEIGHT = 1024;

@Component({
  components: {
    RtcPlayer,
  },
})
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

  @Prop({type: Number, default: DEFAULT_CANVAS_WIDTH})
  readonly canvasWidth!: number;

  @Prop({type: Number, default: DEFAULT_CANVAS_HEIGHT})
  readonly canvasHeight!: number;

  @Prop({type: Number, default: UNKNOWN_ID})
  readonly index!: number;

  @Prop({type: Object, default: createEmptyMediaPlayerOptions})
  readonly options!: MediaPlayerOptions;

  @Ref('canvas-user')
  readonly canvasUser!: HTMLCanvasElement;

  @Ref('canvas-meta')
  readonly canvasMeta!: HTMLCanvasElement;

  @Ref('rtc-player')
  readonly rtcPlayer!: RtcPlayer;

  recoding = false;
  name = '';
  enableVideo = false;
  enableAudio = false;
  signalLevel = 0;

  disconnected = false;
  status = {} as MediaPlayerStatus;

  pixiUser?: Pixi.Application = undefined;
  pixiMeta?: Pixi.Application = undefined;

  mounted() {
    this.createPixi();

    if (this.pixiUser) {
      let graphics = new Pixi.Graphics()
      graphics.lineStyle(8, 0x000000)

      //start
      graphics.moveTo(300, 250)
      //end
      graphics.lineTo(500, 250)
      this.pixiUser.stage.addChild(graphics)
    }
  }

  beforeDestroy() {
    this.destroyPixi();
  }

  createPixi() {
    if (this.pixiUser) {
      this.pixiUser.destroy();
    }
    if (this.pixiMeta) {
      this.pixiMeta.destroy();
    }

    const defaultOptions = {
      width: this.canvasWidth,
      height: this.canvasHeight,
      antialias: true,
      transparent: true,
    } as Pixi.IApplicationOptions;

    this.pixiUser = new Pixi.Application({
      ...defaultOptions,
      view: this.canvasUser,
    } as Pixi.IApplicationOptions);
    this.pixiMeta = new Pixi.Application({
      ...defaultOptions,
      view: this.canvasMeta,
    } as Pixi.IApplicationOptions);
  }

  destroyPixi() {
    if (this.pixiUser) {
      this.pixiUser.destroy();
      this.pixiUser = undefined;
    }
    if (this.pixiMeta) {
      this.pixiMeta.destroy();
      this.pixiMeta = undefined;
    }
  }

  showSystemBar(hover) {
    if (this.hoverSystemBar) {
      return !!hover;
    }
    return true;
  }

  get displayName() {
    if (this.disconnected) {
      return this.$t('disconnected').toString();
    }

    let result = '';
    if (this.index !== UNKNOWN_ID) {
      result += this.index.toString();
    }
    if (this.name) {
      result += this.name;
    }

    if (result) {
      return result;
    } else {
      return this.$t('unknown').toString();
    }
  }

  get video4K() {
    return false;
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

  @Watch('options')
  onWatchOptions(newVal: MediaPlayerOptions, oldVal: MediaPlayerOptions) {
  }

  @Watch('status')
  onWatchStatus(newVal: MediaPlayerStatus, oldVal: MediaPlayerStatus) {
    this.disconnected = newVal.mediaRecoding || false;
    this.name = newVal.name || '';
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
  height: 100%;

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
}
</style>
