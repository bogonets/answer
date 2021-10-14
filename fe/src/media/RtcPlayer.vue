<template>
  <video
      class="video-player"
      ref="video"
      autoplay
      muted
      playsinline
      preload="auto"
  ></video>
</template>

<script lang="ts">
import {Component, Prop, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

const DEFAULT_STUN_SERVER_01 = 'stun:stun.l.google.com:19302';
const DEFAULT_ICE_SERVERS = [
    { urls: [DEFAULT_STUN_SERVER_01] }
] as Array<RTCIceServer>;

@Component
export default class RtcPlayer extends VueBase {
  readonly defaultRtcConfig = {
    sdpSemantics: 'unified-plan',
  } as RTCConfiguration;

  readonly defaultTransceiverInit = {
    direction: 'recvonly'
  } as RTCRtpTransceiverInit;

  @Prop({type: Object})
  readonly config!: RTCConfiguration;

  @Ref('video')
  video!: HTMLVideoElement;

  pc?: RTCPeerConnection = undefined;

  created() {
    (async () => {
      const config = this.config ?? this.defaultRtcConfig;
      const transceiverInit = this.defaultTransceiverInit;
      await this.doNegotiate(config, transceiverInit, this.onTrack);
    })();
  }

  beforeDestroy() {
    this.close();
  }

  async doNegotiate(
      config: RTCConfiguration,
      transceiverInit: RTCRtpTransceiverInit,
      trackCallback: (event: RTCTrackEvent) => void,
  ) {
    try {
      const pc = new RTCPeerConnection(config);
      pc.addEventListener('track', trackCallback);
      pc.addTransceiver('video', transceiverInit);

      // if (this.audio_object) {
      //   this.pc.addTransceiver('audio', {direction: 'recvonly'});
      // }

      // if (this.meta_object) {
      //   this.pc.addTransceiver('meta', {direction: 'recvonly'});
      // }

      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);
      await this.waitToCompleteIceGathering(pc);

      // const type = pc.localDescription.type;
      // const sdp = pc.localDescription.sdp;
      // const answer = await this.$api2.postVmsOffer(pc.localDescription);
      // this.pc.setRemoteDescription(answer);

      this.pc = pc;
    } catch (error) {
      this.toastError(error);
    }
  }

  onTrack(event: RTCTrackEvent) {
    //   this.print_debug('on_track()');
    //   if (event.track.kind == 'video') {
    //     this.video_object.srcObject = event.streams[0];
    //   } else if (event.track.kind == 'audio') {
    //     this.audio_object.srcObject = event.streams[0];
    //   }
  }

  waitToCompleteIceGathering(pc: RTCPeerConnection) {
    return new Promise(resolve => {
      if (pc.iceGatheringState === 'complete') {
        return resolve();
      }

      const stateChangeCallback = () => {
        if (pc.iceGatheringState === 'complete') {
          pc.removeEventListener('icegatheringstatechange', stateChangeCallback);
          return resolve();
        } else if (pc.iceGatheringState === 'gathering') {
          // EMPTY.
        } else if (pc.iceGatheringState === 'new') {
          // EMPTY.
        } else {
          console.assert(false, "Inaccessible section");
        }
      };

      pc.addEventListener('icegatheringstatechange', stateChangeCallback);
    });
  }

  play() {
    this.video.play();
  }

  pause() {
    this.video.pause();
  }

  close() {
    if (this.pc) {
      this.pc.close();
      this.pc = undefined;
    } else {
      console.assert(typeof this.pc === 'undefined');
    }
  }
}
</script>

<style lang="scss" scoped>
.video-player {
  width: 100%;
  height: 100%;
  object-fit: fill;
}
</style>
