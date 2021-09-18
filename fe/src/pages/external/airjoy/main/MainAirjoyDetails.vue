<i18n lang="yaml">
en:
  online: "Online"
  offline: "Offline"
  groups: "Groups"
  devices: "Devices"
  details: "Details"
  categories:
    pm10: "PM10: {0}"
    pm2_5: "PM2.5: {0}"
    co2: "CO2: {0}"
    humidity: "Humidity: {0}"
    temperature: "Temperature: {0}"
    voc: "VOC"
    service: "Service: {0}"
  labels:
    search: "You can filter by author or description."
    as_new: "New A/S"
    delete: "Delete a device"
  hints:
    delete: "Please be careful! It cannot be recovered."
  headers:
    author: "Author"
    description: "Description"
    datetime: "Datetime"
    actions: "Actions"
  tooltip:
    id: "AIRJOY device ID"
    fw: "Firmware version"
  delete_confirm: "Are you sure? Are you really removing this device?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  online: "네트워크 연결이 정상 상태 입니다"
  offline: "네트워크 연결이 끊어졌습니다"
  groups: "Groups"
  devices: "Devices"
  details: "Details"
  categories:
    pm10: "미세먼지: {0}"
    pm2_5: "초미세먼지: {0}"
    co2: "이산화탄소: {0}"
    humidity: "습도: {0}"
    temperature: "온도: {0}"
    voc: "VOC"
    service: "Service: {0}"
  labels:
    search: "담당자 또는 기록을 필터링할 수 있습니다."
    as_new: "새로운 A/S 기록"
    delete: "장치 제거"
  hints:
    delete: "주의하세요! 이 명령은 되돌릴 수 없습니다!"
  headers:
    author: "담당자"
    description: "기록"
    datetime: "날짜"
    actions: "관리"
  tooltip:
    id: "AIRJOY 기기 ID"
    fw: "펌웨어 버전"
  delete_confirm: "이 장치를 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"
    ></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row>
      <v-col cols="12">
        <v-toolbar flat>
          <v-toolbar-title>
            {{ item.name }}
          </v-toolbar-title>

          <v-spacer></v-spacer>

          <v-progress-circular v-show="loading" color="primary" class="mr-2" :indeterminate="loading"
          ></v-progress-circular>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip class="mr-2" outlined color="primary" v-bind="attrs" v-on="on">
                <v-icon left>mdi-identifier</v-icon>
                {{ item.uid }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.id') }}</span>
          </v-tooltip>

          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-chip v-bind="attrs" v-on="on">
                <v-icon left>mdi-tag</v-icon>
                {{ item.fw_ver }}
              </v-chip>
            </template>
            <span>{{ $t('tooltip.fw') }}</span>
          </v-tooltip>
        </v-toolbar>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <v-row class="mt-2">
      <v-col cols="4">
        <div v-ripple class="card" @click="onClickPm10">
          <v-icon left large>mdi-dots-hexagon</v-icon>
          <span class="text--secondary text-subtitle-2">
            {{ $t('categories.pm10', [item.pm10]) }}
          </span>
        </div>
      </v-col>

      <v-col cols="4">
        <div v-ripple class="card" @click="onClickPm2_5">
          <v-icon left large>mdi-dots-horizontal</v-icon>
          <span class="text--secondary text-subtitle-2">
            {{ $t('categories.pm2_5', [item.pm2_5]) }}
          </span>
        </div>
      </v-col>

      <v-col cols="4">
        <div v-ripple class="card" @click="onClickCo2">
          <v-icon left large>mdi-molecule-co2</v-icon>
          <span class="text--secondary text-subtitle-2">
            {{ $t('categories.co2', [item.co2]) }}
          </span>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="4">
        <div v-ripple class="card" @click="onClickHumidity">
          <v-icon left large>mdi-water</v-icon>
          <span class="text--secondary text-subtitle-2">
            {{ $t('categories.humidity', [item.humidity]) }}
          </span>
        </div>
      </v-col>

      <v-col cols="4">
        <div v-ripple class="card" @click="onClickTemperature">
          <v-icon left large>mdi-thermometer</v-icon>
          <span class="text--secondary text-subtitle-2">
            {{ $t('categories.temperature', [item.temperature]) }}
          </span>
        </div>
      </v-col>

      <v-col cols="4">
        <div v-ripple class="card" @click="onClickService">
          <span class="text--secondary text-h6 font-weight-bold">
            {{ $t('categories.voc') }}
          </span>
          <span class="text--secondary text-subtitle-2">
            {{ item.voc }}
          </span>
        </div>
      </v-col>
    </v-row>

<!--    <v-list>-->
<!--      <v-list-item @click.stop="power">-->
<!--        <v-list-item-icon>-->
<!--          <v-icon>mdi-power</v-icon>-->
<!--        </v-list-item-icon>-->
<!--        <v-list-item-title>-->
<!--          {{ $t('power') }}-->
<!--        </v-list-item-title>-->
<!--      </v-list-item>-->
<!--    </v-list>-->

    <v-row>
      <v-col cols="2">
        <div v-ripple class="card elevation-2 green">
          <v-icon large>mdi-power</v-icon>
          <span class="text--secondary text-subtitle-2">POWER</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div v-ripple class="card elevation-2 orange accent-4">
          <v-icon large>mdi-weather-sunny</v-icon>
          <span class="text--secondary text-subtitle-2">UV</span>
        </div>
      </v-col>

      <v-col cols="2">

        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <div v-if="item.online" v-ripple class="card elevation-2 green" v-bind="attrs" v-on="on">
              <v-icon large>mdi-lan-connect</v-icon>
              <span class="text--secondary text-subtitle-2">ONLINE</span>
            </div>
            <div v-else v-ripple class="card elevation-2 red" v-bind="attrs" v-on="on">
              <v-icon large>mdi-lan-disconnect</v-icon>
              <span class="text--secondary text-subtitle-2">OFFLINE</span>
            </div>
          </template>
          <span>{{ onlineDescription }}</span>
        </v-tooltip>
      </v-col>

      <v-col cols="2">
        <div v-ripple class="card elevation-2">
          <v-icon large>mdi-alpha-a-circle-outline</v-icon>
          <span class="text--secondary text-subtitle-2">AUTO</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div v-ripple class="card elevation-2">
          <v-icon large>mdi-lock-open-variant</v-icon>
          <span class="text--secondary text-subtitle-2">UNLOCK</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div v-ripple class="card elevation-2">
          <v-icon large>mdi-sleep</v-icon>
          <span class="text--secondary text-subtitle-2">SLEEP</span>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="2">
        <div v-ripple class="card elevation-2">
          <v-icon large>mdi-air-filter</v-icon>
          <span class="text--secondary text-subtitle-2">RESET</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div v-ripple class="card elevation-2">
          <v-icon large>mdi-fan-auto</v-icon>
          <span class="text--secondary text-subtitle-2">AUTO</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div v-ripple class="card elevation-2">
          <v-icon large>mdi-timer-off-outline</v-icon>
          <span class="text--secondary text-subtitle-2">OFF</span>
        </div>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>

    <v-alert outlined prominent type="error" class="ma-4">
      <v-row align="center" class="pl-4">
        <v-col>
          <v-row>
            <h6 class="text-h6">{{ $t('labels.delete') }}</h6>
          </v-row>
          <v-row>
            <span class="text-body-2">{{ $t('hints.delete') }}</span>
          </v-row>
        </v-col>
        <v-col class="shrink">
          <v-btn color="error" @click.stop="onClickDelete">
            {{ $t('delete') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="320">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('labels.delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('delete_confirm') }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn :loading="loadingDelete" color="error" @click="onClickDeleteOk">
            {{ $t('delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script lang="ts">
import {Component, Emit, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import VueApexCharts from 'vue-apexcharts';
import {
  CATEGORY_PM10,
  CATEGORY_PM2_5,
  CATEGORY_CO2,
  CATEGORY_HUMIDITY,
  CATEGORY_TEMPERATURE,
  createEmptyAirjoyDeviceA
} from '@/packet/airjoy';
import AirjoyFanSpeedGroup from '@/pages/external/airjoy/components/AirjoyFanSpeedGroup.vue';

@Component({
  components: {
    AirjoyFanSpeedGroup,
    ToolbarBreadcrumbs,
    VueApexCharts,
  }
})
export default class MainAirjoyDetails extends VueBase {
  private readonly breadcrumbs = [
    {
      text: this.$t('groups'),
      disabled: false,
      href: () => this.moveToRootGroups(),
    },
    {
      text: this.$route.params.group,
      disabled: false,
      href: () => this.moveToGroup(),
    },
    {
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMain(),
    },
    {
      text: this.$t('devices'),
      disabled: false,
      href: () => this.moveToMainAirjoyDevices(),
    },
    {
      text: this.$t('details'),
      disabled: true,
    },
    {
      text: this.$route.params.airjoy,
      disabled: true,
    },
  ];

  @Prop({type: Number, default: 1000})
  readonly updateIntervalMilliseconds!: number;

  loading = false;
  item = createEmptyAirjoyDeviceA();

  intervalHandle = -1;

  showDeleteDialog = false;
  loadingDelete = false;

  created() {
    this.updateDevice();
  }

  mounted() {
    this.intervalHandle = window.setInterval(() => {
      this.updateDevice();
    }, this.updateIntervalMilliseconds);
  }

  beforeDestroy() {
    window.clearInterval(this.intervalHandle);
  }

  updateDevice() {
    this.loading = true;
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.$api2.getAirjoyDevice(group, project, device)
        .then(item => {
          this.loading = false;
          this.item = item;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  get onlineDescription() {
    if (this.item.online) {
      return this.$t('online');
    } else {
      return this.$t('offline');
    }
  }

  onClickPm10() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_PM10);
  }

  onClickPm2_5() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_PM2_5);
  }

  onClickCo2() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_CO2);
  }

  onClickHumidity() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_HUMIDITY);
  }

  onClickTemperature() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_TEMPERATURE);
  }

  onClickService() {
    this.moveToMainAirjoyService(`${this.item.uid}`);
  }

  onClickDelete() {
    this.showDeleteDialog = true;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk() {
    this.loadingDelete = true;
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.$api2.deleteAirjoyDevice(group, project, device)
        .then(() => {
          this.showDeleteDialog = false;
          this.loadingDelete = false;
          this.moveToMainAirjoyDevices();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.loadingDelete = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

.card {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-content: center;
  align-items: center;

  height: 120px;

  padding: 24px;
  border-radius: 12px;
  border-style: solid;
  border-width: 1px;

  cursor: pointer;
}

.theme--light.v-application .card {
  border-color: rgba(map-get($shades, 'black'), 0.2);
}

.theme--dark.v-application .card {
  border-color: rgba(map-get($shades, 'white'), 0.2);
}
</style>
