<template>
  <v-sheet class="media-player">
    <v-system-bar absolute lights-out>
      <v-icon small color="red">mdi-record</v-icon>
      {{ `CCTV ${options.index}` }}
      <v-spacer></v-spacer>
      <v-icon>mdi-video-4k-box</v-icon>
      <v-icon>mdi-video-off</v-icon>
      <v-icon>mdi-volume-off</v-icon>
      <v-icon>mdi-signal-cellular-outline</v-icon>
    </v-system-bar>
    <v-img src="@/assets/logo/answer-logo-notext.svg" max-width="200px" max-height="200px" contain></v-img>
  </v-sheet>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

interface MediaPlayerOptions {
  index: number;
}

function createEmptyMediaPlayerOptions() {
  return {
    index: -1,
  } as MediaPlayerOptions;
}

@Component
export default class MediaPlayer extends VueBase {
  @Prop({type: Object, default: createEmptyMediaPlayerOptions})
  readonly options!: MediaPlayerOptions;
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
}
</style>
