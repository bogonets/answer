<i18n lang="yaml">
en:
  groups: "Groups"
  devices: "Devices"
  details: "Details"
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
  details: "Details"
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
    <toolbar-breadcrumbs :items="breadcrumbs"
    ></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row class="mt-4">
      <v-col cols="4">
        <div class="card" @click="onClickPm10">
          <v-icon left large>mdi-dots-hexagon</v-icon>
          <span class="text--secondary text-subtitle-2">{{ $t('categories.pm10', [item.pm10]) }}</span>
        </div>
      </v-col>

      <v-col cols="4">
        <div class="card" @click="onClickPm2_5">
          <v-icon left large>mdi-dots-horizontal</v-icon>
          <span class="text--secondary text-subtitle-2">{{ $t('categories.pm2_5', [item.pm2_5]) }}</span>
        </div>
      </v-col>

      <v-col cols="4">
        <div class="card" @click="onClickCo2">
          <v-icon left large>mdi-molecule-co2</v-icon>
          <span class="text--secondary text-subtitle-2">{{ $t('categories.co2', [item.co2]) }}</span>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="4">
        <div class="card" @click="onClickHumidity">
          <v-icon left large>mdi-water</v-icon>
          <span class="text--secondary text-subtitle-2">{{ $t('categories.humidity', [item.humidity]) }}</span>
        </div>
      </v-col>

      <v-col cols="4">
        <div class="card" @click="onClickTemperature">
          <v-icon left large>mdi-thermometer</v-icon>
          <span class="text--secondary text-subtitle-2">{{ $t('categories.temperature', [item.temperature]) }}</span>
        </div>
      </v-col>

      <v-col cols="4">
        <div class="card" @click="onClickAs">
          <v-icon left large>mdi-wrench</v-icon>
          <span class="text--secondary text-subtitle-2">{{ $t('categories.as', [item.asCount]) }}</span>
        </div>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>

    <v-row>
      <v-col cols="2">
        <div class="card elevation-2 green">
          <v-icon large>mdi-power</v-icon>
          <span class="text--secondary text-subtitle-2">POWER</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div class="card elevation-2 orange accent-4">
          <v-icon large>mdi-weather-sunny</v-icon>
          <span class="text--secondary text-subtitle-2">UV</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div class="card elevation-2 green">
          <v-icon large>mdi-lan-connect</v-icon>
          <span class="text--secondary text-subtitle-2">ONLINE</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div class="card elevation-2">
          <v-icon large>mdi-alpha-a-circle-outline</v-icon>
          <span class="text--secondary text-subtitle-2">AUTO</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div class="card elevation-2">
          <v-icon large>mdi-lock-open-variant</v-icon>
          <span class="text--secondary text-subtitle-2">UNLOCK</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div class="card elevation-2">
          <v-icon large>mdi-sleep</v-icon>
          <span class="text--secondary text-subtitle-2">SLEEP</span>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="2">
        <div class="card elevation-2">
          <v-icon large>mdi-air-filter</v-icon>
          <span class="text--secondary text-subtitle-2">RESET</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div class="card elevation-2">
          <v-icon large>mdi-fan-auto</v-icon>
          <span class="text--secondary text-subtitle-2">AUTO</span>
        </div>
      </v-col>

      <v-col cols="2">
        <div class="card elevation-2">
          <v-icon large>mdi-timer-off-outline</v-icon>
          <span class="text--secondary text-subtitle-2">OFF</span>
        </div>
      </v-col>
    </v-row>

    <v-divider class="my-4"></v-divider>

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
export default class MainAirjoyDetails extends VueBase {
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
      text: this.$t('details'),
      disabled: true,
    },
    {
      text: this.$route.params.airjoy,
      disabled: true,
    },
  ];

  readonly headers = [
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

  item = createEmptyAirjoyA();
  asItems = [] as Array<AirjoyAsA>;
  loading = false;
  filter = '';

  showAsDialog = false;
  loadingAsSubmit = false;

  created() {
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

  onClickPm10() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_PM10);
  }

  onClickPm2_5() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_PM2_5);
  }

  onClickCo2() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_CO2);
  }

  onClickHumidity() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_HUMIDITY);
  }

  onClickTemperature() {
    this.moveToMainAirjoyChart(`${this.item.uid}`, CATEGORY_TEMPERATURE);
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
@import '~vuetify/src/styles/styles.sass';

.card {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-content: center;
  align-items: center;

  padding: 24px;
  border-radius: 12px;
  border-style: solid;
  border-width: 1px;

  cursor: pointer;
}

.theme--light.v-application .card {
  border-color: rgba(map-get($shades, 'black'), 0.2);
}

.theme--dark.v-application .card {
  border-color: rgba(map-get($shades, 'white'), 0.2);
}

.row-pointer {
  cursor: pointer;
}
</style>
