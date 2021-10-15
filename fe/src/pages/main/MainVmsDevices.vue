<i18n lang="yaml">
en:
  devices: "VMS Devices"
  headers:
    name: "Name"
    url: "URL"
    user: "User"
    online: "Online"
    actions: "Actions"
  msg:
    search: "You can filter by ip or name."
    loading: "Loading... Please wait"
    empty: "Empty Devices"
  labels:
    add: "Add Device"
    discovery: "Device Discovery"

ko:
  devices: "VMS Devices"
  headers:
    name: "이름"
    url: "URL"
    user: "사용자"
    online: "온라인"
    actions: "관리"
  msg:
    search: "IP 또는 이름을 필터링할 수 있습니다."
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "장치가 존재하지 않습니다."
  labels:
    add: "장치 추가"
    discovery: "장치 탐색"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-data-table
        :items-per-page="itemsPerPage"
        :headers="headers"
        :items="items"
        :search="filter"
        :loading="loading"
        :loading-text="$t('msg.loading')"
    >
      <template v-slot:top>
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
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon small disabled class="mr-2" @click="onClickDevice(item)">
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
      text: this.$t('headers.url').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'url',
    },
    {
      text: this.$t('headers.user').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'user',
    },
    {
      text: this.$t('headers.online').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'online',
    },
    {
      text: this.$t('headers.actions').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'actions',
    },
  ];

  loading = false;
  items = [] as Array<VmsDeviceA>;
  filter = '';

  created() {
    this.updateItems();
  }

  updateItems() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
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
    this.moveToMainVmsDevicesEdit(group, project, device);
  }
}
</script>
