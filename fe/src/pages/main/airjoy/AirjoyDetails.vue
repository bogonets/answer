<i18n lang="yaml">
en:
  groups: "Groups"
  airjoy_table: "Table"
  details: "Details: {0}"
  labels:
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
  airjoy_table: "Table"
  details: "Details: {0}"
  labels:
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
    <toolbar-breadcrumbs :items="breadcrumbs"
    ></toolbar-breadcrumbs>
    <v-divider></v-divider>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import VueApexCharts from 'vue-apexcharts';

@Component({
  components: {
    ToolbarBreadcrumbs,
    VueApexCharts,
  }
})
export default class AirjoyDetails extends VueBase {
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
      text: this.$t('airjoy_table'),
      disabled: false,
      href: () => this.moveToMainAirjoyTable(),
    },
    {
      text: this.$t('details', [this.$route.params.airjoy]),
      disabled: true,
    },
  ];

}
</script>
