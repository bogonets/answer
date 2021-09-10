<i18n lang="yaml">
en:
  groups: "Groups"
  devices: "Devices"
  as: "A/S"
  categories:
    pm10: "PM10: {0}"
    pm2_5: "PM2.5: {0}"
    co2: "CO2: {0}"
    humidity: "Humidity: {0}"
    temperature: "Temperature: {0}"
    voc: "VOC: {0}"
    as: "A/S: {0}"
  labels:
    search: "You can filter by author or description."
    as_new: "New A/S"
    device: "Please select a device ID to output as a chart"
  headers:
    author: "Author"
    description: "Description"
    datetime: "Datetime"
    actions: "Actions"
  msg:
    loading: "Loading... Please wait"
    empty: "Empty A/S"

ko:
  groups: "Groups"
  devices: "Devices"
  as: "A/S"
  categories:
    pm10: "미세먼지: {0}"
    pm2_5: "초미세먼지: {0}"
    co2: "이산화탄소: {0}"
    humidity: "습도: {0}"
    temperature: "온도: {0}"
    voc: "VOC: {0}"
    as: "A/S: {0}"
  labels:
    search: "담당자 또는 기록을 필터링할 수 있습니다."
    as_new: "새로운 A/S 기록"
    device: "차트로 출력할 장치 ID를 선택하세요"
  headers:
    author: "담당자"
    description: "기록"
    datetime: "날짜"
    actions: "관리"
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "A/S 기록이 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row class="my-4">
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

    <v-card>
      <v-data-table
          :class="dataTableClass"
          :headers="headers"
          :items="asItems"
          :search="filter"
          :loading="loading"
          :loading-text="$t('msg.loading')"
          @click:row="onClickAsRow"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-text-field
                class="mr-4"
                v-model="filter"
                append-icon="mdi-magnify"
                single-line
                hide-details
                :label="$t('labels.search')"
            ></v-text-field>
            <v-btn color="primary" @click="onClickNewAs">
              {{ $t('labels.as_new') }}
            </v-btn>
          </v-toolbar>
        </template>

        <template v-if="!hideActions" v-slot:item.actions="{ item }">
          <v-icon v-if="!hideActionEdit" small class="mr-2" @click="onClickAsEdit(item)">
            mdi-pencil
          </v-icon>
          <v-icon v-if="!hideActionMove" small color="red" @click="onClickAsDelete(item)">
            mdi-delete
          </v-icon>
        </template>

        <template v-slot:no-data>
          {{ $t('msg.empty') }}
        </template>
      </v-data-table>

      <!-- A/S dialog. -->
      <v-dialog v-model="showAsDialog" max-width="320">
        <v-card>
          <v-card-title class="text-h5">
            {{ $t('labels.as_new') }}
          </v-card-title>
          <!--        <v-card-text>-->
          <!--          {{ $t('hints.as_new') }}-->
          <!--        </v-card-text>-->
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="onClickNewAsCancel">
              {{ $t('cancel') }}
            </v-btn>
            <v-btn :loading="loadingAsSubmit" color="primary" @click="onClickNewAsSubmit">
              {{ $t('delete') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>

  </v-container>
</template>

<script lang='ts'>
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import VueApexCharts from 'vue-apexcharts';
import type {AirjoyAsA} from '@/packet/airjoy';
import {
  CATEGORY_PM10,
  CATEGORY_PM2_5,
  CATEGORY_CO2,
  CATEGORY_HUMIDITY,
  CATEGORY_TEMPERATURE,
  createEmptyAirjoyA, createEmptyAirjoyAsA,
} from '@/packet/airjoy';

@Component({
  components: {
    ToolbarBreadcrumbs,
    VueApexCharts,
  }
})
export default class MainAirjoyAs extends VueBase {
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
      text: this.$t('as'),
      disabled: true,
    },
    {
      text: this.$route.params.airjoy,
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.author'),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'author',
    },
    {
      text: this.$t('headers.description'),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'description',
    },
    {
      text: this.$t('headers.datetime'),
      align: 'center',
      filterable: false,
      sortable: true,
      value: 'datetime',
    },
    {
      text: this.$t('headers.actions'),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'actions',
    }
  ];

  @Prop({type: Boolean, default: false})
  readonly hideActionEdit!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionMove!: boolean;

  device = '';
  devices = ['100', '200', '300', '400']

  asItems = [] as Array<AirjoyAsA>;
  loading = false;
  filter = '';

  showAsDialog = false;
  loadingAsSubmit = false;

  created() {
    const device = this.$route.params.airjoy;
    const deviceIndex = this.devices.indexOf(device);
    if (deviceIndex !== -1) {
      this.device = device;
    }

    this.asItems = [
      createEmptyAirjoyAsA(),
      createEmptyAirjoyAsA(),
      createEmptyAirjoyAsA(),
      createEmptyAirjoyAsA(),
      createEmptyAirjoyAsA(),
    ];
    this.asItems[0].author = 'User0'
    this.asItems[1].author = 'User1'
    this.asItems[2].author = 'Name2'
    this.asItems[3].author = 'Name3'
    this.asItems[4].author = 'Name4'

    this.asItems[0].description = 'Description0'
    this.asItems[1].description = 'Description1'
    this.asItems[2].description = 'Brief2'
    this.asItems[3].description = 'Brief3'
    this.asItems[4].description = 'Brief4'

    this.asItems[0].datetime = '2021-01-01'
    this.asItems[1].datetime = '2021-02-03'
    this.asItems[2].datetime = '2021-03-20'
    this.asItems[3].datetime = '2021-04-12'
    this.asItems[4].datetime = '2021-05-30'
  }

  get dataTableClass(): string {
    if (this.asItems.length >= 1) {
      return 'row-pointer';
    } else {
      return '';
    }
  }

  get hideActions(): boolean {
    return this.hideActionEdit && this.hideActionMove;
  }

  onClickNewAs() {
    this.showAsDialog = true;
  }

  onClickNewAsCancel() {
    this.showAsDialog = false;
  }

  onClickNewAsSubmit() {
    this.showAsDialog = false;
  }

  onClickAs() {
  }

  onClickAsRow(item: AirjoyAsA) {
  }

  onClickAsEdit(item: AirjoyAsA) {
  }

  onClickAsDelete(item: AirjoyAsA) {
  }
}
</script>

<style lang="scss" scoped>
.row-pointer {
  cursor: pointer;
}
</style>
