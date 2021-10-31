<i18n lang="yaml">
en:
  menu:
    setting: "Setting"

ko:
  menu:
    setting: "설정"
</i18n>

<template>
  <view-port class="d-flex flex-column fill-height">
    <div class="d-flex flex-wrap screen-group">
      <media-player
          v-for="n in maxCards"
          :key="`${n}-${loading}`"
          :style="cardStyle(n)"
          hide-controller
          :group="$route.params.group"
          :project="$route.params.project"
          :device="getDeviceUid(n)"
          :loading="loading"
          @contextmenu="onShowContextMenu(n, $event)"
      ></media-player>
    </div>

    <v-footer :height="footerHeight" padless>
      <v-sheet width="100%">
        <v-system-bar :height="footerSystemBarHeight">
          <v-icon>mdi-application</v-icon>
          <v-spacer></v-spacer>
          <v-btn icon small max-width="22px" max-height="22px" @click="onClickCloseFooter">
            <v-icon small class="ma-0">mdi-close</v-icon>
          </v-btn>
        </v-system-bar>

        <v-virtual-scroll
            ref="event-scroll"
            :bench="benched"
            :items="events"
            :height="footerContentHeight"
            :item-height="footerContentItemHeight"
        >
          <template v-slot:default="{ item }">
            <v-list-item dense :key="item">
              <v-list-item-action>
                <v-icon>mdi-cube-scan</v-icon>
              </v-list-item-action>

              <v-list-item-content>
                <div>
                  <span>
                    {{ item.time }}
                  </span>
                  <span>
                    {{ getDeviceName(item.device_uid) }}
                  </span>
                  <v-chip small color="blue">
                    <v-icon left>mdi-identifier</v-icon>
                    {{ item.device_uid }}
                  </v-chip>
                  <v-chip class="ml-2" small>
                    <v-icon left>mdi-label-percent</v-icon>
                    {{ getScorePercentage(item.extra) }}
                  </v-chip>
                </div>
              </v-list-item-content>

              <v-list-item-action>
                <v-icon small>
                  mdi-open-in-new
                </v-icon>
              </v-list-item-action>
            </v-list-item>

            <v-divider></v-divider>
          </template>
        </v-virtual-scroll>

      </v-sheet>
    </v-footer>

    <v-menu
        v-model="showContextMenu"
        :position-x="contextMenuPositionX"
        :position-y="contextMenuPositionY"
        absolute
        offset-y
        z-index="100"
    >
      <v-list dense>
        <v-list-item @click="onClickEdit">
          <v-list-item-title>{{ $t('menu.setting') }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
  </view-port>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';
import MediaPlayer from '@/media/MediaPlayer.vue';
import {VVirtualScroll} from 'vuetify/lib/components/VVirtualScroll';
import type {VmsDeviceA, VmsLayoutA, VmsEventA} from '@/packet/vms';
import moment from 'moment-timezone';

@Component({
  components: {
    MediaPlayer,
    ViewPort,
  }
})
export default class MainVmsLive extends VueBase {
  readonly footerHeight = 200;
  readonly footerSystemBarHeight = 24;
  readonly footerContentHeight = this.footerHeight - this.footerSystemBarHeight;
  readonly footerContentItemHeight = 48;
  readonly benched = 1;
  readonly eventChunkSize = 10;
  readonly eventTotalSize = 100;

  @Ref('event-scroll')
  eventScroll!: VVirtualScroll;

  maxCards = 4;
  showFooter = true;

  showContextMenu = false;
  contextMenuNumber = 0;
  contextMenuPositionX = 0;
  contextMenuPositionY = 0;

  loading = false;

  layouts = [] as Array<VmsLayoutA>;
  devices = [] as Array<VmsDeviceA>;
  layoutToDevice = {};

  latestTime = Date.now();
  events = [] as Array<VmsEventA>;

  created() {
    this.requestSetup();

    // const data = {
    //   time: moment().format(),
    //   event: 1,
    //   device_uid: 1,
    //   file: '',
    //   extra: {score: 0.8},
    //   tag_uid: undefined,
    // } as VmsEventA;
    // this.events.push(data);
    // this.events.push(data);
    // this.events.push(data);
    // this.events.push(data);
    // this.$nextTick(() => {
    //   this.eventScroll.$el.scrollTop = this.eventScroll.$el.scrollHeight;
    // });
  }

  requestSetup() {
    this.loading = true;
    (async () => {
      await this.setup();
    })();
  }

  async setup() {
    try {
      const group = this.$route.params.group;
      const project = this.$route.params.project;
      this.layouts = await this.$api2.getVmsLayouts(group, project);
      this.devices = await this.$api2.getVmsDevices(group, project);

      const layoutToDevice = {};
      for (let i = 0; i < this.maxCards; ++i) {
        const layout = this.layouts.find(l => l.index == i);
        if (typeof layout === 'undefined') {
          continue;
        }
        const device = this.devices.find(d => d.device_uid === layout.device_uid);
        if (typeof device === 'undefined') {
          continue;
        }

        layoutToDevice[i] = device;
      }
      this.layoutToDevice = layoutToDevice;

    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  cardStyle(cardNumber: number) {
    // return {
    //   width: '33.333%',
    //   height: '33.333%',
    // };
    return {
      width: '50%',
      height: '50%',
    };
  }

  getDeviceName(deviceUid: number) {
    const device = this.devices.find(d => d.device_uid === deviceUid);
    if (typeof device === 'undefined') {
      return undefined;
    }
    return device.name;
  }

  getDeviceUid(cardNumber: number) {
    const layoutIndex = cardNumber - 1;
    const device = this.layoutToDevice[layoutIndex] as VmsDeviceA;
    if (typeof device === 'undefined') {
      return undefined;
    }
    return device.device_uid;
  }

  getScorePercentage(extra: any) {
    if (!extra.hasOwnProperty("score")) {
      return undefined;
    }
    return Math.ceil(extra["score"] * 100);
  }

  // onPredict(cardNumber: number, event: Array<object>) {
  //   const layoutIndex = cardNumber - 1;
  //   const device = this.layoutToDevice[layoutIndex] as VmsDeviceA;
  //   if (typeof device === 'undefined') {
  //     return;
  //   }
  //   const deviceUid = device.device_uid;
  //   console.debug(event);
  //
  //   for (const item of event) {
  //     if (this.events.length >= this.eventTotalSize) {
  //       this.events.splice(0, (this.events.length - this.eventTotalSize) + 1);
  //     }
  //     const data = {
  //       time: moment().format(),
  //       event: 1,
  //       device_uid: deviceUid,
  //       file: '',
  //       extra: item,
  //       tag_uid: undefined,
  //     } as VmsEventA;
  //     this.events.push(data);
  //   }
  //
  //   this.$nextTick(() => {
  //     this.eventScroll.$el.scrollTop = this.eventScroll.$el.scrollHeight;
  //   });
  // }

  onShowContextMenu(cardNumber: number, event) {
    event.preventDefault();
    this.showContextMenu = false;
    this.contextMenuNumber = cardNumber;
    this.contextMenuPositionX = event.clientX;
    this.contextMenuPositionY = event.clientY;
    this.$nextTick(() => {
      this.showContextMenu = true;
    })
  }

  onClickEdit() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const index = this.contextMenuNumber;
    // this.moveToMainVmsDevicesEdit(group, project, media);
  }

  onClickCloseFooter() {
    this.showFooter = false;
  }

  onResize() {
    const size = { x: window.innerWidth, y: window.innerHeight };
  }
}
</script>

<style lang="scss" scoped>
.fill-height {
  height: 100%;
}

.screen-group {
  flex: auto;
}

.control-panel {
  width: 100%;
  height: 100%;
}
</style>
