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
  msg:
    empty_device: "Empty device"
    empty_category: "Empty category"
    no_chart: "No device or category selected"
  range:
    d90: "90Days"
    d30: "30Days"
    d7: "1Week"
    d1: "Today"
  tooltip:
    download_csv: "Download CSV file"

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
  msg:
    empty_device: "Empty device"
    empty_category: "Empty category"
    no_chart: "장치 또는 카테고리가 선택되지 않았습니다"
  range:
    d90: "90일"
    d30: "30일"
    d7: "일주"
    d1: "오늘"
  tooltip:
    download_csv: "CSV 파일 다운로드"
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
            item-text="name"
            item-value="uid"
            return-object
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
      <v-col cols="12" sm="7">
        <div class="d-inline-flex flex-row align-center text-center">
          <v-icon
              v-if="$vuetify.breakpoint.mdAndUp"
              class="mr-2"
          >
            mdi-calendar
          </v-icon>
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

      <v-col class="d-flex flex-row align-center" cols="12" sm="5">
        <v-spacer></v-spacer>
        <v-btn-toggle
            dense
            v-model="rangeIndex"
        >
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
      <div v-else class="d-flex flex-column">
        <div class="d-flex flex-row justify-end">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                  class="mr-4"
                  elevation="4"
                  fab
                  absolute
                  small
                  icon
                  v-bind="attrs"
                  v-on="on"
                  @click="onClickDownloadCsv"
              >
                <v-icon>mdi-file-delimited</v-icon>
              </v-btn>
            </template>
            <span>{{ $t('tooltip.download_csv') }}</span>
          </v-tooltip>
        </div>

        <chart
            class="pa-2"
            type="bar"
            :chart-data="chartData"
            :options="chartOptions"
        ></chart>
      </div>
    </v-card>

  </v-container>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import Chart from '@/chart/Chart.vue';
import {
  createMoment,
  dateToString,
  todayString,
} from '@/chrono/date';
import {download} from '@/utils/download';
import type {AirjoyChartA, AirjoyDeviceA} from '@/packet/airjoy';
import {
  calcHumidity,
  calcTemperature,
  categoryIndexByName,
  categoryNameByIndex,
  getChartScaleYMax,
  INDEX_UNKNOWN,
  INDEX_PM10,
  INDEX_PM2_5,
  INDEX_CO2,
  INDEX_HUMIDITY,
  INDEX_TEMPERATURE,
  INDEX_VOC,
  printableCategoryIndexByName,
  printableCategoryNames,
  UNKNOWN_ROUTE_PARAMS_DEVICE,
} from '@/packet/airjoy';

export function dateRange(days: number) {
  const start = new Date();
  const end = new Date(Date.now());
  start.setDate(end.getDate() - days + 1);
  return [dateToString(start), dateToString(end)];
}

/**
 * For avoid type checking in typescript.
 */
function yMaxDefault(): undefined | number {
  return undefined;
}

function getCategoryData(categoryIndex: number, chart: AirjoyChartA) {
  let avg, min, max;
  switch (categoryIndex) {
    case INDEX_PM10:
      avg = chart.avg_pm10;
      min = chart.min_pm10;
      max = chart.max_pm10;
      break;
    case INDEX_PM2_5:
      avg = chart.avg_pm2_5;
      min = chart.min_pm2_5;
      max = chart.max_pm2_5;
      break;
    case INDEX_CO2:
      avg = chart.avg_co2;
      min = chart.min_co2;
      max = chart.max_co2;
      break;
    case INDEX_HUMIDITY:
      avg = calcHumidity(chart.avg_humidity);
      min = calcHumidity(chart.min_humidity);
      max = calcHumidity(chart.max_humidity);
      break;
    case INDEX_TEMPERATURE:
      avg = calcHumidity(chart.avg_temperature);
      min = calcHumidity(chart.min_temperature);
      max = calcHumidity(chart.max_temperature);
      break;
    case INDEX_VOC:
      avg = chart.avg_voc;
      min = chart.min_voc;
      max = chart.max_voc;
      break;
    default:
      avg = undefined;
      min = undefined;
      max = undefined;
      break;
  }
  return {avg: Math.round(avg), min, max};
}

function isFloating(value) {
  return /\./.test(String(value));
}

@Component({
  components: {
    Chart,
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
      text: this.$route.params.device,
      disabled: true,
    },
  ];

  readonly chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        max: yMaxDefault(),
        ticks: {
          callback: (value, index, values) => {
            if (!isFloating(value)) {
              return value;
            }
          }
        },
      }
    },
  };

  @Prop({type: Number, default: 40})
  readonly datePickerSize!: number;

  chartData = {};

  loadingDevices = false;
  device?: number | AirjoyDeviceA = -1;
  devices = [] as Array<AirjoyDeviceA>;

  category = '';
  items = {};

  showPeriodStartMenu = false;
  periodStart = todayString();

  showPeriodEndMenu = false;
  periodEnd = todayString();

  rangeIndex = -1;

  created() {
    const index = categoryIndexByName(this.$route.params.category);
    if (index !== INDEX_UNKNOWN) {
      this.category = this.categories[index];
    } else {
      this.category = this.categories[0];
    }

    this.updateDevices();
  }

  getCurrentCategoryIndex() {
    return printableCategoryIndexByName(this.category, this.$vuetify.lang.current);
  }

  get categories() {
    return printableCategoryNames(this.$vuetify.lang.current);
  }

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
          this.updateChart();
        })
        .catch(error => {
          this.loadingDevices = false;
          this.toastRequestFailure(error);
        });
  }

  getStartMoment() {
    return createMoment(this.periodStart + 'T00:00:00');
  }

  getEndMoment() {
    return createMoment(this.periodEnd + 'T23:59:59');
  }

  updateChart() {
    if (typeof this.device !== 'object') {
      return;
    }

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.device.uid;
    const begin = this.getStartMoment().format();
    const end = this.getEndMoment().format();
    const categoryIndex = this.getCurrentCategoryIndex();

    this.$api2.getAirjoyChart(group, project, device, begin, end)
        .then(items => {
          const unixTimeToChart = {};
          for (const item of items) {
            unixTimeToChart[createMoment(item.begin).unix()] = item;
          }
          this.items = unixTimeToChart;
          this.updateSeries(categoryIndex);
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  updateSeries(categoryIndex: number) {
    const isOneDay = this.periodStart === this.periodEnd;

    const totalBegin = this.getStartMoment();
    const totalEnd = this.getEndMoment();
    const diffHours = totalEnd.diff(totalBegin, 'hours');
    const diffDays = totalEnd.diff(totalBegin, 'days');
    const totalIteration = isOneDay ? diffHours : diffDays;
    const stepHours = isOneDay ? 1 : 24;

    const labels: Array<string> = [];
    const dataMinMax: Array<Array<number | undefined>> = [];
    const dataAverages: Array<number | undefined> = [];

    const cursor = this.getStartMoment();
    for (let i = 0; i <= totalIteration; ++i) {
      if (isOneDay) {
        const hourLabel = cursor.format("HH");
        labels.push(hourLabel);
      } else {
        const dayLabel = cursor.format("MM/DD");
        labels.push(dayLabel);
      }

      const chart = this.items[cursor.unix()] as AirjoyChartA | undefined;
      if (chart) {
        const {avg, min, max} = getCategoryData(categoryIndex, chart);
        dataAverages.push(avg);
        dataMinMax.push([min, max]);
      } else {
        dataMinMax.push([undefined, undefined]);
        dataAverages.push(undefined);
      }
      cursor.add(stepHours, 'hours');
    }

    const primaryTheme = this.$vuetify.theme.currentTheme.primary;
    const warningTheme = this.$vuetify.theme.currentTheme.warning;

    const barColor = primaryTheme?.toString() || 'blue';
    const lineColor = warningTheme?.toString() || 'orange';

    this.chartOptions.scales.y.max = getChartScaleYMax(categoryIndex);
    this.chartData = {
      labels: labels,
      datasets: [
        {
          label: 'Min,Max',
          backgroundColor: barColor,
          data: dataMinMax,
          order: 1,
        },
        {
          label: 'Avg',
          backgroundColor: lineColor,
          data: dataAverages,
          type: 'line',
          order: 0,
        },
      ],
    };
  }

  onInputPeriodStart() {
    this.showPeriodStartMenu = true;
    this.rangeIndex = -1;
    this.updateChart();
  }

  onInputPeriodEnd() {
    this.showPeriodEndMenu = true;
    this.rangeIndex = -1;
    this.updateChart();
  }

  onChangeDevice() {
    this.updateChart();
  }

  onChangeCategory() {
    const index = this.getCurrentCategoryIndex();
    this.updateSeries(index);
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

  toCsvData() {
    if (!this.chartData.hasOwnProperty('labels')) {
      throw Error('no labels');
    }
    if (!this.chartData.hasOwnProperty('datasets')) {
      throw Error('no datasets');
    }

    const labels = this.chartData['labels'];
    const dataMinMax = this.chartData['datasets'][0].data;
    const dataAverage = this.chartData['datasets'][0].data;
    const lines = [] as Array<string>;
    for (let i = 0; i < labels.length; ++i) {
      const min = dataMinMax[i][0];
      const max = dataMinMax[i][1];
      const avg = dataAverage[i];
      lines.push(`${labels[i]},${min},${max},${avg}`);
    }
    return lines.join('\n');
  }

  downloadChartCsv() {
    const filename = `chart-${this.periodStart}_${this.periodEnd}.csv`;
    const mime = 'text/csv';
    download(this.toCsvData(), filename, mime);
  }

  onClickDownloadCsv() {
    if (typeof this.device !== 'object') {
      return;
    }

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.device.uid;
    const begin = this.getStartMoment().format();
    const end = this.getEndMoment().format();

    this.$api2.getAirjoyChartCsv(group, project, device, begin, end)
        .then(data => {
          const filename = `chart-${this.periodStart}_${this.periodEnd}.csv`;
          const mime = 'text/csv';
          download(data, filename, mime);
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }
}
</script>
