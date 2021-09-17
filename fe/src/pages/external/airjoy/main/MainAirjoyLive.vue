<i18n lang="yaml">
en:
  title: "Airjoy Device Live Viewer"
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

ko:
  title: "Airjoy Device Live Viewer"
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
      <v-btn elevation="4" fab absolute color="primary">
        <v-icon>mdi-play</v-icon>
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
import {
  CATEGORY_CO2,
  CATEGORY_HUMIDITY,
  CATEGORY_PM10,
  CATEGORY_PM2_5,
  CATEGORY_TEMPERATURE,
  CATEGORY_VOC,
} from "@/packet/airjoy";

export function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min; //최댓값은 제외, 최솟값은 포함
}

@Component({
  components: {
    BreadcrumbMain,
    VueApexCharts,
  }
})
export default class MainAirjoyLive extends VueBase {
  select = ''
  items = ['a', 'b', 'c']

  readonly chartOptions = {
    theme: {
      mode: this.$vuetify.theme.dark ? 'dark' : 'light',
    },
    chart: {
      id: 'chart',
      type: 'line',
      animations: {
        enabled: true,
        easing: 'linear',
        dynamicAnimation: {
          speed: 1000
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
      categories: ['01/01/2003', '02/01/2003','03/01/2003','04/01/2003','05/01/2003','06/01/2003','07/01/2003','08/01/2003'],
    },
    yaxis: {
      max: 100
    },
    legend: {
      show: true
    },
  };

  series = [{
    name: '단말기',
    data: [30, 40, 45, 50, 49, 60, 70, 91]
  }, {
    name: '200',
    data: [23, 43, 54, 12, 44, 52, 32, 11]
  }];

  category = '';

  created() {
    const index = this.getCategoryIndex(this.$route.params.category);
    if (index !== -1) {
      this.category = this.categories[index];
    } else {
      this.category = this.categories[0];
    }


    // ApexCharts.exec('chart', 'updateSeries', [{
    // }], true);

    // setInterval(() => {
    //   this.series[0].data.push(getRandomInt(1, 99));
    //   this.series[1].data.push(getRandomInt(1, 99));
    //   this.$refs.chart.updateSeries(this.series);
    // }, 1000);

    // var me = this
    //       window.setInterval(function () {
    //         getNewSeries(lastDate, {
    //           min: 10,
    //           max: 90
    //         })
    //
    //       }, 1000)
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

  getCategoryIndex(name: string) {
    if (name === CATEGORY_PM10) {
      return 0;
    } else if (name === CATEGORY_PM2_5) {
      return 1;
    } else if (name === CATEGORY_CO2) {
      return 2;
    } else if (name === CATEGORY_HUMIDITY) {
      return 3;
    } else if (name === CATEGORY_TEMPERATURE) {
      return 4;
    } else if (name === CATEGORY_VOC) {
      return 5;
    } else {
      return -1;
    }
  }

  // series = [];
  //
  // chartOptions = {
  //   chart: {
  //     id: 'realtime',
  //     height: 350,
  //     type: 'line',
  //     animations: {
  //       enabled: true,
  //       easing: 'linear',
  //       dynamicAnimation: {
  //         speed: 1000
  //       }
  //     },
  //     toolbar: {
  //       show: false
  //     },
  //     zoom: {
  //       enabled: false
  //     }
  //   },
  //   dataLabels: {
  //     enabled: false
  //   },
  //   stroke: {
  //     curve: 'smooth'
  //   },
  //   title: {
  //     text: 'Dynamic Updating Chart',
  //     align: 'left'
  //   },
  //   markers: {
  //     size: 0
  //   },
  //   xaxis: {
  //     type: 'datetime',
  //   },
  //   yaxis: {
  //     max: 100
  //   },
  //   legend: {
  //     show: false
  //   },
  // };

  mounted() {
    // window.setInterval(() => {
    //   getNewSeries(lastDate, {
    //     min: 10,
    //     max: 90
    //   })
    //
    //   this.$refs.chart.updateSeries([{
    //     data: data
    //   }])
    // }, 1000);
    //
    // // every 60 seconds, we reset the data to prevent memory leaks
    // window.setInterval(function () {
    //   this.$refs.chart.updateSeries([{
    //     this.data
    //   }], false, true)
    // }, 60000)
  }

  generateDayWiseTimeSeries(baseval, count, yrange) {
    // let i = 0;
    // let series = [];
    // while (i < count) {
    //   let x = baseval;
    //   let y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
    //   series.push([x, y]);
    //   baseval += 86400000;
    //   i++;
    // }
    // return series;
  }

  updateChart() {
    // const series = [
    //   {
    //     name: 'South',
    //     data: this.generateDayWiseTimeSeries(new Date('11 Feb 2017').getTime(), 20, {
    //       min: 10,
    //       max: 60
    //     })
    //   },
    //   {
    //     name: 'North',
    //     data: this.generateDayWiseTimeSeries(new Date('11 Feb 2017').getTime(), 20, {
    //       min: 10,
    //       max: 20
    //     })
    //   },
    //   {
    //     name: 'Central',
    //     data: this.generateDayWiseTimeSeries(new Date('11 Feb 2017').getTime(), 20, {
    //       min: 10,
    //       max: 15
    //     })
    //   }
    // ]
    // this.series = series
  }
}
</script>
