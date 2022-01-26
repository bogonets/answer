<template>
  <div :style="hlsPlayerStyle">
    <video ref="video"></video>
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

  @Ref()
  video!: HTMLVideoElement;

  hls?: Hls;

  mounted() {
    this.updateHls(this.src, this.options);
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
    // if (!this.disableAspectRatio && this.videoWidth && this.videoHeight) {
    //   style += `aspect-ratio: ${this.videoWidth}/${this.videoHeight};`;
    // }
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
}
</script>
