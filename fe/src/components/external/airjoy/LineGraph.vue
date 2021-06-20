<template>
  <div class="blue-box">
    <v-container class="container" :style="this.$backgroundColor()" fluid>
      <v-row>
        <v-col cols="6" align="center" justify="center">
          <v-autocomplete
            prepend-inner-icon="fas fa-search"
            :label="$t('agency_name')"
            v-model="agency"
            :items="agencyList"
            item-text="name"
            outlined
            dense
            hide-details
          ></v-autocomplete>
        </v-col>
        <v-col cols="6" align="center" justify="center">
          <v-radio-group v-model="graphType" hide-details row class="ma-0 pa-0">
            <v-radio :label="$t('term')"></v-radio>
            <v-radio :label="$t('live')"></v-radio>
          </v-radio-group>
        </v-col>
      </v-row>
      <div v-if="graphType == 0">
        <v-row justify="center">
          <v-col cols="6">
            <v-menu
              v-model="startPicker"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              min-width="auto"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="startDate"
                  :label="$t('start_date')"
                  readonly
                  outlined
                  dense
                  v-bind="attrs"
                  v-on="on"
                  hide-details=""
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="startDate"
                :date-format="(date) => new date(date).toDateString()"
                :max="endDate"
                @input="startPicker = false"
                :locale="this.$vuetify.lang.current"
              ></v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="6">
            <v-menu
              v-model="endPicker"
              :close-on-content-click="false"
              :nudge-right="40"
              transition="scale-transition"
              min-width="auto"
              class="blue-box"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="endDate"
                  :label="$t('end_date')"
                  readonly
                  outlined
                  dense
                  v-bind="attrs"
                  v-on="on"
                  hide-details=""
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="endDate"
                :min="startDate"
                :max="nowDate"
                @input="endPicker = false"
                :locale="this.$vuetify.lang.current"
              ></v-date-picker>
            </v-menu>
          </v-col>
        </v-row>
        <v-row class="blue-box">
          <v-col xl="6" lg="6" md="6" sm="12" xs="12">
            <v-btn class="mr-2 mt-1" width="70" @click="setStartDate(1)">{{
              $t("one_day")
            }}</v-btn>
            <v-btn class="mr-2 mt-1" width="70" @click="setStartDate(7)">{{
              $t("one_week")
            }}</v-btn>
            <v-btn class="mr-2 mt-1" width="70" @click="setStartDate(30)">{{
              $t("one_month")
            }}</v-btn>
            <v-btn class="mt-1" width="70" @click="setStartDate(180)"
              >{{ $t("six_month") }}
            </v-btn>
          </v-col>
          <v-col xl="6" lg="6" md="6" sm="12" xs="12">
            <v-btn :disabled="!isAgency()" @click="setGraphDataTerm()">
              {{ $t("search") }}
            </v-btn>
          </v-col>
        </v-row>
      </div>
      <div v-else>
        <v-row>
          <v-col cols="6">
            <v-btn class="ma-1" @click="initChartData()">{{
              $t("initialize")
            }}</v-btn>
            <v-btn class="ma-1" :disabled="!isAgency()" @click="graphSet()">{{
              buttonString
            }}</v-btn>
          </v-col>
        </v-row>
      </div>
      <v-row>
        <div :style="graphStyles()">
          <graph
            :chart-data="chartData"
            :options="chartOptions"
            :styles="chartStyles"
          />
        </div>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch, Prop } from "vue-property-decorator";
import Graph from "./Graph.vue";
import Chart from "chart.js";
import "chartjs-plugin-colorschemes";
import axios from "axios";

export interface Data {
  label: string;
  data: Array<any>;
}

export interface Value {
  x: Date;
  y: number;
}

@Component({
  components: {
    Graph,
  },
})
export default class LineGraph extends Vue {
  @Prop({ default: "60vh" }) readonly graphHeight!: string;

  private BASE_URL = this.$api.getUrl();
  private TIMEOUT = 3000;

  private allData: Data[] = [];
  private agencyList = [];
  private agency = "";

  private startDate = new Date().toISOString().substr(0, 10);
  private endDate = new Date().toISOString().substr(0, 10);
  private nowDate = new Date().toISOString().substr(0, 10);
  private startPicker = false;
  private endPicker = false;

  private graphType = 0;
  private playGraph = false;
  private buttonString!: string;

  private datasetLength = 10;

  /**
   * Data for chart
   */
  private chartData: Chart.ChartData = {};
  private chartOptions: Chart.ChartOptions = {};
  /**
   * chart style
   */
  public chartStyles = {
    height: "100%",
    width: "100%",
    // margin: "auto",
  };

  private graphStyles() {
    return {
      height: `${this.graphHeight}`,
      width: `90vw`,
      margin: `auto`,
    };
  }

  private startInterval!: any;
  windowWidth = window.innerWidth;

  private isAgency() {
    if (this.agency.length > 0) {
      return true;
    } else {
      return false;
    }
  }

  private start() {
    this.startInterval = setInterval(() => {
      this.setGraphDataLive();
    }, 1000);
  }
  private stop() {
    clearInterval(this.startInterval);
    this.startInterval = undefined;
  }

  created() {
    this.setAgencyList();
  }

  /**
   * mounted
   */
  mounted() {
    this.initChartOptions();
    this.initChartData();

    // this.$nextTick(function() {
    //   window.addEventListener("resize", () => {
    //     this.getWidth();
    //   });
    // });
  }

  initChartData() {
    var emptyLabels = Array();
    for (var i = 0; i < this.datasetLength; i++) {
      emptyLabels.push("00:00:00");
    }

    this.chartData = {
      labels: emptyLabels,
      datasets: this.getEmptyDatasets(),
    };

    // Term Data & Live Data Change
    this.startInterval = undefined;
    this.buttonString = this.$t("start") as string;
    this.playGraph = false;
  }

  getEmptyDatasets() {
    this.allData = [
      { label: "온도", data: this.getZeroDatas() },
      { label: "습도", data: this.getZeroDatas() },
      { label: "PM10", data: this.getZeroDatas() },
      { label: "PM2.5", data: this.getZeroDatas() },
      { label: "CO2", data: this.getZeroDatas() },
      { label: "VOC", data: this.getZeroDatas() },
    ];
    return this.allData;
  }

  getZeroDatas() {
    var datas = Array();
    for (var i = 0; i < this.datasetLength; i++) {
      datas.push(0);
    }
    return datas;
  }

  initChartOptions() {
    var fontColor: string;
    if (this.$vuetify.theme.dark) {
      fontColor = "white";
    } else {
      fontColor = "black";
    }
    this.chartOptions = {
      legend: {
        labels: {
          fontColor: fontColor,
          boxWidth: 20,
        },
      },
      responsive: true,
      plugins: {
        colorschemes: {
          scheme: "brewer.Paired12",
        },
      },
      maintainAspectRatio: false,
      scales: {
        xAxes: [
          {
            ticks: {
              beginAtZero: true,
              fontColor: fontColor,
            },
          },
        ],
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              fontColor: fontColor,
            },
          },
        ],
      },
      elements: {
        line: {
          tension: 0,
        },
      },
    };
  }

  beforeDestroy() {
    // window.removeEventListener("resize", () => {
    //   this.getWidth();
    // });
  }

  getWidth() {
    this.windowWidth = window.innerWidth;
  }

  setStartDate(days: number) {
    var d = new Date();
    var dayOfMonth = d.getDate();
    d.setDate(dayOfMonth - days);
    this.startDate = d.toISOString().substr(0, 10);
    this.endDate = this.nowDate;
  }

  private appendDatasets(liveData) {
    var _chartData = { ...this.chartData };
    if (_chartData.labels) {
      _chartData.labels.push(liveData.label);
      _chartData.labels.splice(0, 1);
    }

    if (_chartData.datasets) {
      for (var chartData of _chartData.datasets) {
        for (var data of liveData.datasets) {
          if (chartData.label == data.label) {
            if (chartData.data) {
              chartData.data.push(data.data[0]);
              chartData.data.splice(0, 1);
            } else {
              chartData.data = data.data;
            }
          }
        }
      }
    }
    this.chartData = _chartData;
  }

  private addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
      dataset.data.push(data);
    });
    chart.update();
  }

  private graphSet() {
    this.playGraph = !this.playGraph;
    this.playGraph
      ? (this.buttonString = this.$t("stop") as string)
      : (this.buttonString = this.$t("start") as string);
    if (this.playGraph) {
      this.start();
    } else {
      this.stop();
    }
  }

  initAxiosInstance() {
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });
    return instance;
  }

  async setAgencyList() {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/agency`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });
    this.agencyList = await instance.get(url).then((response) => {
      return response.data.result;
    });
  }

  async setGraphDataLive() {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/graph/live/agency/${this.agency}`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });

    // var data = await instance.get(url).then((response) => {
    //   return response.data.result;
    // });
    this.appendDatasets(
      await instance.get(url).then((response) => {
        return response.data.result;
      })
    );
  }

  async setGraphDataTerm() {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/graph/term`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });
    var data = {
      agency: this.agency,
      start: this.startDate,
      end: this.endDate,
    };
    this.chartData = await instance.post(url, data).then((response) => {
      return response.data.result;
    });
  }

  @Watch("graphType")
  onGraphTypeChanged(val: number, oldVal: number) {
    this.stop();
    this.initChartData();
    if (val == 0) {
      this.playGraph = false;
      this.buttonString = this.$t("start") as string;
    }
  }
}
</script>

<style lang="scss">
.button-area {
  width: fit-content;
  flex-direction: row;
  margin: auto;
  button {
    margin-top: 10px;
    margin-left: 10px;
  }
}
.main {
  height: 100%;
  padding: 10px 10px 0px 10px;
}
.container {
  height: 100%;
  padding: 10px 10px 0px 10px;
}
</style>
