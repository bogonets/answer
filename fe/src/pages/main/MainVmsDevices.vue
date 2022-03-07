<i18n lang="yaml">
en:
  devices: "Devices"
  headers:
    name: "Name"
    stream_address: "Stream URL"
    server_running: "Server Running"
    server_status: "Server Status"
    actions: "Actions"
  msg:
    search: "You can filter by name."
    loading: "Loading... Please wait"
    empty: "Empty Devices"
  labels:
    add: "Add Device"
    discovery: "Device Discovery"
  control:
    start: "Start"
    stop: "Stop"
    sync: "Sync"
  status:
    created: "Created"
    beginning: "Beginning"
    running: "Running"
    ending: "Ending"
    restarting: "Restarting"
    paused: "Paused"
    exited: "Exited"
    dead: "Dead"
    unknown: "Unknown"
    undefined: "Undefined"

ko:
  devices: "Devices"
  headers:
    name: "이름"
    stream_address: "스트리밍 주소"
    server_running: "서버 실행"
    server_status: "서버 상태"
    actions: "관리"
  msg:
    search: "이름을 필터링할 수 있습니다."
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "장치가 존재하지 않습니다."
  labels:
    add: "장치 추가"
    discovery: "장치 탐색"
  control:
    start: "Start"
    stop: "Stop"
    sync: "Sync"
  status:
    created: "Created"
    beginning: "Beginning"
    running: "Running"
    ending: "Ending"
    restarting: "Restarting"
    paused: "Paused"
    exited: "Exited"
    dead: "Dead"
    unknown: "Unknown"
    undefined: "Undefined"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-data-table
        :value="selected"
        @input="onInputSelected"
        show-select
        sort-desc
        sort-by="name"
        item-key="device_uid"
        :items-per-page="itemsPerPage"
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
                :label="$t('msg.search')"
                single-line
                hide-details
            ></v-text-field>

            <v-btn color="primary" class="align-self-center mr-2" @click="onClickDiscovery">
              {{ $t('labels.discovery') }}
            </v-btn>
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

      <template v-slot:item.server_running="{ item }">
        <v-icon v-show="item.server_running" small disabled>
          mdi-check
        </v-icon>
      </template>

      <template v-slot:item.server_status="{ item }">
        <v-chip small :color="serverStatusColor(item)">
          {{ serverStatusText(item) }}
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
import type {VmsDeviceA} from '@/packet/vms';
import {
  MEDIA_SERVER_STATUS_CREATE,
  MEDIA_SERVER_STATUS_BEGINNING,
  MEDIA_SERVER_STATUS_RUNNING,
  MEDIA_SERVER_STATUS_ENDING,
  MEDIA_SERVER_STATUS_RESTARTING,
  MEDIA_SERVER_STATUS_PAUSED,
  MEDIA_SERVER_STATUS_EXITED,
  MEDIA_SERVER_STATUS_DEAD,
} from '@/packet/vms';

const ITEMS_PER_PAGE = 15;

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class MainVmsDevices extends VueBase {
  readonly itemsPerPage = ITEMS_PER_PAGE;
  readonly breadcrumbs = [
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
      disabled: true,
    },
  ];

  readonly headers = [
    {
      text: this.$t('headers.name').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'name',
    },
    {
      text: this.$t('headers.stream_address').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'stream_address',
    },
    {
      text: this.$t('headers.server_running').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      width: '100px',
      value: 'server_running',
    },
    {
      text: this.$t('headers.server_status').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      width: '100px',
      value: 'server_status',
    },
    {
      text: this.$t('headers.actions').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      width: '1px',
      value: 'actions',
    },
  ];

  loading = false;
  items = [] as Array<VmsDeviceA>;
  selected = [] as Array<VmsDeviceA>;
  filter = '';

  disabledStart = true;
  disabledStop = true;

  created() {
    this.updateItems();
  }

  updateItems() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    this.$api2.getVmsDevices(group, project)
        .then(items => {
          this.loading = false;
          this.items = items;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  serverStatusColor(item: VmsDeviceA) {
    if (typeof item.server_status === 'undefined') {
      return 'grey';
    }
    switch (item.server_status) {
      case MEDIA_SERVER_STATUS_CREATE:
        return 'info';
      case MEDIA_SERVER_STATUS_BEGINNING:
        return 'info';
      case MEDIA_SERVER_STATUS_RUNNING:
        return 'success';
      case MEDIA_SERVER_STATUS_ENDING:
        return 'info';
      case MEDIA_SERVER_STATUS_RESTARTING:
        return 'info';
      case MEDIA_SERVER_STATUS_PAUSED:
        return 'info';
      case MEDIA_SERVER_STATUS_EXITED:
        return 'grey';
      case MEDIA_SERVER_STATUS_DEAD:
        return 'error';
      default:
        return 'grey';
    }
  }

  serverStatusText(item: VmsDeviceA) {
    if (typeof item.server_status === 'undefined') {
      return this.$t('status.undefined').toString();
    }
    switch (item.server_status) {
      case MEDIA_SERVER_STATUS_CREATE:
        return this.$t('status.create').toString();
      case MEDIA_SERVER_STATUS_BEGINNING:
        return this.$t('status.beginning').toString();
      case MEDIA_SERVER_STATUS_RUNNING:
        return this.$t('status.running').toString();
      case MEDIA_SERVER_STATUS_ENDING:
        return this.$t('status.ending').toString();
      case MEDIA_SERVER_STATUS_RESTARTING:
        return this.$t('status.restarting').toString();
      case MEDIA_SERVER_STATUS_PAUSED:
        return this.$t('status.paused').toString();
      case MEDIA_SERVER_STATUS_EXITED:
        return this.$t('status.exited').toString();
      case MEDIA_SERVER_STATUS_DEAD:
        return this.$t('status.dead').toString();
      default:
        return this.$t('status.unknown').toString();
    }
  }

  onClickStart() {
    for (const item of this.selected) {
      const group = this.$route.params.group;
      const project = this.$route.params.project;
      const device = item.device_uid.toString();
      this.$api2.postVmsDeviceProcessStart(group, project, device)
          .then(() => {
            this.toastRequestSuccess();
            this.updateItems();
          })
          .catch(error => {
            this.toastRequestFailure(error);
          });
    }
  }

  onClickStop() {
    for (const item of this.selected) {
      const group = this.$route.params.group;
      const project = this.$route.params.project;
      const device = item.device_uid.toString();
      this.$api2.postVmsDeviceProcessStop(group, project, device)
          .then(() => {
            this.toastRequestSuccess();
            this.updateItems();
          })
          .catch(error => {
            this.toastRequestFailure(error);
          });
    }
  }

  onClickSync() {
    this.updateItems();
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

  onClickDiscovery() {
    this.moveToMainVmsDevicesDiscovery();
  }

  onClickAdd() {
    this.moveToMainVmsDevicesNew();
  }

  onClickDevice(item: VmsDeviceA) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = item.device_uid.toString();
    this.moveToMainVmsDevicesEditInfo(group, project, device);
  }
}
</script>
