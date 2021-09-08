<i18n lang="yaml">
en:
  label:
    search: "You can filter by name or UID."
  msg:
    loading: "Loading... Please wait"
    empty: "Devices do not exist"

ko:
  label:
    search: "이름 또는 UID를 필터링할 수 있습니다."
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "장치가 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <breadcrumb-main name="Table"></breadcrumb-main>
    <v-divider></v-divider>

    <v-data-table
        hide-default-header
        :items="items"
        :search="filter"
        :loading="loading"
        :headers="headers"
        :loading-text="$t('msg.loading')"
    >
      <template v-if="!hideTopBar" v-slot:top>
        <v-toolbar flat>
          <v-text-field
              v-if="!hideFilterInput"
              class="mr-4"
              v-model="filter"
              append-icon="mdi-magnify"
              single-line
              hide-details
              :label="$t('label.search')"
          ></v-text-field>
        </v-toolbar>
      </template>

      <template v-slot:item="{ item }">
        <airjoy-table-item
            hide-description
            :item="item"
        ></airjoy-table-item>
      </template>

      <template v-slot:no-data>
        {{ $t('msg.empty') }}
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import {AirjoyA, createEmptyAirjoyA} from "@/packet/airjoy";
import AirjoyTableItem from "@/pages/main/airjoy/AirjoyTableItem.vue";

@Component({
  components: {
    AirjoyTableItem,
    BreadcrumbMain,
  }
})
export default class AirjoyTable extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly hideFilterInput!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionDelete!: boolean;

  @Prop({type: Boolean, default: false})
  readonly clickableRow!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  readonly headers = [
    {
      filterable: true,
      value: 'name',
    },
    {
      filterable: true,
      value: 'uid',
    },
  ];

  items = [] as Array<AirjoyA>;
  filter = '';

  get hideTopBar(): boolean {
    return this.hideFilterInput;
  }

  created() {
    this.items = [
      createEmptyAirjoyA(),
      createEmptyAirjoyA(),
      createEmptyAirjoyA(),
      createEmptyAirjoyA(),
      createEmptyAirjoyA(),
    ] as Array<AirjoyA>;
    this.items[0].name = 'name1';
    this.items[1].name = 'name2';
    this.items[2].name = 'name3';
    this.items[3].name = 'name4';
    this.items[4].name = 'name5';

    this.items[0].description = 'More description1';
    this.items[1].description = 'More description2';
    this.items[2].description = 'More description3';
    this.items[3].description = 'More description4';
    this.items[4].description = 'More description5';

    this.items[0].online = true;
    this.items[1].online = true;
    this.items[2].online = false;
    this.items[3].online = false;
    this.items[4].online = false;

    this.items[0].asCount = 0;
    this.items[1].asCount = 0;
    this.items[2].asCount = 10;
    this.items[3].asCount = 20;
    this.items[4].asCount = 30;

    this.items[0].asLast = '';
    this.items[1].asLast = '';
    this.items[2].asLast = '2020-01-01';
    this.items[3].asLast = '2020-01-02';
    this.items[4].asLast = '2021-09-10T21:10';

    this.items[0].fwVer = 10;
    this.items[1].fwVer = 20;
    this.items[2].fwVer = 30;
    this.items[3].fwVer = 40;
    this.items[4].fwVer = 51;

    this.items[0].uid = 100;
    this.items[1].uid = 200;
    this.items[2].uid = 300;
    this.items[3].uid = 400;
    this.items[4].uid = 501;

    this.items[0].pm10 = 0;
    this.items[1].pm10 = 10;
    this.items[2].pm10 = 20;
    this.items[3].pm10 = 30;
    this.items[4].pm10 = 40;

    this.items[0].pm2_5 = 0;
    this.items[1].pm2_5 = 3;
    this.items[2].pm2_5 = 3.24;
    this.items[3].pm2_5 = 30;
    this.items[4].pm2_5 = 100;

    this.items[0].co2 = 0;
    this.items[1].co2 = 20;
    this.items[2].co2 = 30;
    this.items[3].co2 = 40;
    this.items[4].co2 = 100;

    this.items[0].humidity = 0;
    this.items[1].humidity = 20;
    this.items[2].humidity = 30;
    this.items[3].humidity = 40;
    this.items[4].humidity = 100;

    this.items[0].temperature = 0;
    this.items[1].temperature = 20;
    this.items[2].temperature = 30;
    this.items[3].temperature = 40;
    this.items[4].temperature = 100;

    this.items[0].voc = 0;
    this.items[1].voc = 1;
    this.items[2].voc = 2;
    this.items[3].voc = 3;
    this.items[4].voc = 3;

    this.items[0].mode = 0;
    this.items[1].mode = 0;
    this.items[2].mode = 1;
    this.items[3].mode = 1;
    this.items[4].mode = 1;

    this.items[0].mode = 0;
    this.items[1].mode = 0;
    this.items[2].mode = 1;
    this.items[3].mode = 1;
    this.items[4].mode = 1;

    this.items[0].powerState = 0;
    this.items[1].powerState = 0;
    this.items[2].powerState = 1;
    this.items[3].powerState = 1;
    this.items[4].powerState = 1;

    this.items[0].fanControl = 1;
    this.items[1].fanControl = 2;
    this.items[2].fanControl = 3;
    this.items[3].fanControl = 4;
    this.items[4].fanControl = 5;

    this.items[0].lock = 0;
    this.items[1].lock = 0;
    this.items[2].lock = 1;
    this.items[3].lock = 1;
    this.items[4].lock = 1;

    this.items[0].filter = 0;
    this.items[1].filter = 0;
    this.items[2].filter = 1;
    this.items[3].filter = 1;
    this.items[4].filter = 2;

    this.items[0].filterLife = 0;
    this.items[1].filterLife = 1;
    this.items[2].filterLife = 10;
    this.items[3].filterLife = 20;
    this.items[4].filterLife = 40;

    this.items[0].uvLed = 0;
    this.items[1].uvLed = 0;
    this.items[2].uvLed = 1;
    this.items[3].uvLed = 1;
    this.items[4].uvLed = 1;

    this.items[0].timeReservation = 0;
    this.items[1].timeReservation = 1;
    this.items[2].timeReservation = 2;
    this.items[3].timeReservation = 3;
    this.items[4].timeReservation = 4;

    this.items[0].sleepMode = 0;
    this.items[1].sleepMode = 0;
    this.items[2].sleepMode = 1;
    this.items[3].sleepMode = 1;
    this.items[4].sleepMode = 1;
  }
}
</script>
