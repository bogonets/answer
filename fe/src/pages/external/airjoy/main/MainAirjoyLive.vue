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

    <v-card class="mt-4 pt-4">
      <div class="mb-2 text--primary text-subtitle-2 text-center">
        {{ $t('title') }}
      </div>
      <vue-apex-charts
          type="line"
          height="350"
          ref="chart"
          :options="chartOptions"
          :series="series">
      </vue-apex-charts>
      <v-spacer class="py-4"></v-spacer>
    </v-card>

    <v-row class="mt-1" align="center" justify="center">
      <v-btn elevation="4" fab absolute :color="playColor" @click="onClickPlay">
        <v-icon>{{ playIcon }}</v-icon>
      </v-btn>
    </v-row>

    <v-row class="mt-12">
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

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import VueApexCharts from 'vue-apexcharts';
import type {AirjoySensorA} from '@/packet/airjoy';
import {
  CATEGORY_CO2,
  CATEGORY_HUMIDITY,
  CATEGORY_PM10,
  CATEGORY_PM2_5,
  CATEGORY_TEMPERATURE,
  CATEGORY_VOC,
} from '@/packet/airjoy';

const INDEX_PM10 = 0;
const INDEX_PM2_5 = 1;
const INDEX_CO2 = 2;
const INDEX_HUMIDITY = 3;
const INDEX_TEMPERATURE = 4;
const INDEX_VOC = 5;

export function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //최댓값은 제외, 최솟값은 포함
}

const UPDATE_INTERVAL_MILLISECONDS = 1000;
const Y_AXIS_COUNTER = 10;
const Y_AXIS_RANGE = UPDATE_INTERVAL_MILLISECONDS * Y_AXIS_COUNTER;
const MAX_SERIES = 1000;

@Component({
  components: {
    BreadcrumbMain,
    VueApexCharts,
  }
})
export default class MainAirjoyLive extends VueBase {
  chartOptions = {
    theme: {
      mode: this.$vuetify.theme.dark ? 'dark' : 'light',
    },
    chart: {
      id: 'realtime',
      type: 'line',
      animations: {
        enabled: true,
        easing: 'linear',
        dynamicAnimation: {
          speed: UPDATE_INTERVAL_MILLISECONDS,
        }
      },
      toolbar: {
        show: false
      },
      zoom: {
        enabled: false
      }
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth'
    },
    xaxis: {
      type: 'datetime',
      range: Y_AXIS_RANGE,
    },
    yaxis: {
    },
    legend: {
      show: true
    },
  };

  series = [];
  // series = [{
  //   name: '',
  //   data: [
  //     {x: new Date(Date.now()), y: 0}
  //   ]
  // }];

  play = true;
  category = '';

  intervalHandle = -1;

  created() {
    const index = this.getCategoryIndexByEnum(this.$route.params.category);
    if (index !== -1) {
      this.category = this.categories[index];
    } else {
      this.category = this.categories[0];
    }
  }

  mounted() {
    this.intervalHandle = window.setInterval(() => {
      if (this.play) {
        this.updateChart();
      }

      // this.series[0].data.push({x: new Date(Date.now()), y: getRandomInt(0, 100)})
      // if (this.series[0].data.length > 100) {
      //   this.series[0].data.splice(0, this.series[0].data.length);
      // }
      // // this.$refs.chart.updateSeries([{data: this.series[0].data}])
      // this.$refs.chart.updateSeries(this.series);
    }, UPDATE_INTERVAL_MILLISECONDS);
  }

  beforeDestroy() {
    if (this.intervalHandle != -1) {
      window.clearInterval(this.intervalHandle);
      this.intervalHandle = -1;
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

  get playColor() {
    if (this.play) {
      return 'primary';
    } else {
      return 'error';
    }
  }


  get playIcon() {
    if (this.play) {
      return 'mdi-play';
    } else {
      return 'mdi-pause';
    }
  }

  updateChart() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.$api2.getAirjoyLive(group, project)
        .then(items => {
          this.updateSeries(items);
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  updateSeries(items: Array<AirjoySensorA>) {
    for (const item of items) {
      const name = item.uid.toString();

      // const time = new Date(item.time);
      const now = new Date(Date.now());
      const offset = now.getTimezoneOffset() * 60 * 1000;
      const time = new Date(Date.now() - offset);

      let value;
      switch (this.categoryIndex) {
        case INDEX_PM10:
          value = item.pm10;
          break;
        case INDEX_PM2_5:
          value = item.pm2_5;
          break;
        case INDEX_CO2:
          value = item.co2;
          break;
        case INDEX_HUMIDITY:
          value = item.humidity;
          break;
        case INDEX_TEMPERATURE:
          value = item.temperature;
          break;
        case INDEX_VOC:
          value = item.voc;
          break;
      }

      const series = this.series.find(i => i.name === name);
      if (typeof series === 'undefined') {
        this.series.push({name: name, data: [{x: time, y: value}]});
      } else {
        series.data.push({x: time, y: value});
      }
    }

    if (this.series[0].data.length >= MAX_SERIES) {
      this.series = [];
    }

    this.$refs.chart.updateSeries(this.series);
  }

  onChangeCategory(value) {
    console.assert(value == this.category);
    this.series = [];
  }

  onClickPlay() {
    this.play = !this.play;
  }
}
</script>
