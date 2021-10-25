<i18n lang="yaml">
en:
  labels:
    search: "You can filter by daemon name."
    add: "Add Daemon"
  headers:
    plugin: "Plugin"
    slug: "Slug"
    name: "Name"
    address: "Address"
    enable: "Enable"
    status: "Status"
    actions: "Actions"
  msg:
    loading: "Loading... Please wait"
    empty: "Empty Daemon"
  control:
    start: "Start"
    stop: "Stop"
    sync: "Sync"

ko:
  labels:
    search: "데몬 이름을 필터링할 수 있습니다."
    add: "데몬 추가"
  headers:
    plugin: "플러그인"
    slug: "슬러그"
    name: "이름"
    address: "주소"
    enable: "활성화"
    status: "상태"
    actions: "관리"
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "데몬이 존재하지 않습니다."
  control:
    start: "Start"
    stop: "Stop"
    sync: "Sync"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-data-table
        :value="selected"
        @input="onInputSelected"
        show-select
        item-key="device_uid"
        :headers="headers"
        :items="items"
        :search="filter"
        :loading="loading"
        :loading-text="$t('msg.loading')"
    >
      <template v-slot:top>
        <div>
          <v-toolbar flat>
            <v-text-field
                class="mr-4"
                v-model="filter"
                append-icon="mdi-magnify"
                single-line
                hide-details
                :label="$t('labels.search')"
            ></v-text-field>

            <v-btn color="primary" class="align-self-center mr-2" @click="onClickAdd">
              {{ $t('labels.add') }}
            </v-btn>
          </v-toolbar>
        </div>
        <div class="d-flex flex-row">
          <v-btn
              class="ml-2 rounded-xl"
              color="green"
              small
              rounded
              tile
              :disabled="disabledStart"
              @click="onClickStart"
          >
            <v-icon left>mdi-play</v-icon>
            {{ $t('control.start') }}
          </v-btn>
          <v-btn
              class="ml-2 rounded-xl"
              color="red"
              small
              rounded
              tile
              :disabled="disabledStop"
              @click="onClickStop"
          >
            <v-icon left>mdi-stop</v-icon>
            {{ $t('control.stop') }}
          </v-btn>
          <v-btn
              class="ml-2 rounded-xl"
              color="primary"
              small
              outlined
              rounded
              tile
              @click="onClickSync"
          >
            <v-icon left>mdi-sync</v-icon>
            {{ $t('control.sync') }}
          </v-btn>
        </div>
      </template>

      <template v-slot:item.enable="{ item }">
        <v-icon v-show="item.enable" small disabled>
          mdi-check
        </v-icon>
      </template>

      <template v-slot:item.status="{ item }">
        <v-chip small :color="serverStatusColor(item)">
          {{ item.status }}
        </v-chip>
      </template>


      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="onClickDevice(item)">
          mdi-pencil
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('msg.empty') }}
      </template>
    </v-data-table>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import type {DaemonA} from '@/packet/daemon';
import {getStatusColor} from '@/packet/daemon';

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class DevDaemons extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Dev',
      disabled: false,
      href: () => this.moveToDev(),
    },
    {
      text: 'Daemons',
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.plugin'),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'plugin',
    },
    {
      text: this.$t('headers.slug'),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'slug',
    },
    {
      text: this.$t('headers.name'),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'name',
    },
    {
      text: this.$t('headers.address'),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'address',
    },
    {
      text: this.$t('headers.enable'),
      align: 'center',
      filterable: false,
      sortable: true,
      value: 'enable',
    },
    {
      text: this.$t('headers.status'),
      align: 'center',
      filterable: false,
      sortable: true,
      value: 'status',
    },
    {
      text: this.$t('headers.actions'),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'actions',
    },
  ];

  loading = false;
  items = [] as Array<DaemonA>;
  selected = [] as Array<DaemonA>;
  filter = '';

  disabledStart = true;
  disabledStop = true;

  created() {
    this.updateItems();
  }

  updateItems() {
    this.loading = true;
    this.$api2.getDevDaemons()
        .then(items => {
          this.loading = false;
          this.items = items;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  serverStatusColor(item: DaemonA) {
    return getStatusColor(item.status)
  }

  onInputSelected(value) {
    this.selected = value;
    if (this.selected.length == 0) {
      this.disabledStart = true;
      this.disabledStop = true;
    } else {
      this.disabledStart = false;
      this.disabledStop = false;
    }
  }

  onClickAdd() {
    this.moveToDevDaemonsNew();
  }

  onClickStart() {
    (async () => {
      await this.startSelected();
    })();
  }

  onClickStop() {
    (async () => {
      await this.stopSelected();
    })();
  }

  async startSelected() {
    try {
      for (const item of this.selected) {
        await this.$api2.postDevDaemonsPdaemonStart(item.slug);
      }
      this.toastRequestSuccess();
      this.updateItems();
    } catch (error) {
      this.toastRequestFailure(error);
    }
  }

  async stopSelected() {
    try {
      for (const item of this.selected) {
        await this.$api2.postDevDaemonsPdaemonStop(item.slug);
      }
      this.toastRequestSuccess();
      this.updateItems();
    } catch (error) {
      this.toastRequestFailure(error);
    }
  }

  onClickSync() {
    this.updateItems();
  }

  onClickDevice(item: DaemonA) {
    this.moveToDevDaemonsEdit(item.slug);
  }
}
</script>
