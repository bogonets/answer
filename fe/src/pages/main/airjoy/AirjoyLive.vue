<template>
  <v-container>
    <breadcrumb-main name="Live"></breadcrumb-main>
    <v-divider></v-divider>

    <v-card class="mt-4 pt-4">
      <div class="mb-2 text--primary text-subtitle-2 text-center">
        {{ 'Title' }}
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

    <v-row>
      <v-col class="pb-0" cols="12">
        <v-select
            multiple
            small-chips
            deletable-chips
            clearable
            persistent-hint
            v-model="select"
            :items="items"
            label="I use chips"
            hint="Select ships"
        ></v-select>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-select
            small-chips
            deletable-chips
            clearable
            persistent-hint
            v-model="select"
            :items="items"
            label="I use chips"
            hint="Select ships"
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

@Component({
  components: {
    BreadcrumbMain,
    VueApexCharts,
  }
})
export default class AirjoyLive extends VueBase {
  select = ''
  items = ['a', 'b', 'c']

  readonly chartOptions = {
    theme: {
      mode: this.$vuetify.theme.dark ? 'dark' : 'light',
    },
    chart: {
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
    name: 'Series A',
    data: [30, 40, 45, 50, 49, 60, 70, 91]
  }, {
    name: 'Series B',
    data: [23, 43, 54, 12, 44, 52, 32, 11]
  }];

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
