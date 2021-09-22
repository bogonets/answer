<i18n lang="yaml">
en:
  groups: "Groups"
  devices: "Devices"
  chart: "Chart"
  period:
    start: "Start date"
    end: "End date"
  labels:
    device: "Please select a device ID to output as a chart"
    category: "Please select a category to output as a chart"
  categories:
    pm10: "PM10"
    pm2_5: "PM2.5"
    co2: "CO2"
    humidity: "Humidity"
    temperature: "Temperature"
    voc: "VOC"
  msg:
    empty_device: "Empty device"
    empty_category: "Empty category"
  range:
    d90: "90d"
    d30: "30d"
    d7: "7d"
    d1: "1d"

ko:
  groups: "Groups"
  devices: "Devices"
  chart: "Chart"
  period:
    start: "시작일"
    end: "종료일"
  labels:
    device: "차트로 출력할 장치 ID를 선택하세요"
    category: "차트로 출력할 카테고리를 선택하세요"
  categories:
    pm10: "미세먼지"
    pm2_5: "초미세먼지"
    co2: "이산화탄소"
    humidity: "습도"
    temperature: "온도"
    voc: "VOC"
  msg:
    empty_device: "Empty device"
    empty_category: "Empty category"
  range:
    d90: "90일"
    d30: "30일"
    d7: "일주"
    d1: "오늘"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row class="mt-4">
      <v-col class="pb-0" cols="12">
        <v-select
            dense
            rounded
            outlined
            hide-details
            v-model="device"
            :loading="loadingDevices"
            :items="devices"
            :label="$t('labels.device')"
            @change="onChangeDevice"
        >
          <template v-slot:item="{ item }">
            {{ item.name }}
            <v-chip class="ml-2" x-small outlined color="primary">
              <v-icon left>mdi-identifier</v-icon>
              {{ item.uid }}
            </v-chip>
          </template>

          <template v-slot:selection="{ item }">
            {{ item.name }}
            <v-chip class="ml-2" x-small outlined color="primary">
              <v-icon left>mdi-identifier</v-icon>
              {{ item.uid }}
            </v-chip>
          </template>
        </v-select>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col class="pb-0" cols="12">
        <v-select
            dense
            rounded
            outlined
            hide-details
            v-model="category"
            :items="categories"
            :label="$t('labels.category')"
            @change="onChangeCategory"
        ></v-select>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="8">
        <div class="d-inline-flex flex-row align-center text-center">
          <v-icon class="mr-2">mdi-calendar</v-icon>
          <v-menu
              offset-y
              transition="scale-transition"
              min-width="auto"
              v-model="showPeriodStartMenu"
              :nudge-right="datePickerSize"
              :close-on-content-click="false"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                  dense
                  rounded
                  outlined
                  readonly
                  hide-details
                  v-model="periodStart"
                  :label="$t('period.start')"
                  v-bind="attrs"
                  v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
                v-model="periodStart"
                no-title
                scrollable
                @input="onInputPeriodStart"
            ></v-date-picker>
          </v-menu>
          <span class="mx-2">~</span>
          <v-menu
              offset-y
              transition="scale-transition"
              min-width="auto"
              v-model="showPeriodEndMenu"
              :nudge-right="datePickerSize"
              :close-on-content-click="false"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-text-field
                  dense
                  rounded
                  outlined
                  readonly
                  hide-details
                  v-model="periodEnd"
                  :label="$t('period.end')"
                  v-bind="attrs"
                  v-on="on"
              ></v-text-field>
            </template>
            <v-date-picker
                v-model="periodEnd"
                no-title
                scrollable
                @input="onInputPeriodEnd"
            ></v-date-picker>
          </v-menu>
        </div>
      </v-col>

      <v-col class="d-flex flex-row align-center" cols="4">
        <v-spacer></v-spacer>
        <v-btn-toggle dense>
          <v-btn @click="onClickRange90d">
            {{ $t('range.d90') }}
          </v-btn>
          <v-btn @click="onClickRange30d">
            {{ $t('range.d30') }}
          </v-btn>
          <v-btn @click="onClickRange7d">
            {{ $t('range.d7') }}
          </v-btn>
          <v-btn @click="onClickRange1d">
            {{ $t('range.d1') }}
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>

    <v-card class="mt-4 pt-4">
      <vue-apex-charts
          class="mx-2"
          type="rangeBar"
          height="350"
          ref="chart"
          :options="chartOptions"
          :series="series"
      ></vue-apex-charts>
      <v-spacer class="py-4"></v-spacer>
    </v-card>

  </v-container>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import VueApexCharts from 'vue-apexcharts';
import type {AirjoyDeviceA, AirjoySensorA} from '@/packet/airjoy';
import {
  CATEGORY_PM10,
  CATEGORY_PM2_5,
  CATEGORY_CO2,
  CATEGORY_HUMIDITY,
  CATEGORY_TEMPERATURE,
  CATEGORY_VOC,
  createEmptyAirjoyDeviceA,
} from '@/packet/airjoy';
import * as _ from 'lodash';

export function dateToText(time: Date) {
  const year = time.getFullYear();
  const month = time.getMonth() + 1;
  const day = time.getDate();
  const yearText = `${year}`.padStart(4, '0');
  const monthText = `${month}`.padStart(2, '0');
  const dayText = `${day}`.padStart(2, '0');
  return `${yearText}-${monthText}-${dayText}`;
}

export function today() {
  return dateToText(new Date(Date.now()));
}

export function yesterday() {
  const now = new Date(Date.now());
  const start = new Date();
  start.setDate(now.getDate() - 1);
  return dateToText(start);
}

export function dateRange(days: number) {
  const end = new Date(Date.now());
  const start = new Date();
  start.setDate(end.getDate() - days);
  return [dateToText(start), dateToText(end)];
}

const UNKNOWN_DEVICE = '-';
const CHUNK_SIZE = 10;

const INDEX_PM10 = 0;
const INDEX_PM2_5 = 1;
const INDEX_CO2 = 2;
const INDEX_HUMIDITY = 3;
const INDEX_TEMPERATURE = 4;
const INDEX_VOC = 5;


@Component({
  components: {
    ToolbarBreadcrumbs,
    VueApexCharts,
  }
})
export default class MainAirjoyChart extends VueBase {
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
      text: this.$t('chart'),
      disabled: true,
    },
    {
      text: this.$route.params.airjoy,
      disabled: true,
    },
  ];

  readonly chartOptions = {
    theme: {
      mode: this.$vuetify.theme.dark ? 'dark' : 'light',
    },
    chart: {
      height: 350,
      type: 'rangeBar',
    },
    plotOptions: {
      bar: {
        horizontal: false
      }
    },
    // title: {
    //   text: 'CandleStick Chart - Category X-axis',
    //   align: 'left'
    // },
    tooltip: {
      enabled: true,
    },
    xaxis: {
      type: 'datetime',
    //   labels: {
    //     formatter: function(val) {
    //       const n = Date.parse(val)
    //       const d = new Date(n);
    //       const s = d.toLocaleString();
    //       return s;
    //     }
    //   }
    },
    yaxis: {
    //   tooltip: {
    //     enabled: true
    //   }
    }
  };

  series = [];

  @Prop({type: Number, default: 40})
  readonly datePickerSize!: number;

  loadingDevices = false;
  device = createEmptyAirjoyDeviceA();
  devices = [] as Array<AirjoyDeviceA>;

  showPeriodStartMenu = false;
  periodStart = yesterday();

  showPeriodEndMenu = false;
  periodEnd = today();

  category = '';

  loading = false;
  items = [] as Array<AirjoySensorA>;

  created() {
    let uid = undefined;
    if (!!this.$route.params.device && this.$route.params.device !== UNKNOWN_DEVICE) {
      uid = Number.parseInt(this.$route.params.device);
    }
    this.updateDevices(uid);

    const index = this.getCategoryIndexByEnum(this.$route.params.category);
    if (index !== -1) {
      this.category = this.categories[index];
    } else {
      this.category = this.categories[0];
    }
  }

  getCategoryIndexByEnum(name: string) {
    if (name === CATEGORY_PM10) {
      return INDEX_PM10;
    } else if (name === CATEGORY_PM2_5) {
      return INDEX_PM2_5;
    } else if (name === CATEGORY_CO2) {
      return INDEX_CO2;
    } else if (name === CATEGORY_HUMIDITY) {
      return INDEX_HUMIDITY;
    } else if (name === CATEGORY_TEMPERATURE) {
      return INDEX_TEMPERATURE;
    } else if (name === CATEGORY_VOC) {
      return INDEX_VOC;
    } else {
      return -1;
    }
  }

  get categories() {
    return [
      this.$t('categories.pm10').toString(),
      this.$t('categories.pm2_5').toString(),
      this.$t('categories.co2').toString(),
      this.$t('categories.humidity').toString(),
      this.$t('categories.temperature').toString(),
      this.$t('categories.voc').toString(),
    ];
  }

  get categoryIndex() {
    return this.categories.findIndex(i => i === this.category);
  }

  updateDevices(device?: number) {
    this.loadingDevices = true;
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.$api2.getAirjoyDevices(group, project)
        .then(items => {
          this.loadingDevices = false;
          this.devices = items;
          if (typeof device !== 'undefined') {
            this.device = this.devices.find(i => i.uid === device);
          } else {
            this.device = createEmptyAirjoyDeviceA();
          }
        })
        .catch(error => {
          this.loadingDevices = false;
          this.toastRequestFailure(error);
        });
  }

  updateChart() {
    if (!this.device.uid) {
      return;
    }

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.device.uid;
    this.$api2.getAirjoyChart(group, project, device, this.periodStart, this.periodEnd)
        .then(items => {
          this.items = items;
          this.toastRequestSuccess();
          this.updateSeries();
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  updateSeries() {
    const pm10 = [];
    const pm2_5 = [];
    const co2 = [];
    const humidity = [];
    const temperature = [];
    const voc = [];

    for (const item of this.items) {
      const time = new Date(item.time);
      pm10.push({x: time, y: item.pm10});
      pm2_5.push({x: time, y: item.pm2_5});
      co2.push({x: time, y: item.co2});
      humidity.push({x: time, y: item.humidity});
      temperature.push({x: time, y: item.temperature});
      voc.push({x: time, y: item.voc});
    }

    let series;
    switch (this.categoryIndex) {
      case INDEX_PM10:
        series = pm10;
        break;
      case INDEX_PM2_5:
        series = pm2_5;
        break;
      case INDEX_CO2:
        series = co2;
        break;
      case INDEX_HUMIDITY:
        series = humidity;
        break;
      case INDEX_TEMPERATURE:
        series = temperature;
        break;
      case INDEX_VOC:
        series = voc;
        break;
    }

    const data = [];
    for (const chunk of _.chunk(series, CHUNK_SIZE)) {
      const timeMin = _.minBy(chunk, o => o.x);
      const timeMax = _.maxBy(chunk, o => o.x);
      const dataMin = _.minBy(chunk, o => o.y);
      const dataMax = _.maxBy(chunk, o => o.y);
      data.push({x: timeMin.x, y: [dataMin.y, dataMax.y]});
    }

    this.series = [{data: data}];
    this.$refs.chart.updateSeries(this.series);
  }

  onInputPeriodStart() {
    this.showPeriodStartMenu = true;
    console.log('onInputPeriodStart');
    this.updateChart();
  }

  onInputPeriodEnd() {
    this.showPeriodEndMenu = true;
    console.log('onInputPeriodEnd');
    this.updateChart();
  }

  onChangeDevice() {
    console.log('onChangeDevice');
    this.updateChart();
  }

  onChangeCategory() {
    console.log('onChangeCategory');
    this.updateChart();
  }

  onClickRange90d() {
    const range = dateRange(90);
    this.periodStart = range[0];
    this.periodEnd = range[1];
    console.log('onClickRange90d');
    this.updateChart();
  }

  onClickRange30d() {
    const range = dateRange(30);
    this.periodStart = range[0];
    this.periodEnd = range[1];
    console.log('onClickRange30d');
    this.updateChart();
  }

  onClickRange7d() {
    const range = dateRange(7);
    this.periodStart = range[0];
    this.periodEnd = range[1];
    console.log('onClickRange7d');
    this.updateChart();
  }

  onClickRange1d() {
    const range = dateRange(1);
    this.periodStart = range[0];
    this.periodEnd = range[1];
    console.log('onClickRange1d');
    this.updateChart();
  }
}
</script>
