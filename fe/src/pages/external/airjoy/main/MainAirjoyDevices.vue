<i18n lang="yaml">
en:
  add_device:
    button: "Add Device"
    title: "Register Airjoy Device"
    subtitle: "Detects and registers new Airjoy devices"
  label:
    search: "You can filter by name or UID."
  msg:
    loading: "Loading... Please wait"
    empty: "Devices do not exist"

ko:
  add_device:
    button: "장치 추가"
    title: "에어조이 기기 등록"
    subtitle: "새로운 에어조이 기기를 탐지하고 등록합니다"
  label:
    search: "이름 또는 UID를 필터링할 수 있습니다."
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "장치가 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <breadcrumb-main name="Table"></breadcrumb-main>
    <v-divider></v-divider>

    <v-data-table
        hide-default-header
        sort-desc
        sort-by="name"
        :items="items"
        :search="filter"
        :loading="loading"
        :headers="headers"
        :loading-text="$t('msg.loading')"
    >
      <template v-if="!hideTopBar" v-slot:top>
        <v-toolbar flat>
          <v-text-field
              v-if="!hideFilterInput"
              class="mr-4"
              v-model="filter"
              append-icon="mdi-magnify"
              single-line
              hide-details
              :label="$t('label.search')"
          ></v-text-field>
          <v-btn color="primary" @click="onClickAddDevice">
            {{ $t('add_device.button') }}
          </v-btn>
        </v-toolbar>
      </template>

      <template v-slot:item="{ item }">
        <airjoy-device-row
            hide-description
            :item="item"
            @click:body="onClickBody"
            @click:name="onClickName"
            @click:power="onClickPower"
            @click:pm10="onClickPm10"
            @click:pm2_5="onClickPm2_5"
            @click:co2="onClickCo2"
            @click:humidity="onClickHumidity"
            @click:temperature="onClickTemperature"
            @click:voc="onClickVoc"
            @click:service="onClickService"
            @click:mode="onClickMode"
            @click:fan-weak="onClickFanWeak"
            @click:fan-medium="onClickFanMedium"
            @click:fan-high="onClickFanHigh"
            @click:lock="onClickLock"
            @click:filter="onClickFilter"
            @click:sleep="onClickSleep"
            @click:timer-off="onClickTimerOff"
            @click:timer-one="onClickTimerOne"
            @click:timer-two="onClickTimerTwo"
            @click:timer-four="onClickTimerFour"
            @click:timer-eight="onClickTimerEight"
        ></airjoy-device-row>
      </template>

      <template v-slot:no-data>
        {{ $t('msg.empty') }}
      </template>
    </v-data-table>

    <!-- Add Dialog -->
    <v-dialog
        v-model="showAddDialog"
        persistent
        no-click-animation
        :max-width="widthAddDialog"
        @keydown.esc.stop="onClickAddCancel"
    >
      <airjoy-device-add
          :title="$t('add_device.title')"
          :subtitle="$t('add_device.subtitle')"
          :submit-loading="loadingAddDevice"
          @cancel="onClickAddCancel"
          @ok="onClickAddOk"
      ></airjoy-device-add>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import AirjoyDeviceRow from '@/pages/external/airjoy/components/AirjoyDeviceRow.vue';
import AirjoyDeviceAdd from '@/pages/external/airjoy/components/AirjoyDeviceAdd.vue';
import {
  CATEGORY_PM10,
  CATEGORY_PM2_5,
  CATEGORY_CO2,
  CATEGORY_HUMIDITY,
  CATEGORY_TEMPERATURE,
  CATEGORY_VOC,
} from '@/packet/airjoy';
import type {
  AirjoyDeviceA,
  AirjoyCreateDeviceQ,
  AirjoyControlQ,
} from '@/packet/airjoy';
import {Control} from "@/pages/external/airjoy/main/MainAirjoyDetails.vue";

const POWER_STATE_OFF = 0;
const POWER_STATE_ON = 1;

const MODE_AUTO = 0;
const MODE_MANUAL = 1;

const FAN_CONTROL_WEAK = 1;
const FAN_CONTROL_MEDIUM = 2;
const FAN_CONTROL_HIGH = 3;

const UNLOCK = 0;
const LOCK = 1;

const AWAKE = 0;
const SLEEP = 1;

@Component({
  components: {
    BreadcrumbMain,
    AirjoyDeviceRow,
    AirjoyDeviceAdd,
  }
})
export default class MainAirjoyDevices extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly hideFilterInput!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionDelete!: boolean;

  @Prop({type: Boolean, default: false})
  readonly clickableRow!: boolean;

  @Prop({type: Number, default: 480})
  readonly widthAddDialog!: number;

  @Prop({type: Number, default: 1000})
  readonly updateIntervalMilliseconds!: number;

  readonly headers = [
    {
      filterable: true,
      value: 'name',
    },
    {
      filterable: true,
      value: 'uid',
    },
  ];

  loading = false;
  items = [] as Array<AirjoyDeviceA>;
  filter = '';

  showAddDialog = false;
  loadingAddDevice = false;

  intervalHandle = -1;

  get hideTopBar(): boolean {
    return this.hideFilterInput;
  }

  created() {
    this.updateDevices();
  }

  mounted() {
    this.intervalHandle = window.setInterval(() => {
      this.updateDevices(false);
    }, this.updateIntervalMilliseconds);
  }

  beforeDestroy() {
    window.clearInterval(this.intervalHandle);
  }

  updateDevices(changeLoading = true) {
    if (changeLoading) {
      this.loading = true;
    }
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.$api2.getAirjoyDevices(group, project)
        .then(items => {
          if (changeLoading) {
            this.loading = false;
          }
          this.items = items;
        })
        .catch(error => {
          if (changeLoading) {
            this.loading = false;
          }
          this.toastRequestFailure(error);
        });
  }

  onClickAddDevice() {
    this.showAddDialog = true;
  }

  onClickAddCancel() {
    this.showAddDialog = false;
  }

  onClickAddOk(body: AirjoyCreateDeviceQ) {
    this.loadingAddDevice = true;
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.$api2.postAirjoyDevices(group, project, body)
        .then(() => {
          this.loadingAddDevice = false;
          this.showAddDialog = false;
          this.toastRequestSuccess();
          this.updateDevices();
        })
        .catch(error => {
          this.loadingAddDevice = false;
          this.toastRequestFailure(error);
        })
  }

  onClickBody(item: AirjoyDeviceA) {
    this.moveToMainAirjoyDetails(`${item.uid}`);
  }

  onClickName(item: AirjoyDeviceA) {
    this.moveToMainAirjoyDetails(`${item.uid}`);
  }

  onClickPm10(item: AirjoyDeviceA) {
    this.moveToMainAirjoyChart(`${item.uid}`, CATEGORY_PM10);
  }

  onClickPm2_5(item: AirjoyDeviceA) {
    this.moveToMainAirjoyChart(`${item.uid}`, CATEGORY_PM2_5);
  }

  onClickCo2(item: AirjoyDeviceA) {
    this.moveToMainAirjoyChart(`${item.uid}`, CATEGORY_CO2);
  }

  onClickHumidity(item: AirjoyDeviceA) {
    this.moveToMainAirjoyChart(`${item.uid}`, CATEGORY_HUMIDITY);
  }

  onClickTemperature(item: AirjoyDeviceA) {
    this.moveToMainAirjoyChart(`${item.uid}`, CATEGORY_TEMPERATURE);
  }

  onClickVoc(item: AirjoyDeviceA) {
    this.moveToMainAirjoyChart(`${item.uid}`, CATEGORY_VOC);
  }

  onClickService(item: AirjoyDeviceA) {
    this.moveToMainAirjoyService(`${item.uid}`);
  }

  controlDevice(item: AirjoyDeviceA, state: Control) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    const body = {
      uid: item.uid,
      mode: state.mode ?? item.mode,
      power_state: state.power_state ?? item.power_state,
      fan_control: state.fan_control ?? item.fan_control,
      lock: state.lock ?? item.lock,
      filter_reset: state.filter_reset ?? 0,
      sleep_mode: state.sleep_mode ?? item.sleep_mode,
      time_reservation: state.time_reservation ?? item.time_reservation,
    } as AirjoyControlQ;
    this.$api2.postAirjoyControl(group, project, item.uid.toString(), body)
        .then(() => {
          this.loading = false;
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  onClickPower(item: AirjoyDeviceA) {
    let power_state;
    if (item.power_state == POWER_STATE_ON) {
      power_state = POWER_STATE_OFF;
    } else {
      power_state = POWER_STATE_ON;
    }
    this.controlDevice(item, {power_state: power_state});
  }

  onClickMode(item: AirjoyDeviceA) {
    let mode;
    if (item.mode == MODE_AUTO) {
      mode = MODE_MANUAL;
    } else {
      mode = MODE_AUTO;
    }
    this.controlDevice(item, {mode: mode});
  }

  onClickFanWeak(item: AirjoyDeviceA) {
    this.controlDevice(item, {fan_control: FAN_CONTROL_WEAK});
  }

  onClickFanMedium(item: AirjoyDeviceA) {
    this.controlDevice(item, {fan_control: FAN_CONTROL_MEDIUM});
  }

  onClickFanHigh(item: AirjoyDeviceA) {
    this.controlDevice(item, {fan_control: FAN_CONTROL_HIGH});
  }

  onClickLock(item: AirjoyDeviceA) {
    let lock;
    if (item.lock == LOCK) {
      lock = UNLOCK;
    } else {
      lock = LOCK;
    }
    this.controlDevice(item, {lock: lock});
  }

  onClickFilter(item: AirjoyDeviceA) {
    this.controlDevice(item, {filter_reset: 1});
  }

  onClickSleep(item: AirjoyDeviceA) {
    let sleep_mode;
    if (item.sleep_mode == SLEEP) {
      sleep_mode = AWAKE;
    } else {
      sleep_mode = SLEEP;
    }
    this.controlDevice(item, {sleep_mode: sleep_mode});
  }

  onClickTimerOff(item: AirjoyDeviceA) {
    this.controlDevice(item, {time_reservation: 0});
  }

  onClickTimerOne(item: AirjoyDeviceA) {
    this.controlDevice(item, {time_reservation: 1});
  }

  onClickTimerTwo(item: AirjoyDeviceA) {
    this.controlDevice(item, {time_reservation: 2});
  }

  onClickTimerFour(item: AirjoyDeviceA) {
    this.controlDevice(item, {time_reservation: 3});
  }

  onClickTimerEight(item: AirjoyDeviceA) {
    this.controlDevice(item, {time_reservation: 4});
  }
}
</script>
