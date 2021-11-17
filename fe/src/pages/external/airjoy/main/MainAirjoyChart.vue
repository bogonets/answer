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
import {dateToString, todayString, yesterdayString} from '@/chrono/date';
import {download} from '@/utils/download';
import type {AirjoyChartA, AirjoyDeviceA} from '@/packet/airjoy';
import {
  calcHumidity,
  calcTemperature,
  categoryIndexByName,
  categoryNameByIndex,
  getChartScaleYMax,
  INDEX_HUMIDITY,
  INDEX_TEMPERATURE,
  INDEX_UNKNOWN,
  INDEX_VOC,
  printableCategoryIndexByName,
  printableCategoryNames,
  UNKNOWN_ROUTE_PARAMS_DEVICE,
} from '@/packet/airjoy';

export function dateRange(days: number) {
  const end = new Date(Date.now());
  const start = new Date();
  start.setDate(end.getDate() - days);
  return [dateToString(start), dateToString(end)];
}

/**
 * For avoid type checking in typescript.
 */
function yMaxDefault(): undefined | number {
  return undefined;
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

  showPeriodStartMenu = false;
  periodStart = yesterdayString();

  showPeriodEndMenu = false;
  periodEnd = todayString();

  rangeIndex = -1;

  period = '';

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

  updateChart() {
    if (typeof this.device !== 'object') {
      return;
    }

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.device.uid;
    const start = this.periodStart;
    const end = this.periodEnd;
    const categoryIndex = this.getCurrentCategoryIndex();
    const category = categoryNameByIndex(categoryIndex);

    this.chartOptions.scales.y.max = getChartScaleYMax(categoryIndex);
    this.$api2.getAirjoyChart(group, project, device, start, end, category)
        .then(items => {
          this.updateSeries(categoryIndex, items);
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  updateSeries(categoryIndex: number, items: Array<AirjoyChartA>) {
    const labels: Array<string> = [];
    const data: Array<Array<number>> = [];
    for (const item of items) {
      labels.push(item.bucket)

      if (categoryIndex == INDEX_HUMIDITY) {
        const min = calcHumidity(item.min);
        const max = calcHumidity(item.max);
        data.push([min, max]);
      } else if (categoryIndex == INDEX_TEMPERATURE) {
        const min = calcTemperature(item.min);
        const max = calcTemperature(item.max);
        data.push([min, max]);
      } else {
        data.push([item.min, item.max]);
      }
    }

    const background = this.$vuetify.theme.currentTheme.primary?.toString() || 'blue';
    this.chartData = {
      labels: labels,
      datasets: [
        {
          label: this.category,
          backgroundColor: background,
          data: data,
        }
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

  toCsvData() {
    if (!this.chartData.hasOwnProperty('labels')) {
      throw Error('no labels');
    }
    if (!this.chartData.hasOwnProperty('datasets')) {
      throw Error('no datasets');
    }

    const labels = this.chartData['labels'];
    const data = this.chartData['datasets'][0].data;
    const lines = [] as Array<string>;
    for (let i = 0; i < labels.length; ++i) {
      lines.push(`${labels[i]},${data[i][0]},${data[i][1]}`);
    }
    return lines.join('\n');
  }

  onClickDownloadCsv() {
    download(this.toCsvData(), `chart-${todayString()}`, 'text/csv');
  }
}
</script>
