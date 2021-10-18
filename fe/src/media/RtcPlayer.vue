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
import type {RtcOfferQ} from '@/packet/vms';

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

  @Prop({type: String})
  readonly group!: string;

  @Prop({type: String})
  readonly project!: string;

  @Prop({type: Number})
  readonly device!: number;

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

      const group = this.group;
      const project = this.project;
      const device = this.device.toString();
      const body = {
        type: pc.localDescription?.type || '',
        sdp: pc.localDescription?.sdp || '',
      } as RtcOfferQ;
      const answer = await this.$api2.postVmsDeviceRtcIce(group, project, device, body);
      const answerInit = {
        type: answer.type,
        sdp: answer.sdp,
      } as RTCSessionDescriptionInit;
      await pc.setRemoteDescription(answerInit);

      this.pc = pc;
    } catch (error) {
      this.toastError(error);
    }
  }

  onTrack(event: RTCTrackEvent) {
    if (event.track.kind == 'video') {
      this.video.srcObject = event.streams[0];
    } else if (event.track.kind == 'audio') {
      // this.audio.srcObject = event.streams[0];
    }
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
