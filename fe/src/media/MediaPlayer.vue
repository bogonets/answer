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

      <v-img
          v-if="disconnected"
          src="@/assets/logo/answer-logo-notext.svg"
          min-width="80px"
          max-width="200px"
          min-height="80px"
          max-height="200px"
          contain
      ></v-img>
      <rtc-player
          v-else
      ></rtc-player>

    </v-card>
  </v-hover>
</template>

<script lang="ts">
import {Component, Prop, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import RtcPlayer from '@/media/RtcPlayer.vue';

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

@Component({
  components: {
    RtcPlayer,
  },
})
export default class MediaPlayer extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly hideSystemBar!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hoverSystemBar!: boolean;

  @Prop({type: Number, default: UNKNOWN_ID})
  readonly index!: number;

  @Prop({type: Object, default: createEmptyMediaPlayerOptions})
  readonly options!: MediaPlayerOptions;

  recoding = false;
  name = '';
  enableVideo = false;
  enableAudio = false;
  signalLevel = 0;

  disconnected = true;
  status = {} as MediaPlayerStatus;

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
}
</style>
