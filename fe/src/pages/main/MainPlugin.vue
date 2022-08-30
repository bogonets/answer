<template>
  <view-port flex>
    <iframe class="plugin-frame" ref="frame" :src="src" @load="onFrameLoad"></iframe>
  </view-port>
</template>

<script lang="ts">
import {Component, Prop, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';
import {ReccCwcCore} from '@recc/api/dist/reccCwcCore';
import {
  ReccCwcDataInit,
  ToastLevel,
  ReccCwcDataToast,
  ReccCwcDataMove,
  ReccCwcDataFullscreen,
  ReccCwcDataRenewalAccessToken,
} from '@recc/api/dist/reccCwc';
import moment from 'moment-timezone';

@Component({
  components: {
    ViewPort,
  },
})
export default class MainPlugin extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly verbose!: boolean;

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
    if (this.verbose) {
      console.debug(`<plugin>.onToast(message=${data.message},detail=${data.detail})`);
    }

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
      case ToastLevel.RequestSuccess:
        this.toastRequestSuccess(data.detail);
        break;
      case ToastLevel.RequestFailure:
        this.toastError(this.$t('toast.request_failure').toString(), data.detail);
        break;
      default:
        throw new Error(`Unknown toast level: ${data.level}`);
    }
  }

  onMove(data: ReccCwcDataMove) {
    if (this.verbose) {
      console.debug(`<plugin>.onMove(name=${data.name},path=${data.path})`);
    }

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
    if (this.verbose) {
      console.debug(
        `<plugin>.onFullscreen(fullscreen=${data.fullscreen},flip=${data.flip})`,
      );
    }

    if (!data.fullscreen && !data.flip) {
      throw new Error('fullscreen or flip argument must be provided');
    }
    if (data.fullscreen && data.flip) {
      throw new Error('fullscreen and flip arguments cannot coexist');
    }
  }

  onRefreshTokenError() {
    if (this.verbose) {
      console.debug('<plugin>.onRefreshTokenError()');
    }

    if (this.$api2.onRefreshTokenError) {
      this.$api2.onRefreshTokenError();
    }
  }

  onRenewalAccessToken(data: ReccCwcDataRenewalAccessToken) {
    if (this.verbose) {
      console.debug('<plugin>.onRenewalAccessToken(...)');
    }

    this.$api2.setAccessToken(data.accessToken);
    if (this.$api2.onRenewalAccessToken) {
      this.$api2.onRenewalAccessToken(data.accessToken);
    }
  }

  onUninitializedService() {
    if (this.verbose) {
      console.debug('<plugin>.onUninitializedService()');
    }

    if (this.$api2.onUninitializedService) {
      this.$api2.onUninitializedService();
    }
  }

  /**
   * Do not call from `mounted()` callback method.
   * `frame.contentWindow` may not be complete.
   */
  onFrameLoad() {
    if (!this.frame.contentWindow) {
      throw new Error('<iframe>.contentWindow not exist');
    }

    const apiOptions = this.$api2.asPortableOptions();
    const dark = this.$vuetify.theme.dark ? 1 : 0;
    const lang = this.$vuetify.lang.current;
    const timezone = moment.tz.guess();
    const group = this.$route.params.group;
    const project = this.$route.params.project;

    this.cwc = new ReccCwcCore(this.frame, {
      origin: window.origin,
      initData: {
        apiOptions,
        dark,
        lang,
        timezone,
        group,
        project,
      } as ReccCwcDataInit,
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
