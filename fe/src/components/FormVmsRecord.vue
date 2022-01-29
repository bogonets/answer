<i18n lang="yaml">
en:
  submit: "Submit"

ko:
  submit: "제출"
</i18n>

<template>
  <div>
    <hls-player
        :src="hlsUrl"
        :options="hlsOptions"
        :group="$route.params.group"
        :project="$route.params.project"
        :device="$route.params.device"
    ></hls-player>
  </div>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import HlsPlayer from '@/media/HlsPlayer.vue';

@Component({
  components: {
    HlsPlayer,
  }
})
export default class FormVmsRecord extends VueBase {
  @Prop({type: String, default: ''})
  readonly group!: string;

  @Prop({type: String, default: ''})
  readonly project!: string;

  @Prop({type: [String, Number]})
  readonly device?: string | number;

  hlsUrl = "";
  hlsOptions = {};

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

  mounted() {
    this.hlsUrl = this.$api2.urlVmsRecords(this.group, this.project, this.deviceText);
    this.hlsOptions = {
      xhrSetup: (xhr: XMLHttpRequest, url: string) => {
        const bearer_token = `Bearer ${this.$localStore.access}`;
        xhr.setRequestHeader('Authorization', bearer_token);
      },
    }
  }
}
</script>

<style lang="scss" scoped>
.category-z-index {
  // The z-index for the v-select-list displayed at the top of the `MediaPlayer`.
  // Media players use a z-index between 0 and 100.
  z-index: 100;
}
</style>
