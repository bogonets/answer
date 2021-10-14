<i18n lang="yaml">
en:
  devices: "VMS Devices"
  discovery: "Discovery"
  headers:
    name: "Name"
    ip: "IP"
    port: "Port"
    user: "User"
    online: "Online"
    actions: "Actions"
  msg:
    loading: "Loading... Please wait"
    empty: "Empty Devices"
  labels:
    username: "Username"
    password: "Password"
    timeout: "Timeout"
    discovery: "Discovery"
  hints:
    username: "Please enter the ID."
    password: "Please enter the password."
    timeout: "Device discovery timeout (Seconds)"

ko:
  devices: "VMS Devices"
  discovery: "Discovery"
  headers:
    name: "이름"
    ip: "IP"
    port: "포트"
    user: "사용자"
    online: "온라인"
    actions: "관리"
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "장치가 존재하지 않습니다."
  labels:
    username: "사용자명"
    password: "비밀번호"
    timeout: "검색 시간"
    discovery: "탐색"
  hints:
    username: "아이디를 입력해 주세요."
    password: "비밀번호를 입력해 주세요."
    timeout: "장치 검색 제한시간 (초)"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <p :class="subtitleClass">{{ $t('labels.username') }}</p>
    <v-text-field
        dense
        persistent-hint
        type="text"
        autocomplete="off"
        v-model="username"
        :hint="$t('hints.username')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.password') }}</p>
    <v-text-field
        dense
        persistent-hint
        type="password"
        autocomplete="off"
        v-model="password"
        :hint="$t('hints.password')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.timeout') }}</p>
    <v-text-field
        dense
        persistent-hint
        type="number"
        v-model="timeout"
        :hint="$t('hints.timeout')"
    ></v-text-field>

    <v-row class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="onClickSearch">
        {{ $t('labels.discovery') }}
      </v-btn>
    </v-row>

    <v-divider></v-divider>

    <v-data-table
        :items-per-page="itemsPerPage"
        :headers="headers"
        :items="items"
        :loading="loading"
        :loading-text="$t('msg.loading')"
    >
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
import {SUBTITLE_CLASS} from '@/styles/subtitle';

const ITEMS_PER_PAGE = 15;
const DEFAULT_TIMEOUT = 30;

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class AdminVmsDevicesDiscovery extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly itemsPerPage = ITEMS_PER_PAGE;
  readonly breadcrumbs = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: this.$t('devices'),
      disabled: false,
      href: () => this.moveToAdminVmsDevices(),
    },
    {
      text: this.$t('discovery'),
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
      text: this.$t('headers.ip').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'ip',
    },
    {
      text: this.$t('headers.port').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'port',
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

  exploring = false;
  session = '';
  username = '';
  password = '';
  timeout = DEFAULT_TIMEOUT;

  created() {
    this.updateItems();
  }

  updateItems() {
  }

  onClickRefresh() {
  }

  onClickSearch() {
  }

  onClickDevice(item: VmsDeviceA) {
  }
}
</script>
