<template>
  <div :style="hlsPlayerStyle">
    <video
        ref="hls-video"
        autoplay
        muted
        playsinline
        preload="auto"
        @pause="onPause"
        @play="onPlay"
        @resize="onResize"
    ></video>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Ref, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {UnsupportedException} from '@/exceptions';
import Hls from 'hls.js';
import type {HlsConfig} from 'hls.js';

@Component
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

  @Ref('hls-video')
  hlsVideo!: HTMLVideoElement;

  hls?: Hls;

  paused = true;
  videoWidth = 0;
  videoHeight = 0;

  mounted() {
    this.updateHls(this.src, this.options);
  }

  beforeDestroy() {
    this.close();
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
      hls.attachMedia(this.hlsVideo);
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

  onPause() {
    this.paused = true;
  }

  onPlay() {
    this.paused = false;
  }

  onResize() {
    this.videoWidth = this.hlsVideo.videoWidth;
    this.videoHeight = this.hlsVideo.videoHeight;
  }

}
</script>
