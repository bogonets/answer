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
            @click:as="onClickAs"
            @click:mode="onClickMode"
            @click:fan-weak="onClickFanWeak"
            @click:fan-medium="onClickFanMedium"
            @click:fan-high="onClickFanHigh"
            @click:lock="onClickLock"
            @click:filter="onClickFilter"
            @click:sleep="onClickSleep"
            @click:time-off="onClickTimeOff"
            @click:time-one="onClickTimeOne"
            @click:time-two="onClickTimeTwo"
            @click:time-four="onClickTimeFour"
            @click:time-eight="onClickTimeEight"
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
import type {AirjoyDeviceA} from '@/packet/airjoy';
import {
  CATEGORY_PM10,
  CATEGORY_PM2_5,
  CATEGORY_CO2,
  CATEGORY_HUMIDITY,
  CATEGORY_TEMPERATURE,
  CATEGORY_VOC, CreateAirjoyDeviceQ,
} from '@/packet/airjoy';

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

  onClickAddOk(body: CreateAirjoyDeviceQ) {
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

  onClickPower(item: AirjoyDeviceA) {
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

  onClickAs(item: AirjoyDeviceA) {
  }

  onClickMode(item: AirjoyDeviceA) {
  }

  onClickFanWeak(item: AirjoyDeviceA) {
  }

  onClickFanMedium(item: AirjoyDeviceA) {
  }

  onClickFanHigh(item: AirjoyDeviceA) {
  }

  onClickLock(item: AirjoyDeviceA) {
  }

  onClickFilter(item: AirjoyDeviceA) {
  }

  onClickSleep(item: AirjoyDeviceA) {
  }

  onClickTimeOff(item: AirjoyDeviceA) {
  }

  onClickTimeOne(item: AirjoyDeviceA) {
  }

  onClickTimeTwo(item: AirjoyDeviceA) {
  }

  onClickTimeFour(item: AirjoyDeviceA) {
  }

  onClickTimeEight(item: AirjoyDeviceA) {
  }
}
</script>
