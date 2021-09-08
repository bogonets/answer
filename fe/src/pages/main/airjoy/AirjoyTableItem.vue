<i18n lang="yaml">
en:
  online: "Online"
  offline: "Offline"
  uv:
    normal: "UV/Normal"
    alarm: "UV/Alarm"
  tooltip:
    id: "AIRJOY device ID"
    fw: "Firmware version"
    as_last: "Last A/S: {0}"
    pm10: "PM10: {0}"
    pm2_5: "PM2.5: {0}"
    co2: "CO2: {0}"
    humidity: "Humidity: {0}"
    temperature: "Temperature: {0}"
    voc: "VOC: {0}"
  filter:
    normal: "Filter state is normal"
    reset: "Filter state is reset"
    exchange: "Filter state is exchange"
    unknown: "Filter state is unknown"
  fan:
    normal: "Fan/Normal"
    weak: "Fan/Weak"
    medium: "Fan/Medium"
    high: "Fan/High"
    auto: "Fan/Auto"
    sleep: "Fan/Sleep"
    unknown: "Fan/Unknown"
  lock:
    open: "Unlock"
    close: "Lock"
    unknown: "Lock/Unknown"
  sleep:
    enable: "Sleep/Enabled"
    disable: "Sleep/Disabled"
    unknown: "Sleep/Unknown"
  mode:
    auto: "Auto Mode"
    manual: "Manual Mode"
    unknown: "Unknown Mode"
  timer:
    cancel: "Cancel"
    off: "Off"
    one: "1h"
    two: "2h"
    four: "4h"
    eight: "8h"
    unknown: "Timer/Unknown"

ko:
  online: "네트워크 연결이 정상 상태 입니다"
  offline: "네트워크 연결이 끊어졌습니다"
  uv:
    normal: "UV 알람이 꺼져있습니다"
    alarm: "UV 알람이 켜져있습니다"
  tooltip:
    id: "AIRJOY 기기 ID"
    fw: "펌웨어 버전"
    as_last: "마지막 A/S: {0}"
    pm10: "PM10: {0}"
    pm2_5: "PM2.5: {0}"
    co2: "이산화탄소: {0}"
    humidity: "습도: {0}"
    temperature: "온도: {0}"
    voc: "VOC: {0}"
  filter:
    normal: "필터는 정상입니다"
    reset: "필터 시간 초기화"
    exchange: "필터를 교체해야 합니다"
    unknown: "알 수 없는 상태 입니다"
  fan:
    normal: "팬"
    weak: "약"
    medium: "중"
    high: "강"
    auto: "자동"
    sleep: "잠자기"
    unknown: "알 수 없는 팬 상태 입니다"
  lock:
    open: "잠금이 해제되어 있습니다"
    close: "잠금 상태 입니다"
    unknown: "알 수 없는 잠금 상태 입니다"
  sleep:
    enable: "슬립 모드 입니다"
    disable: "슬립 모드가 해제되었습니다"
    unknown: "알 수 없는 슬립 모드 입니다"
  mode:
    auto: "자동 모드 입니다"
    manual: "수동 모드 입니다"
    unknown: "알 수 없는 모드 입니다"
  timer:
    cancel: "예약을 취소합니다"
    off: "예약이 설정되어 있지 않습니다"
    one: "1시간"
    two: "2시간"
    four: "4시간"
    eight: "8시간"
    unknown: "알 수 없는 예약 시간 입니다"
</i18n>

<template>
  <div class="table-item">
    <v-divider></v-divider>

    <div class="table-item--wrapper" @click="body">
      <v-btn
          fab
          small
          :color="powerColor"
          :loading="loading"
          :disabled="loading"
          @click.stop="power"
      >
        <v-icon>mdi-power</v-icon>
      </v-btn>
      <div class="table-item--body-left">
        <div class="table-item--body-left-top">
          <span class="text--primary text-subtitle-2" @click.stop="name">
            {{ item.name }}
          </span>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" x-small outlined color="primary" v-bind="attrs" v-on="on">
                <v-icon left small>mdi-identifier</v-icon>
                {{ item.uid }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.id') }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" x-small outlined v-bind="attrs" v-on="on">
                <v-icon left>mdi-tag</v-icon>
                {{ item.fwVer }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.fw') }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" x-small :color="filterColor" v-bind="attrs" v-on="on">
                <v-icon left>mdi-air-filter</v-icon>
                <v-icon v-if="filterReset" left>mdi-timer-outline</v-icon>
                <v-icon v-if="filterExchange" left>mdi-cached</v-icon>
                <v-icon v-if="filterUnknown" left>mdi-help</v-icon>
                {{ filterLifeMinutes }}
              </v-chip>
            </template>
            <span>{{ filterLifeDescription }}</span>
          </v-tooltip>

          <v-tooltip v-if="!item.uvLed" bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" x-small color="orange accent-4" v-bind="attrs" v-on="on">
                <v-icon>mdi-weather-sunny</v-icon>
              </v-chip>
            </template>
            <span>{{ uvLedDescription }}</span>
          </v-tooltip>

          <v-tooltip v-if="!item.online" bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip x-small :color="onlineColor" v-bind="attrs" v-on="on">
                <v-icon>mdi-lan-connect</v-icon>
              </v-chip>
            </template>
            <span>{{ onlineDescription }}</span>
          </v-tooltip>
        </div>

        <div class="table-item--body-left-bottom">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" small v-bind="attrs" v-on="on">
                <v-icon left>mdi-dots-hexagon</v-icon>
                {{ item.pm10 }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.pm10', [item.pm10]) }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" small v-bind="attrs" v-on="on">
                <v-icon left>mdi-dots-horizontal</v-icon>
                {{ item.pm2_5 }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.pm2_5', [item.pm2_5]) }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" small v-bind="attrs" v-on="on">
                <v-icon left>mdi-molecule-co2</v-icon>
                {{ item.co2 }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.co2', [item.co2]) }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" small v-bind="attrs" v-on="on">
                <v-icon left>mdi-water</v-icon>
                {{ item.humidity }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.humidity', [item.humidity]) }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" small v-bind="attrs" v-on="on">
                <v-icon left>mdi-thermometer</v-icon>
                {{ item.temperature }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.temperature', [item.temperature]) }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" small v-bind="attrs" v-on="on">
                <v-icon left size="22">mdi-alpha-v</v-icon>
                {{ item.voc }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.voc', [item.voc]) }}</span>
          </v-tooltip>

          <v-tooltip v-if="item.asCount" bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-1" small v-bind="attrs" v-on="on">
                <v-icon left>mdi-wrench</v-icon>
                {{ item.asCount }}
              </v-chip>
            </template>
            <span v-if="item.asLast">
              {{ $t('tooltip.as_last', [item.asLast]) }}
            </span>
          </v-tooltip>
        </div>
      </div>

      <div class="table-item--body-center">
        <div
            v-if="$vuetify.breakpoint.mdAndUp && !hideDescription"
            class="text--secondary text-body-2 text-center"
        >
          {{ item.description }}
        </div>
      </div>

      <div class="table-item--body-right">

        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small icon :disabled="loading" @click.stop="mode" v-bind="attrs" v-on="on">
              <v-icon>{{ modeIcon }}</v-icon>
            </v-btn>
          </template>
          <span>{{ modeDescription }}</span>
        </v-tooltip>

        <v-menu class="button-group" offset-y>
          <template v-slot:activator="{ on: menu, attrs }">
            <v-tooltip top>
              <template v-slot:activator="{ on: tooltip }">
                <v-btn x-small icon :disabled="loading" v-bind="attrs" v-on="{...tooltip, ...menu}">
                  <v-icon>{{ fanIcon }}</v-icon>
                </v-btn>
              </template>
              <span>{{ fanDescription }}</span>
            </v-tooltip>
          </template>

          <div class="button-group--wrapper">
            <v-btn class="rounded-l-xl" small tile @click.stop="fanWeak">
              <v-icon>mdi-fan-speed-1</v-icon>
            </v-btn>
            <v-btn small tile @click.stop="fanMedium">
              <v-icon>mdi-fan-speed-2</v-icon>
            </v-btn>
            <v-btn class="rounded-r-xl" small tile @click.stop="fanHigh">
              <v-icon>mdi-fan-speed-3</v-icon>
            </v-btn>
          </div>
        </v-menu>

        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small icon :disabled="loading" @click.stop="lock" v-bind="attrs" v-on="on">
              <v-icon>{{ lockIcon }}</v-icon>
            </v-btn>
          </template>
          <span>{{ lockDescription }}</span>
        </v-tooltip>

        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small icon :disabled="loading" @click.stop="filter" v-bind="attrs" v-on="on">
              <v-icon :color="filterColor">mdi-air-filter</v-icon>
            </v-btn>
          </template>
          <span>{{ filterLifeDescription }}</span>
        </v-tooltip>

        <v-tooltip top>
          <template v-slot:activator="{ on, attrs }">
            <v-btn x-small icon :disabled="loading" @click.stop="sleep" v-bind="attrs" v-on="on">
              <v-icon>{{ sleepIcon }}</v-icon>
            </v-btn>
          </template>
          <span>{{ sleepDescription }}</span>
        </v-tooltip>

        <v-menu class="button-group" offset-y>
          <template v-slot:activator="{ on: menu, attrs }">
            <v-tooltip top>
              <template v-slot:activator="{ on: tooltip }">
                <v-btn x-small icon :disabled="loading" v-bind="attrs" v-on="{...tooltip, ...menu}">
                  <v-icon>{{ timerIcon }}</v-icon>
                </v-btn>
              </template>
              <span>{{ timerDescription }}</span>
            </v-tooltip>
          </template>

          <div class="button-group--wrapper">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn class="rounded-l-xl" small tile @click.stop="timeOff" v-bind="attrs" v-on="on">
                  <v-icon>mdi-timer-off-outline</v-icon>
                </v-btn>
              </template>
              <span>{{ $t('timer.cancel') }}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn small tile @click.stop="timeOne" v-bind="attrs" v-on="on">
                  <v-icon>mdi-clock-time-one-outline</v-icon>
                </v-btn>
              </template>
              <span>{{ $t('timer.one') }}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn small tile @click.stop="timeTwo" v-bind="attrs" v-on="on">
                  <v-icon>mdi-clock-time-two-outline</v-icon>
                </v-btn>
              </template>
              <span>{{ $t('timer.two') }}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn small tile @click.stop="timeFour" v-bind="attrs" v-on="on">
                  <v-icon>mdi-clock-time-four-outline</v-icon>
                </v-btn>
              </template>
              <span>{{ $t('timer.four') }}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn class="rounded-r-xl" small tile @click.stop="timeEight" v-bind="attrs" v-on="on">
                  <v-icon>mdi-clock-time-eight-outline</v-icon>
                </v-btn>
              </template>
              <span>{{ $t('timer.eight') }}</span>
            </v-tooltip>
          </div>
        </v-menu>

      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import type {AirjoyA} from "@/packet/airjoy";
import {createEmptyAirjoyA} from "@/packet/airjoy";

const FILTER_STATUS_NORMAL = 0;
const FILTER_STATUS_RESET = 1;
const FILTER_STATUS_EXCHANGE = 2;

const FILTER_LIFE_MINUTES_UNIT = 10;

const FAN_CONTROL_NORMAL = 0;
const FAN_CONTROL_WEAK = 1;
const FAN_CONTROL_MEDIUM = 2;
const FAN_CONTROL_HIGH = 3;
const FAN_CONTROL_AUTO = 4;
const FAN_CONTROL_SLEEP = 5;

const UNLOCK = 0;
const LOCK = 1;

@Component({
  components: {
    BreadcrumbMain,
  }
})
export default class AirjoyTable extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly hideDescription!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disable!: boolean;

  @Prop({type: Object, default: createEmptyAirjoyA})
  readonly item!: AirjoyA;

  get powerColor() {
    if (this.item.powerState) {
      return 'green';
    } else {
      return 'deep-orange';
    }
  }

  get modeDescription() {
    switch (this.item.mode) {
      case 0:
        return this.$t('mode.auto');
      case 1:
        return this.$t('mode.manual');
      default:
        return this.$t('mode.unknown');
    }
  }

  get filterLifeMinutes() {
    const life = this.item.filterLife || 0;
    const lifeMinutes = life * FILTER_LIFE_MINUTES_UNIT;
    return `${lifeMinutes}m`;
  }

  get filterReset() {
    return this.item.filter == FILTER_STATUS_RESET;
  }

  get filterExchange() {
    return this.item.filter == FILTER_STATUS_EXCHANGE;
  }

  get filterColor() {
    switch (this.item.filter) {
      case FILTER_STATUS_NORMAL:
        return '';  // 'light-green darken-4';
      case FILTER_STATUS_RESET:
        return 'yellow darken-4';
      case FILTER_STATUS_EXCHANGE:
        return 'red';
      default:
        return 'blue-grey';
    }
  }

  get filterUnknown() {
    switch (this.item.filter) {
      case FILTER_STATUS_NORMAL:
      case FILTER_STATUS_RESET:
      case FILTER_STATUS_EXCHANGE:
        return false;
      default:
        return true;
    }
  }

  get filterLifeDescription() {
    switch (this.item.filter) {
      case FILTER_STATUS_NORMAL:
        return this.$t('filter.normal');
      case FILTER_STATUS_RESET:
        return this.$t('filter.reset');
      case FILTER_STATUS_EXCHANGE:
        return this.$t('filter.exchange');
      default:
        return this.$t('filter.unknown');
    }
  }

  get uvLedDescription() {
    if (this.item.uvLed) {
      return this.$t('uv.normal');
    } else {
      return this.$t('uv.alarm');
    }
  }

  get onlineColor() {
    if (this.item.online) {
      return 'green';
    } else {
      return 'red';
    }
  }

  get onlineDescription() {
    if (this.item.online) {
      return this.$t('online');
    } else {
      return this.$t('offline');
    }
  }

  get modeIcon() {
    switch (this.item.mode) {
      case 0:
        return 'mdi-alpha-a-circle-outline';
      case 1:
        return 'mdi-alpha-m-circle';
      default:
        return 'mdi-help-circle-outline';
    }
  }

  get fanIcon() {
    switch (this.item.fanControl) {
      case FAN_CONTROL_NORMAL:
        return 'mdi-fan';
      case FAN_CONTROL_WEAK:
        return 'mdi-fan-speed-1';
      case FAN_CONTROL_MEDIUM:
        return 'mdi-fan-speed-2';
      case FAN_CONTROL_HIGH:
        return 'mdi-fan-speed-3';
      case FAN_CONTROL_AUTO:
        return 'mdi-fan-auto';
      case FAN_CONTROL_SLEEP:
        return 'mdi-fan-off';
      default:
        return 'mdi-fan';
    }
  }

  get fanDescription() {
    switch (this.item.fanControl) {
      case FAN_CONTROL_NORMAL:
        return this.$t('fan.normal');
      case FAN_CONTROL_WEAK:
        return this.$t('fan.weak');
      case FAN_CONTROL_MEDIUM:
        return this.$t('fan.medium');
      case FAN_CONTROL_HIGH:
        return this.$t('fan.high');
      case FAN_CONTROL_AUTO:
        return this.$t('fan.auto');
      case FAN_CONTROL_SLEEP:
        return this.$t('fan.sleep');
      default:
        return this.$t('fan.unknown');
    }
  }

  get fanSpeedIndex() {
    switch (this.item.fanControl) {
      case FAN_CONTROL_WEAK:
        return 0;
      case FAN_CONTROL_MEDIUM:
        return 1;
      case FAN_CONTROL_HIGH:
        return 2;
      default:
        return -1;
    }
  }

  get lockIcon() {
    switch (this.item.lock) {
      case LOCK:
        return 'mdi-lock';
      case UNLOCK:
        return 'mdi-lock-open-variant';
      default:
        return 'mdi-lock-alert';
    }
  }

  get lockDescription() {
    switch (this.item.lock) {
      case LOCK:
        return this.$t('lock.close');
      case UNLOCK:
        return this.$t('lock.open');
      default:
        return this.$t('lock.unknown');
    }
  }

  get sleepIcon() {
    switch (this.item.sleepMode) {
      case 0:
        return 'mdi-sleep-off';
      case 1:
        return 'mdi-sleep';
      default:
        return 'mdi-help';
    }
  }

  get sleepDescription() {
    switch (this.item.sleepMode) {
      case 0:
        return this.$t('sleep.disable');
      case 1:
        return this.$t('sleep.enable');
      default:
        return this.$t('sleep.unknown');
    }
  }

  get timerIcon() {
    switch (this.item.timeReservation) {
      case 0:
        return 'mdi-timer-off-outline';
      case 1:
        return 'mdi-clock-time-one-outline';
      case 2:
        return 'mdi-clock-time-two-outline';
      case 3:
        return 'mdi-clock-time-four-outline';
      case 4:
        return 'mdi-clock-time-eight-outline';
      default:
        return 'mdi-help';
    }
  }

  get timerDescription() {
    const time = this.item.timeReservation || 0;
    switch (time) {
      case 0:
        return this.$t('timer.off');
      case 1:
        return this.$t('timer.one');
      case 2:
        return this.$t('timer.two');
      case 3:
        return this.$t('timer.four');
      case 4:
        return this.$t('timer.eight');
      default:
        return this.$t('timer.unknown');
    }
  }

  @Emit('click:body')
  body() {
    return this.item;
  }

  @Emit('click:name')
  name() {
    return this.item;
  }

  @Emit('click:power')
  power() {
    return this.item;
  }

  @Emit('click:mode')
  mode() {
    return this.item;
  }

  @Emit('click:fan-weak')
  fanWeak() {
    return this.item;
  }

  @Emit('click:fan-medium')
  fanMedium() {
    return this.item;
  }

  @Emit('click:fan-high')
  fanHigh() {
    return this.item;
  }

  @Emit('click:lock')
  lock() {
    return this.item;
  }

  @Emit('click:filter')
  filter() {
    return this.item;
  }

  @Emit('click:sleep')
  sleep() {
    return this.item;
  }

  @Emit('click:time-off')
  timeOff() {
    return this.item;
  }

  @Emit('click:time-one')
  timeOne() {
    return this.item;
  }

  @Emit('click:time-two')
  timeTwo() {
    return this.item;
  }

  @Emit('click:time-four')
  timeFour() {
    return this.item;
  }

  @Emit('click:time-eight')
  timeEight() {
    return this.item;
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

@mixin flex-column {
  display: flex;
  flex-direction: column;
}

@mixin flex-row {
  display: flex;
  flex-direction: row;
}

.table-item {
  @include flex-column;

  .table-item--wrapper {
    @include flex-row;
    align-items: center;
    padding: 4px;

    .table-item--body-left {
      @include flex-column;
      padding-left: 8px;

      .table-item--body-left-top {
      }
      .table-item--body-left-bottom {
      }
    }

    .table-item--body-center {
      @include flex-row;
      justify-content: space-around;
      align-items: center;
      flex: auto;
    }

    .table-item--body-right {
      @include flex-row;
      align-items: center;
      padding-right: 4px;
    }
  }
}

$hover-transparent: 0.2;

.theme--light.v-application {
  .table-item .table-item--wrapper:hover {
    cursor: pointer;
    border-radius: 3px;
    background: rgba(map-get($shades, 'black'), $hover-transparent);
  }
}

.theme--dark.v-application {
  .table-item .table-item--wrapper:hover {
    cursor: pointer;
    border-radius: 3px;
    background: rgba(map-get($shades, 'white'), $hover-transparent);
  }
}

.v-menu__content {
  box-shadow: none;
}

.button-group--wrapper {
  @include flex-row;
  flex-wrap: nowrap;
  padding: 2px;
}
</style>
