<template>
  <hls-player
      :group="$route.params.group"
      :project="$route.params.project"
      :device="$route.params.device"
  ></hls-player>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import HlsPlayer from '@/media/HlsPlayer.vue';

@Component({
  components: {
    HlsPlayer,
  }
})
export default class MainVmsDevicesEditRecord extends VueBase {
}
</script>
