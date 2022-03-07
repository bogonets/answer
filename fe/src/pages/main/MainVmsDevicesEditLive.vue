<template>
  <media-player
      :value="item"
      :group="$route.params.group"
      :project="$route.params.project"
      :device="$route.params.device"
  ></media-player>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MediaPlayer from '@/media/MediaPlayer.vue';
import type {VmsDeviceA} from '@/packet/vms';

@Component({
  components: {
    MediaPlayer,
  }
})
export default class MainVmsDevicesEditLive extends VueBase {
  item = {} as VmsDeviceA;

  created() {
    this.setup();
  }

  setup() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.$api2.getVmsDevice(group, project, device)
        .then(item => {
          this.item = item;
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }
}
</script>
