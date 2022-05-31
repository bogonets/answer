<template>
  <view-port>
    <iframe
      class="plugin-frame"
      ref="plugin-frame"
      :src="src"
      @load="onFrameLoad"
    ></iframe>
  </view-port>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';

@Component({
  components: {
    ViewPort,
  },
})
export default class MainPlugin extends VueBase {
  @Ref('plugin-frame')
  readonly pluginFrame!: HTMLIFrameElement;

  src!: string;

  created() {
    const plugin = this.$route.params.plugin;
    const menu = this.$route.params.menu;
    this.src = `${window.origin}/plugins/${plugin}/${menu}`;
  }

  onFrameLoad() {
    console.debug(`iframe onload => ${this.src}`);
  }
}
</script>

<style lang="scss" scoped>
@mixin fill-size {
  width: 100%;
  height: 100%;
}

.plugin-frame {
  @include fill-size;

  border: 0;
}
</style>
