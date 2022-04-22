<i18n lang="yaml">
en:
  menu:
    events: 'Events'
    setting: 'Setting'
  msg:
    new_events: '{0} events have been added.'
  unknown_device: '[Unknown Device]'
  no_name_device: '[No name Device]'
  close: 'Close'

ko:
  menu:
    events: '이벤트'
    setting: '설정'
  msg:
    new_events: '{0}개의 이벤트가 추가되었습니다.'
  unknown_device: '[알 수 없는 장치]'
  no_name_device: '[이름 없는 장치]'
  close: '닫기'
</i18n>

<template>
  <div>
    <v-navigation-drawer
      right
      app
      clipped
      permanent
      stateless
      touchless
      :mini-variant.sync="mini"
    >
      <v-list nav dense>
        <v-list-item link @click.stop="onClickFoldNavigation">
          <v-list-item-icon>
            <v-icon>mdi-star</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('menu.events') }}
          </v-list-item-title>
          <v-btn icon @click.stop="onClickFoldNavigation">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-list-item>
        <v-divider></v-divider>

        <div ref="events-scroll-placeholder"></div>
        <v-virtual-scroll
          v-resize="onResize"
          :bench="benched"
          :items="events"
          :height="eventsHeight"
          :item-height="itemHeight"
        >
          <template v-slot:default="{item}">
            <v-list-item class="ma-0" :key="item.event_uid">
              <div class="event-reference">
                <vms-snapshot
                  thumbnail
                  v-ripple
                  :group="$route.params.group"
                  :project="$route.params.project"
                  :event="item.event_uid"
                  :width="imageWidth"
                  :height="imageHeight"
                ></vms-snapshot>
              </div>

              <div class="event-title">
                <div>
                  <v-icon>{{ eventCategoryIcon(item) }}</v-icon>
                  <span class="text-caption text--secondary text-no-wrap">
                    {{ eventDeviceName(item.device_uid) }}
                  </span>
                </div>
                <div>
                  <span class="text-caption text--secondary text-no-wrap">
                    {{ eventDateTime(item) }}
                  </span>
                </div>
              </div>
            </v-list-item>
            <v-divider></v-divider>
          </template>
        </v-virtual-scroll>
      </v-list>
    </v-navigation-drawer>

    <view-port class="d-flex flex-column fill-height">
      <div class="d-flex flex-wrap screen-group">
        <media-player
          v-for="n in maxCards"
          :key="`${n}-${loading}`"
          :style="cardStyle(n)"
          :group="$route.params.group"
          :project="$route.params.project"
          :device="getDeviceUid(n)"
          :loading="loading"
          :value="getDevice(n)"
          @contextmenu="onShowContextMenu(n, $event)"
        ></media-player>
      </div>

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
  </div>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';
import MediaPlayer from '@/media/MediaPlayer.vue';
import VmsSnapshot from '@/components/VmsSnapshot.vue';
import {VVirtualScroll} from 'vuetify/lib/components/VVirtualScroll';
import type {
  VmsDeviceA,
  VmsLayoutA,
  VmsEventA,
  VmsNewsEventQ,
  VmsLatestEventQ,
} from '@/packet/vms';
import {
  EVENT_CATEGORY_ID_COLOR,
  EVENT_CATEGORY_ID_DETECTION,
  EVENT_CATEGORY_ID_MATCHING,
  EVENT_CATEGORY_ID_OCR,
  USER_CONFIG_REFRESH_INTERVAL,
  USER_CONFIG_POPUP,
  USER_CONFIG_BEEP,
  USER_CONFIG_BEEP_INTERVAL,
  USER_CONFIG_BEEP_DURATION,
} from '@/packet/vms';
import {iso8601ToLocalDateTime} from '@/chrono/iso8601';
import moment from 'moment-timezone';

const EVENT_BOTTOM_MARGIN = 8;

@Component({
  components: {
    MediaPlayer,
    ViewPort,
    VmsSnapshot,
  },
})
export default class MainVmsLive extends VueBase {
  readonly benched = 1;
  readonly itemHeight = 64 + 4 + 4; // content height + margin top + margin bottom;
  readonly eventTotalSize = 30;

  readonly imageWidth = 64;
  readonly imageHeight = 64;

  @Ref('event-scroll')
  readonly eventScroll!: VVirtualScroll;

  @Ref('events-scroll-placeholder')
  readonly eventsScrollPlaceholder!: HTMLDivElement;

  mini = false;
  eventsHeight = 100;

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
  lastEventTime = moment().tz(moment.tz.guess()).format();

  intervalHandle = -1;

  vmsRefreshInterval = USER_CONFIG_REFRESH_INTERVAL;
  vmsPopup = USER_CONFIG_POPUP;
  vmsBeep = USER_CONFIG_BEEP;
  vmsBeepInterval = USER_CONFIG_BEEP_INTERVAL;
  vmsBeepDuration = USER_CONFIG_BEEP_DURATION;

  beepPlaying = false;
  beepCounter = 0;
  beepIntervalHandle = -1;

  created() {
    const extra = this.$localStore.userExtra;
    this.vmsRefreshInterval = extra.vmsRefreshInterval || USER_CONFIG_REFRESH_INTERVAL;
    this.vmsPopup = extra.vmsPopup || USER_CONFIG_POPUP;
    this.vmsBeep = extra.vmsBeep || USER_CONFIG_BEEP;
    this.vmsBeepInterval = extra.vmsBeepInterval || USER_CONFIG_BEEP_INTERVAL;
    this.vmsBeepDuration = extra.vmsBeepDuration || USER_CONFIG_BEEP_DURATION;
    this.requestSetup();
  }

  beforeDestroy() {
    if (this.intervalHandle != -1) {
      window.clearInterval(this.intervalHandle);
    }
    if (this.beepIntervalHandle != -1) {
      window.clearInterval(this.beepIntervalHandle);
    }
  }

  playAlertSound() {
    const audio = new Audio(require('@/assets/sfx/beep01.wav'));
    audio.play();
  }

  doBeep() {
    if (!this.vmsBeep) {
      return;
    }

    if (this.beepPlaying) {
      return;
    }

    if (this.vmsBeepDuration <= 0) {
      // TODO: If it is 0, it must be turned off manually.
      throw Error('Beep Duration is 0. Not Implementation');
    }

    if (this.vmsBeepInterval <= 0) {
      throw Error('Beep Interval is 0.');
    }

    this.beepPlaying = true;
    this.beepCounter = Math.ceil(this.vmsBeepDuration / this.vmsBeepInterval);
    this.playAlertSound();
    this.beepCounter--;
    console.debug(`Current beep count: ${this.beepCounter}`);

    this.beepIntervalHandle = window.setInterval(() => {
      console.debug(`Current beep count: ${this.beepCounter}`);
      if (this.beepCounter > 0) {
        this.beepCounter--;
        this.playAlertSound();
      } else {
        this.beepCounter = 0;
        this.beepPlaying = false;
        window.clearInterval(this.beepIntervalHandle);
      }
    }, this.vmsBeepInterval * 1000);
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

      const body = {
        max: this.eventTotalSize,
      } as VmsLatestEventQ;
      this.$api2
        .postVmsEventsLatest(group, project, body)
        .then(items => {
          this.events = items;
          if (items.length >= 1) {
            this.lastEventTime = items[0].time;
          } else {
            this.lastEventTime = moment().tz(moment.tz.guess()).format();
          }
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });

      this.intervalHandle = window.setInterval(() => {
        this.requestEvents();
      }, this.vmsRefreshInterval * 1000);
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  requestEvents() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const body = {
      time: this.lastEventTime,
      max: this.eventTotalSize,
    } as VmsNewsEventQ;
    this.$api2
      .postVmsEventsNews(group, project, body)
      .then(items => {
        if (items.length >= 1) {
          this.lastEventTime = items[0].time;
          this.events = [...items, ...this.events];
          if (this.events.length > this.eventTotalSize) {
            this.events.splice(this.eventTotalSize);
          }
          if (this.vmsPopup) {
            this.toastInfo(this.$t('msg.new_events', [items.length]));
          }
          this.doBeep();
        }
      })
      .catch(error => {
        // this.toastRequestFailure(error);
      });
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

  getDevice(cardNumber: number) {
    const layoutIndex = cardNumber - 1;
    return this.layoutToDevice[layoutIndex] as VmsDeviceA;
  }

  getDeviceUid(cardNumber: number) {
    const layoutIndex = cardNumber - 1;
    const device = this.layoutToDevice[layoutIndex] as VmsDeviceA;
    if (typeof device === 'undefined') {
      return undefined;
    }
    return device.device_uid;
  }

  eventDeviceName(value: number) {
    const findDevice = this.devices.find(i => i.device_uid == value);
    if (typeof findDevice === 'undefined') {
      return '';
    }
    return findDevice.name;
  }

  eventCategoryIcon(item: VmsEventA) {
    switch (item.category_id) {
      case EVENT_CATEGORY_ID_COLOR:
        return 'mdi-palette';
      case EVENT_CATEGORY_ID_DETECTION:
        return 'mdi-image-search';
      case EVENT_CATEGORY_ID_MATCHING:
        return 'mdi-compare';
      case EVENT_CATEGORY_ID_OCR:
        return 'mdi-ocr';
      default:
        return 'mdi-help';
    }
  }

  eventDateTime(item: VmsEventA) {
    return iso8601ToLocalDateTime(item.time);
  }

  onShowContextMenu(cardNumber: number, event) {
    event.preventDefault();
    this.showContextMenu = false;
    this.contextMenuNumber = cardNumber;
    this.contextMenuPositionX = event.clientX;
    this.contextMenuPositionY = event.clientY;
    this.$nextTick(() => {
      this.showContextMenu = true;
    });
  }

  onClickEdit() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const cardNumber = this.contextMenuNumber;
    const uid = this.getDeviceUid(cardNumber);
    if (typeof uid === 'undefined') {
      return;
    }
    this.moveToMainVmsDevicesEditInfo(group, project, uid.toString());
  }

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  onResize() {
    const size = {x: window.innerWidth, y: window.innerHeight};
    const rect = this.eventsScrollPlaceholder.getBoundingClientRect();
    this.eventsHeight = Math.abs(size.y - rect.y - EVENT_BOTTOM_MARGIN);
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

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

.event-title {
  display: flex;
  flex-direction: column;
}

.event-description {
  display: flex;
  flex-direction: column;

  justify-content: space-around;
  align-items: center;
  flex: auto;

  margin-left: 8px;

  .event-description--wrapper {
    width: 100%;
  }
}

.event-reference {
  width: 64px;
  height: 64px;
  min-width: 64px;
  min-height: 64px;
  max-width: 64px;
  max-height: 64px;

  margin: 4px;

  cursor: pointer;
}

$hover-transparent: 0.2;

.theme--light.v-application {
  .event-reference {
    background: rgba(map-get($shades, 'black'), $hover-transparent);
  }
}

.theme--dark.v-application {
  .event-reference {
    background: rgba(map-get($shades, 'white'), $hover-transparent);
  }
}
</style>
