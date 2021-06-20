<template>
  <div class="main">
    <v-container class="container pa-0" fluid>
      <v-layout fill-height>
        <v-row no-gutters>
          <v-col class="mx-auto">
            <v-row no-gutters class="table">
              <v-col v-if="isMobile()" cols="12">
                <v-layout>
                  <v-autocomplete
                    prepend-inner-icon="fas fa-search"
                    v-model="search"
                    :items="agencyList"
                    outlined
                    dense
                    hide-details
                    v-on:change="onSearchFilter(search)"
                    class="elevation-1"
                  ></v-autocomplete>
                </v-layout>
              </v-col>
              <v-col v-else>
                <v-layout class="flex-column" style="height: 90vh">
                  <v-flex>
                    <v-text-field
                      prepend-inner-icon="fas fa-search"
                      :label="$t('agency_name')"
                      class="elevation-1 ma-2"
                      v-model="search"
                      dense
                      solo
                      outlined
                      width="80%"
                      hide-details
                    >
                    </v-text-field>
                  </v-flex>
                  <v-flex style="overflow: auto; height: 100%" class="pa-0">
                    <v-simple-table class="mx-2">
                      <template v-slot:default>
                        <tbody>
                          <tr
                            v-for="item in agencyList"
                            :key="item.name"
                            :class="{ selectedRow: item === selectedItem }"
                            @click="onSearchFilter(item), onSelectedItem(item)"
                          >
                            <td v-if="item.includes(search)">
                              {{ item }}
                            </td>
                          </tr>
                        </tbody>
                      </template>
                    </v-simple-table>
                  </v-flex>
                </v-layout>
              </v-col>

              <v-col md="10" sm="12" xs="12">
                <v-layout column style="height: 90vh">
                  <v-flex>
                    <v-data-table
                      :style="this.$backgroundColor()"
                      mobile-breakpoint="0"
                      :footer-props="{ itemsPerPageText: this.pageText }"
                      height="37vh"
                      disable-sort
                      :headers="manageHeader.firstHeader"
                      :items="manageData.nonMetricDatas"
                      class="elevation-1 ma-2"
                    >
                      <template v-slot:body="{ headers, items }">
                        <tbody>
                          <tr v-for="(item, idx) in items" :key="idx">
                            <td v-for="(header, key) in headers" :key="key">
                              <table-item
                                :serial="item.serial"
                                :header="header.value"
                                :item="String(item[header.value])"
                                v-on:editItem="editItem($event, false)"
                                v-on:buttonEvent="deviceSignal($event)"
                              ></table-item>
                            </td>
                          </tr>
                        </tbody>
                      </template>
                    </v-data-table>
                  </v-flex>
                  <v-flex>
                    <v-data-table
                      :style="this.$backgroundColor()"
                      mobile-breakpoint="0"
                      :footer-props="{ itemsPerPageText: this.pageText }"
                      height="37vh"
                      :headers="manageHeader.secondHeader"
                      :items="manageData.metricDatas"
                      class="elevation-1 ma-2"
                    >
                      <template v-slot:body="{ headers, items }">
                        <tbody>
                          <tr v-for="(item, idx) in items" :key="idx">
                            <td v-for="(header, key) in headers" :key="key">
                              <table-item
                                :serial="item.serial"
                                :header="header.value"
                                :item="String(item[header.value])"
                                v-on:editItem="editItem($event, true)"
                                v-on:buttonEvent="deviceSignal($event)"
                              ></table-item>
                            </td>
                          </tr>
                        </tbody>
                      </template>
                    </v-data-table>
                  </v-flex>
                </v-layout>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-layout>
    </v-container>
  </div>
</template>
<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";
import TableItem from "./TableItem.vue";
import * as AirJoy from "./AirJoy";
import axios from "axios";

@Component({
  components: {
    TableItem,
  },
})
export default class AirJoyManage extends Vue {
  private BASE_URL = this.$api.getUrl();
  private TIMEOUT = 3000;

  search = "";
  dialog = false;
  pageText = "";

  windowWidth = window.innerWidth;

  // data
  manageHeader!: AirJoy.ManageHeader;
  manageData = new AirJoy.ManageData();
  metricDatas!: Array<AirJoy.ManageMetricData>;
  nonMetricDatas!: Array<AirJoy.ManageNonMetricData>;
  agencyList = new Array<string>();
  selectedItem = null;

  created() {
    this.initManageData();
    this.setPageText();
  }

  setPageText() {
    if (this.$i18n.locale == "ko") {
      this.pageText = "페이지당 데이터 수";
    } else {
      this.pageText = "Row per Page";
    }
  }

  mounted() {
    this.$nextTick(function() {
      window.addEventListener("resize", () => {
        this.getWidth();
      });
    });
  }

  initManageData() {
    this.setManageHeader();
    this.setNonMetricData();
  }

  isMobile() {
    if (this.windowWidth < 960) {
      return true;
    } else {
      return false;
    }
  }

  getWidth() {
    this.windowWidth = window.innerWidth;
    this.setManageHeader();
  }

  setManageHeader() {
    this.manageHeader = new AirJoy.ManageHeader(this.windowWidth);
  }

  beforeDestroy() {
    window.removeEventListener("resize", () => {
      this.getWidth();
    });
  }

  onSelectedItem(item) {
    this.selectedItem = item;
  }

  onSearchFilter(search: string) {
    if (search == "[모두 선택]" || search == "[All Select]") {
      this.manageData.nonMetricDatas = this.nonMetricDatas;
      this.manageData.metricDatas = this.metricDatas;
    } else {
      this.manageData.nonMetricDatas = this.nonMetricDatas.filter(
        (n) => n.agency == search
      );

      this.manageData.metricDatas = new Array<AirJoy.ManageMetricData>();
      for (const data of this.manageData.nonMetricDatas) {
        for (const metric of this.metricDatas) {
          if (data.serial == metric.serial)
            this.manageData.metricDatas.push(metric);
        }
      }
    }
  }

  @Watch("search")
  onClearEvent() {
    if (this.search == null || this.search.length == 0) {
      this.manageData.metricDatas = this.metricDatas;
      this.manageData.nonMetricDatas = this.nonMetricDatas;
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

  async getApi(url: string) {
    return await this.initAxiosInstance()
      .get(url)
      .then((response) => {
        return response.data.result;
      });
  }

  async putApi(url: string, data: any) {
    return await this.initAxiosInstance()
      .put(url, data)
      .then((response) => {
        return response.data.result;
      });
  }

  async postApi(url: string, data: any) {
    return await this.initAxiosInstance()
      .post(url, data)
      .then((response) => {
        return response.data.result;
      });
  }

  async deleteApi(url: string) {
    return await this.initAxiosInstance()
      .delete(url)
      .then((response) => {
        return response.data.result;
      });
  }

  async setNonMetricData() {
    const projectName = this.$store.getters["project/getSelectProject"];
    const nonMetricUrl = `/api/v1/extra/airjoy/project/${projectName}/manage/non-metric`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });
    this.nonMetricDatas = await instance.get(nonMetricUrl).then((response) => {
      return response.data.result;
    });

    this.manageData.nonMetricDatas = this.nonMetricDatas;
    if (this.$i18n.locale == "ko") {
      this.agencyList.push("[모두 선택]");
    } else {
      this.agencyList.push("[All Select]");
    }
    for (const item of this.nonMetricDatas) {
      if (!this.agencyList.includes(item.agency))
        this.agencyList.push(item.agency);
    }

    this.setMetricData();
  }

  async setMetricData() {
    const projectName = this.$store.getters["project/getSelectProject"];
    const metricUrl = `/api/v1/extra/airjoy/project/${projectName}/manage/metric`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });
    this.metricDatas = await instance.get(metricUrl).then((response) => {
      return response.data.result;
    });
    this.manageData.metricDatas = this.metricDatas;
  }

  async editItem(event, metric) {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/manage/edit`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });

    var data = {
      serial: event.serial,
      header: event.header,
      value: event.value,
    };

    var result = await instance.post(url, data).then((response) => {
      return response.data.result;
    });

    // if (metric) {
    //   this.setMetricData();
    // } else {
    //   this.setNonMetricData();
    // }
  }

  async deviceSignal(event) {
    const projectName = this.$store.getters["project/getSelectProject"];
    const url = `/api/v1/extra/airjoy/project/${projectName}/manage/signal`;
    const access = this.$store.getters["user/getAccessToken"];
    const instance = axios.create({
      baseURL: this.BASE_URL,
      timeout: this.TIMEOUT,
      headers: { Authorization: "Bearer " + access },
    });
    var data = {
      serial: event.signal,
      signal: event.header,
    };
    var result = await instance.post(url, data).then((response) => {
      return response.data.result;
    });
  }
}
</script>

<style scoped>
.main {
  height: 100%;
}
.container {
  height: 100%;
}
.table {
  background-color: rgba(125, 125, 125, 0.2);
}
.v-data-table-header-mobile {
  display: none !important;
}
.selectedRow {
  background-color: darkgrey;
  font-weight: bold;
}
</style>
