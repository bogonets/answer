<template>
  <view-port>
    <iframe class="plugin-frame" ref="frame" :src="src" @load="onFrameLoad"></iframe>
  </view-port>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';
import {ReccCwcCore} from '@recc/api/dist/reccCwcCore';
import {
  ReccCwcDataFullscreen,
  ReccCwcDataMove,
  ReccCwcDataRenewalAccessToken,
  ReccCwcDataToast,
  ToastLevel,
} from '@recc/api/dist/reccCwc';

@Component({
  components: {
    ViewPort,
  },
})
export default class MainPlugin extends VueBase {
  @Ref('frame')
  frame!: HTMLIFrameElement;

  cwc?: ReccCwcCore = undefined;

  get src() {
    const plugin = this.$route.params.plugin;
    const menu = this.$route.params.menu;
    const path = this.$route.params.path;
    if (path) {
      const decodedPath = decodeURI(path);
      const suffix = decodedPath[0] === '/' ? decodedPath.slice(1) : decodedPath;
      return `/plugins/${plugin}/${suffix}`;
    } else {
      return `/plugins/${plugin}/${menu}`;
    }
  }

  beforeDestroy() {
    if (this.cwc) {
      this.cwc.unregister();
      this.cwc = undefined;
    }
  }

  onToast(data: ReccCwcDataToast) {
    console.debug(`<plugin>.onToast(message=${data.message},detail=${data.detail})`);
    switch (data.level) {
      case ToastLevel.Success:
        this.toastSuccess(data.message, data.detail);
        break;
      case ToastLevel.Info:
        this.toastInfo(data.message, data.detail);
        break;
      case ToastLevel.Warning:
        this.toastWarning(data.message, data.detail);
        break;
      case ToastLevel.Error:
        this.toastError(data.message, data.detail);
        break;
      default:
        throw new Error(`Unknown toast level: ${data.level}`);
    }
  }

  onMove(data: ReccCwcDataMove) {
    console.debug(`<plugin>.onMove(name=${data.name},path=${data.path})`);
    if (!data.name && !data.path) {
      throw new Error('name or path argument must be provided');
    }
    if (data.name && data.path) {
      throw new Error('name and path arguments cannot coexist');
    }

    if (data.name) {
      this.moveTo(data.name, {...data.params});
    } else if (data.path) {
      throw new Error('Unsupported operation');
    }
  }

  onFullscreen(data: ReccCwcDataFullscreen) {
    console.debug(
      `<plugin>.onFullscreen(fullscreen=${data.fullscreen},flip=${data.flip})`,
    );
    if (!data.fullscreen && !data.flip) {
      throw new Error('fullscreen or flip argument must be provided');
    }
    if (data.fullscreen && data.flip) {
      throw new Error('fullscreen and flip arguments cannot coexist');
    }
  }

  onRefreshTokenError() {
    console.debug('<plugin>.onRefreshTokenError()');
    if (this.$api2.onRefreshTokenError) {
      this.$api2.onRefreshTokenError();
    }
  }

  onRenewalAccessToken(data: ReccCwcDataRenewalAccessToken) {
    console.debug('<plugin>.onRenewalAccessToken(...)');
    this.$api2.setAccessToken(data.accessToken);
    if (this.$api2.onRenewalAccessToken) {
      this.$api2.onRenewalAccessToken(data.accessToken);
    }
  }

  onUninitializedService() {
    console.debug('<plugin>.onUninitializedService()');
    if (this.$api2.onUninitializedService) {
      this.$api2.onUninitializedService();
    }
  }

  onFrameLoad() {
    if (!this.frame.contentWindow) {
      throw new Error('<iframe>.contentWindow not exist');
    }

    this.cwc = new ReccCwcCore(this.frame, {
      origin: window.origin,
      onToast: data => {
        this.onToast(data);
      },
      onMove: data => {
        this.onMove(data);
      },
      onFullscreen: data => {
        this.onFullscreen(data);
      },
      onRefreshTokenError: () => {
        this.onRefreshTokenError();
      },
      onRenewalAccessToken: data => {
        this.onRenewalAccessToken(data);
      },
      onUninitializedService: () => {
        this.onUninitializedService();
      },
    });

    this.cwc.postInit(
      this.$api2.asPortableOptions(),
      this.$localStore.dark,
      this.$localStore.lang,
    );
  }
}
</script>

<style lang="scss" scoped>
.plugin-frame {
  width: 100%;
  height: 100%;
  border: 0;
}
</style>
