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
            :items="devices"
            :label="$t('labels.device')"
        ></v-select>
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
          <v-btn>
            3M
          </v-btn>
          <v-btn>
            1M
          </v-btn>
          <v-btn>
            1W
          </v-btn>
          <v-btn>
            TODAY
          </v-btn>
        </v-btn-toggle>
      </v-col>
    </v-row>

    <v-card class="mt-4 pt-4">
      <vue-apex-charts
          class="mx-2"
          type="candlestick"
          height="350"
          ref="chart"
          :options="chartOptions"
          :series="series">
      </vue-apex-charts>
      <v-spacer class="py-4"></v-spacer>
    </v-card>

  </v-container>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import VueApexCharts from 'vue-apexcharts';
import {
  CATEGORY_PM10,
  CATEGORY_PM2_5,
  CATEGORY_CO2,
  CATEGORY_HUMIDITY,
  CATEGORY_TEMPERATURE,
  CATEGORY_VOC,
} from '@/packet/airjoy';

export function today() {
  const now = new Date(Date.now());
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const day = now.getDate();
  const yearText = `${year}`.padStart(4, '0');
  const monthText = `${month}`.padStart(2, '0');
  const dayText = `${day}`.padStart(2, '0');
  return `${yearText}-${monthText}-${dayText}`;
}

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
      type: 'candlestick',
    },
    title: {
      text: 'CandleStick Chart - Category X-axis',
      align: 'left'
    },
    tooltip: {
      enabled: true,
    },
    xaxis: {
      type: 'category',
      labels: {
        formatter: function(val) {
          const n = Date.parse(val)
          const d = new Date(n);
          const s = d.toLocaleString();
          return s;
        }
      }
    },
    yaxis: {
      tooltip: {
        enabled: true
      }
    }
  };

  series = [{
    name: 'candle',
    data: [
      {
        x: new Date(1538857800000),
        y: [6593.86, 6604.28, 6586.57, 6600.01]
      },
      {
        x: new Date(1538859600000),
        y: [6601.81, 6603.21, 6592.78, 6596.25]
      },
      {
        x: new Date(1538861400000),
        y: [6596.25, 6604.2, 6590, 6602.99]
      },
      {
        x: new Date(1538863200000),
        y: [6602.99, 6606, 6584.99, 6587.81]
      },
      {
        x: new Date(1538865000000),
        y: [6587.81, 6595, 6583.27, 6591.96]
      },
      {
        x: new Date(1538866800000),
        y: [6591.97, 6596.07, 6585, 6588.39]
      },
      {
        x: new Date(1538868600000),
        y: [6587.6, 6598.21, 6587.6, 6594.27]
      },
      {
        x: new Date(1538870400000),
        y: [6596.44, 6601, 6590, 6596.55]
      },
      {
        x: new Date(1538872200000),
        y: [6598.91, 6605, 6596.61, 6600.02]
      },
      {
        x: new Date(1538874000000),
        y: [6600.55, 6605, 6589.14, 6593.01]
      },
      {
        x: new Date(1538875800000),
        y: [6593.15, 6605, 6592, 6603.06]
      },
      {
        x: new Date(1538877600000),
        y: [6603.07, 6604.5, 6599.09, 6603.89]
      },
      {
        x: new Date(1538879400000),
        y: [6604.44, 6604.44, 6600, 6603.5]
      },
      {
        x: new Date(1538881200000),
        y: [6603.5, 6603.99, 6597.5, 6603.86]
      },
      {
        x: new Date(1538883000000),
        y: [6603.85, 6605, 6600, 6604.07]
      },
      {
        x: new Date(1538884800000),
        y: [6604.98, 6606, 6604.07, 6606]
      },
    ]
  }];

  @Prop({type: Number, default: 40})
  readonly datePickerSize!: number;

  device = '';
  devices = ['100', '200', '300', '400']

  showPeriodStartMenu = false;
  periodStart = today();

  showPeriodEndMenu = false;
  periodEnd = today();

  category = '';

  created() {
    const device = this.$route.params.airjoy;
    const deviceIndex = this.devices.indexOf(device);
    if (deviceIndex !== -1) {
      this.device = device;
    }

    const index = this.getCategoryIndex(this.$route.params.category);
    if (index !== -1) {
      this.category = this.categories[index];
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

  onInputPeriodStart() {
    this.showPeriodStartMenu = true;
  }

  onInputPeriodEnd() {
    this.showPeriodEndMenu = true;
  }
}
</script>
