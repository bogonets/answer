<i18n lang="yaml">
en:
  labels:
    search: "You can filter by port name."
    add: "Add Port"
    range: "Port range"

ko:
  labels:
    search: "포트 이름을 필터링할 수 있습니다."
    add: "포트 추가"
    range: "포트 범위"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row class="mt-2">
      <v-col>
        <div class="d-inline-flex flex-row align-center">
          <label-span size="subtitle-1" color="secondary">
            {{ $t('labels.range') }}
          </label-span>
          <v-text-field
              class="pl-2"
              disabled
              dense
              rounded
              outlined
              readonly
              hide-details
              v-model="portMinText"
          ></v-text-field>
          <span class="mx-2">~</span>
          <v-text-field
              disabled
              dense
              rounded
              outlined
              readonly
              hide-details
              v-model="portMaxText"
          ></v-text-field>
        </div>
      </v-col>
    </v-row>

<!--    <v-data-table-->
<!--        :value="selected"-->
<!--        @input="onInputSelected"-->
<!--        show-select-->
<!--        item-key="device_uid"-->
<!--        :headers="headers"-->
<!--        :items="items"-->
<!--        :search="filter"-->
<!--        :loading="loading"-->
<!--        :loading-text="$t('msg.loading')"-->
<!--    >-->
<!--      <template v-slot:top>-->
<!--        <div>-->
<!--          <v-toolbar flat>-->
<!--            <v-text-field-->
<!--                class="mr-4"-->
<!--                v-model="filter"-->
<!--                append-icon="mdi-magnify"-->
<!--                single-line-->
<!--                hide-details-->
<!--                :label="$t('labels.search')"-->
<!--            ></v-text-field>-->

<!--            <v-btn color="primary" class="align-self-center mr-2" @click="onClickAdd">-->
<!--              {{ $t('labels.add') }}-->
<!--            </v-btn>-->
<!--          </v-toolbar>-->
<!--        </div>-->
<!--        <div class="d-flex flex-row">-->
<!--          <v-btn-->
<!--              class="ml-2 rounded-xl"-->
<!--              color="green"-->
<!--              small-->
<!--              rounded-->
<!--              tile-->
<!--              :disabled="disabledStart"-->
<!--              @click="onClickStart"-->
<!--          >-->
<!--            <v-icon left>mdi-play</v-icon>-->
<!--            {{ $t('control.start') }}-->
<!--          </v-btn>-->
<!--          <v-btn-->
<!--              class="ml-2 rounded-xl"-->
<!--              color="red"-->
<!--              small-->
<!--              rounded-->
<!--              tile-->
<!--              :disabled="disabledStop"-->
<!--              @click="onClickStop"-->
<!--          >-->
<!--            <v-icon left>mdi-stop</v-icon>-->
<!--            {{ $t('control.stop') }}-->
<!--          </v-btn>-->
<!--          <v-btn-->
<!--              class="ml-2 rounded-xl"-->
<!--              color="primary"-->
<!--              small-->
<!--              outlined-->
<!--              rounded-->
<!--              tile-->
<!--              @click="onClickSync"-->
<!--          >-->
<!--            <v-icon left>mdi-sync</v-icon>-->
<!--            {{ $t('control.sync') }}-->
<!--          </v-btn>-->
<!--        </div>-->
<!--      </template>-->

<!--      <template v-slot:item.enable="{ item }">-->
<!--        <v-icon v-show="item.enable" small disabled>-->
<!--          mdi-check-->
<!--        </v-icon>-->
<!--      </template>-->

<!--      <template v-slot:item.status="{ item }">-->
<!--        <v-chip small :color="serverStatusColor(item)">-->
<!--          {{ item.status }}-->
<!--        </v-chip>-->
<!--      </template>-->


<!--      <template v-slot:item.actions="{ item }">-->
<!--        <v-icon small class="mr-2" @click="onClickDevice(item)">-->
<!--          mdi-pencil-->
<!--        </v-icon>-->
<!--      </template>-->

<!--      <template v-slot:no-data>-->
<!--        {{ $t('msg.empty') }}-->
<!--      </template>-->
<!--    </v-data-table>-->

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LabelSpan from '@/components/LabelSpan.vue';
// import type {DaemonA} from '@/packet/daemon';
// import {getStatusColor} from '@/packet/daemon';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LabelSpan,
  }
})
export default class AdminPorts extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Ports',
      disabled: true,
    },
  ];

  // private readonly headers = [
  //   {
  //     text: this.$t('headers.number'),
  //     align: 'center',
  //     filterable: true,
  //     sortable: true,
  //     value: 'number',
  //   },
  //   {
  //     text: this.$t('headers.ref_uid'),
  //     align: 'center',
  //     filterable: true,
  //     sortable: true,
  //     value: 'ref_uid',
  //   },
  //   {
  //     text: this.$t('headers.ref_category'),
  //     align: 'center',
  //     filterable: true,
  //     sortable: true,
  //     value: 'ref_category',
  //   },
  //   {
  //     text: this.$t('headers.description'),
  //     align: 'center',
  //     filterable: true,
  //     sortable: true,
  //     value: 'description',
  //   },
  //   {
  //     text: this.$t('headers.actions'),
  //     align: 'center',
  //     filterable: false,
  //     sortable: false,
  //     value: 'actions',
  //   },
  // ];

  loading = false;
  portMin?: number;
  portMax?: number;
  portMinText = '';
  portMaxText = '';

  // items = [] as Array<PortA>;
  // selected = [] as Array<PortA>;
  // filter = '';
  //
  // disabledStart = true;
  // disabledStop = true;

  created() {
    this.loading = true;
    (async () => {
      await this.setup();
    })();
  }

  async setup() {
    try {
      const range = await this.$api2.getAdminPortsRange();
      this.portMin = range.min;
      this.portMax = range.max;
      this.portMinText = range.min.toString();
      this.portMaxText = range.max.toString();
      console.debug("range: ", this.portMin, this.portMax);
    } catch (error) {
      this.portMin = undefined;
      this.portMax = undefined;
      this.portMinText = '';
      this.portMaxText = '';
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  // serverStatusColor(item: DaemonA) {
  //   return getStatusColor(item.status)
  // }
  //
  // onInputSelected(value) {
  //   this.selected = value;
  //   if (this.selected.length == 0) {
  //     this.disabledStart = true;
  //     this.disabledStop = true;
  //   } else {
  //     this.disabledStart = false;
  //     this.disabledStop = false;
  //   }
  // }
  //
  // onClickAdd() {
  //   this.moveToAdminDaemonsNew();
  // }
  //
  // onClickStart() {
  //   (async () => {
  //     await this.startSelected();
  //   })();
  // }
  //
  // onClickStop() {
  //   (async () => {
  //     await this.stopSelected();
  //   })();
  // }
  //
  // async startSelected() {
  //   try {
  //     for (const item of this.selected) {
  //       await this.$api2.postAdminDaemonsPdaemonStart(item.slug);
  //     }
  //     this.toastRequestSuccess();
  //     this.updateItems();
  //   } catch (error) {
  //     this.toastRequestFailure(error);
  //   }
  // }
  //
  // async stopSelected() {
  //   try {
  //     for (const item of this.selected) {
  //       await this.$api2.postAdminDaemonsPdaemonStop(item.slug);
  //     }
  //     this.toastRequestSuccess();
  //     this.updateItems();
  //   } catch (error) {
  //     this.toastRequestFailure(error);
  //   }
  // }
  //
  // onClickSync() {
  //   this.updateItems();
  // }
  //
  // onClickDevice(item: DaemonA) {
  //   this.moveToAdminDaemonsEdit(item.slug);
  // }
}
</script>
