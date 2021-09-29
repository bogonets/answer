<i18n lang="yaml">
en:
  title: "Airjoy Device Live Viewer"
  groups: "Groups"
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

ko:
  title: "AIRJOY 실시간 모니터링"
  groups: "Groups"
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
</i18n>

<template>
  <v-container>
    <breadcrumb-main name="Live"></breadcrumb-main>
    <v-divider></v-divider>

    <v-row class="my-4">
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

    <v-card class="mt-4 pt-4">
      <div class="mb-2 text--primary text-subtitle-2 text-center">
        {{ $t('title') }}
      </div>
      <chart
          type="line"
          :chart-data="chartData"
          :options="chartOptions"
      ></chart>
      <v-spacer class="py-4"></v-spacer>
    </v-card>

    <v-row class="mt-1" align="center" justify="center">
      <v-btn elevation="4" fab absolute :color="playColor" @click="onClickPlay">
        <v-icon>{{ playIcon }}</v-icon>
      </v-btn>
    </v-row>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import Chart from '@/chart/Chart.vue';
import {Chart as ChartJS} from 'chart.js';
import type {AirjoyDeviceA, AirjoySensorA} from '@/packet/airjoy';
import {
  INDEX_UNKNOWN,
  INDEX_PM10,
  INDEX_PM2_5,
  INDEX_CO2,
  INDEX_HUMIDITY,
  INDEX_TEMPERATURE,
  INDEX_VOC,
  categoryIndexByName,
  printableCategoryNames,
  printableCategoryIndexByName,
  calcTemperature,
  calcHumidity,
} from '@/packet/airjoy';
import * as _ from 'lodash';

const UPDATE_INTERVAL_MILLISECONDS = 1000;
const STREAMING_FRAME_RATE = 30;

@Component({
  components: {
    BreadcrumbMain,
    Chart,
  }
})
export default class MainAirjoyLive extends VueBase {
  chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom',
      },
      streaming: {
        pause: false,
        frameRate: STREAMING_FRAME_RATE,
      },
    },
    scales: {
      x: {
        type: 'realtime',
        realtime: {
          onRefresh: this.onChartRefresh,
        }
      },
      y: {
        min: 0
      },
    }
  };

  loadingDevices = false;

  originalChartData = {};
  chartData = {};

  category = '';

  intervalHandle = -1;
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

  mounted() {
    this.intervalHandle = window.setInterval(() => {
      if (!this.isPause()) {
        this.updateChart();
      }
    }, UPDATE_INTERVAL_MILLISECONDS);
  }

  beforeDestroy() {
    if (this.intervalHandle != -1) {
      window.clearInterval(this.intervalHandle);
      this.intervalHandle = -1;
    }
  }

  isPause() {
    return this.chartOptions.plugins.streaming.pause;
  }

  get categories() {
    return printableCategoryNames(this.$vuetify.lang.current);
  }

  get playColor() {
    if (this.isPause()) {
      return 'primary';
    } else {
      return 'primary';
    }
  }

  get playIcon() {
    if (this.isPause()) {
      return 'mdi-play';
    } else {
      return 'mdi-pause';
    }
  }

  updateDevices() {
    this.loadingDevices = true;
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.$api2.getAirjoyDevices(group, project)
        .then(items => {
          this.loadingDevices = false;
          this.updateChartData(items);
        })
        .catch(error => {
          this.loadingDevices = false;
          this.toastRequestFailure(error);
        });
  }

  updateChartData(items: Array<AirjoyDeviceA>) {
    const background = this.$vuetify.theme.currentTheme.primary?.toString() || 'blue';
    const chartData = {
      datasets: [] as Array<object>
    };

    for (const item of items) {
      const name = item.name.toString();
      const uid = item.uid.toString();
      const label = name ? name : uid;
      chartData.datasets.push({
        label: label,
        backgroundColor: background,
        data: [],
      });
    }

    this.originalChartData = chartData;
    this.chartData = _.cloneDeep(this.originalChartData);
  }

  updateChart() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.$api2.getAirjoyLive(group, project)
        .then(items => {
          this.items = items;
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  getSensorValue(item: AirjoySensorA) {
    const lang = this.$vuetify.lang.current;
    const index = printableCategoryIndexByName(this.category, lang);
    switch (index) {
      case INDEX_PM10:
        return item.pm10;
      case INDEX_PM2_5:
        return item.pm2_5;
      case INDEX_CO2:
        return item.pm2_5;
      case INDEX_HUMIDITY:
        return calcHumidity(item.humidity);
      case INDEX_TEMPERATURE:
        return calcTemperature(item.temperature);
      case INDEX_VOC:
        return item.voc;
      default:
        return 0;
    }
  }

  onChartRefresh(chart: ChartJS) {
    for (const item of this.items) {
      const name = item.name.toString();
      const uid = item.uid.toString();
      const label = name ? name : uid;
      const value = this.getSensorValue(item);
      const data = {x: Date.now(), y: value};

      const dataset = chart.data.datasets.find(dataset => dataset.label == label);
      if (typeof dataset !== 'undefined') {
        dataset.data.push(data);
      }
    }
  }

  onChangeCategory(value) {
    console.assert(value == this.category);
    this.chartData = _.cloneDeep(this.originalChartData);
  }

  onClickPlay() {
    const pause = this.chartOptions.plugins.streaming.pause;
    this.chartOptions.plugins.streaming.pause = !pause;
  }
}
</script>
