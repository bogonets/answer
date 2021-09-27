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
    no_chart: "No device or category selected"
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
    no_chart: "장치 또는 카테고리가 선택되지 않았습니다"
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

    <v-card class="my-4 py-4">
      <div v-if="noChart" class="d-flex flex-column align-center">
        <v-icon x-large>
          mdi-chart-bar
        </v-icon>
        <div class="text--secondary text-subtitle-1 text-center">
          {{ $t('msg.no_chart') }}
        </div>
      </div>
      <bar-chart v-else :chart-data="chartData"></bar-chart>
    </v-card>

  </v-container>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import BarChart from '@/components/chart/BarChart.vue'
import type {AirjoyDeviceA, AirjoySensorA} from '@/packet/airjoy';
import {
  UNKNOWN_ROUTE_PARAMS_DEVICE,
  INDEX_UNKNOWN,
  categoryIndexByName,
  printableCategoryNames,
} from '@/packet/airjoy';
import {dateToString, todayString, yesterdayString} from '@/chrono/date';

export function dateRange(days: number) {
  const end = new Date(Date.now());
  const start = new Date();
  start.setDate(end.getDate() - days);
  return [dateToString(start), dateToString(end)];
}

function getRandomInt() {
  return Math.floor(Math.random() * (50 - 5 + 1)) + 5
}

@Component({
  components: {
    BarChart,
    ToolbarBreadcrumbs,
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

  chartData = {
    labels: [getRandomInt(), getRandomInt()],
    datasets: [
      {
        label: 'Data One',
        backgroundColor: '#f87979',
        data: [getRandomInt(), getRandomInt()]
      }, {
        label: 'Data One',
        backgroundColor: '#f87979',
        data: [getRandomInt(), getRandomInt()]
      }
    ]
  };

  @Prop({type: Number, default: 40})
  readonly datePickerSize!: number;

  loadingDevices = false;
  device?: number | AirjoyDeviceA = -1;
  devices = [] as Array<AirjoyDeviceA>;

  showPeriodStartMenu = false;
  periodStart = yesterdayString();

  showPeriodEndMenu = false;
  periodEnd = todayString();

  category = '';

  loading = false;
  items = [] as Array<AirjoySensorA>;

  created() {
    const index = categoryIndexByName(this.$route.params.category);
    if (index !== INDEX_UNKNOWN) {
      this.category = this.categories[index];
    } else {
      this.category = this.categories[0];
    }

    this.updateDevices();
  }

  get categories() {
    return printableCategoryNames(this.$vuetify.lang.current);
  }

  // get categoryIndex() {
  //   return this.categories.findIndex(i => i === this.category);
  // }

  get noChart() {
    return typeof this.device !== 'object' || !this.category;
  }

  get selectedAirjoyUid() {
    if (this.$route.params.device !== UNKNOWN_ROUTE_PARAMS_DEVICE) {
      return Number.parseInt(this.$route.params.device);
    }
    return undefined;
  }

  updateDevices() {
    this.loadingDevices = true;
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.$api2.getAirjoyDevices(group, project)
        .then(items => {
          this.loadingDevices = false;
          this.devices = items;
          if (typeof this.selectedAirjoyUid !== 'undefined') {
            this.device = this.devices.find(i => i.uid === this.selectedAirjoyUid);
          } else {
            this.device = undefined;
          }
        })
        .catch(error => {
          this.loadingDevices = false;
          this.toastRequestFailure(error);
        });
  }

  updateChart() {
    if (typeof this.device !== 'object') {
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
    // const pm10 = [];
    // const pm2_5 = [];
    // const co2 = [];
    // const humidity = [];
    // const temperature = [];
    // const voc = [];
    //
    // for (const item of this.items) {
    //   const time = new Date(item.time);
    //   pm10.push({x: time, y: item.pm10});
    //   pm2_5.push({x: time, y: item.pm2_5});
    //   co2.push({x: time, y: item.co2});
    //   humidity.push({x: time, y: item.humidity});
    //   temperature.push({x: time, y: item.temperature});
    //   voc.push({x: time, y: item.voc});
    // }
    //
    // let series;
    // switch (this.categoryIndex) {
    //   case INDEX_PM10:
    //     series = pm10;
    //     break;
    //   case INDEX_PM2_5:
    //     series = pm2_5;
    //     break;
    //   case INDEX_CO2:
    //     series = co2;
    //     break;
    //   case INDEX_HUMIDITY:
    //     series = humidity;
    //     break;
    //   case INDEX_TEMPERATURE:
    //     series = temperature;
    //     break;
    //   case INDEX_VOC:
    //     series = voc;
    //     break;
    // }
    //
    // const data = [];
    // for (const chunk of _.chunk(series, CHUNK_SIZE)) {
    //   const timeMin = _.minBy(chunk, o => o.x);
    //   const timeMax = _.maxBy(chunk, o => o.x);
    //   const dataMin = _.minBy(chunk, o => o.y);
    //   const dataMax = _.maxBy(chunk, o => o.y);
    //   data.push({x: timeMin.x, y: [dataMin.y, dataMax.y]});
    // }
    //
    // this.series = [{data: data}];
    // this.$refs.chart.updateSeries(this.series);
  }

  onInputPeriodStart() {
    this.showPeriodStartMenu = true;
    this.updateChart();
  }

  onInputPeriodEnd() {
    this.showPeriodEndMenu = true;
    this.updateChart();
  }

  onChangeDevice() {
    this.updateChart();
  }

  onChangeCategory() {
    this.updateChart();
  }

  onClickRange90d() {
    const range = dateRange(90);
    this.periodStart = range[0];
    this.periodEnd = range[1];
    this.updateChart();
  }

  onClickRange30d() {
    const range = dateRange(30);
    this.periodStart = range[0];
    this.periodEnd = range[1];
    this.updateChart();
  }

  onClickRange7d() {
    const range = dateRange(7);
    this.periodStart = range[0];
    this.periodEnd = range[1];
    this.updateChart();
  }

  onClickRange1d() {
    const range = dateRange(1);
    this.periodStart = range[0];
    this.periodEnd = range[1];
    this.updateChart();
  }
}
</script>
