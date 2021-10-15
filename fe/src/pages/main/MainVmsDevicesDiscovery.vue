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
    session: "Session"
    discovery: "Discovery"
  hints:
    username: "Please enter the ID."
    password: "Please enter the password."
    timeout: "Device discovery timeout (Seconds)"
    session: "A key value to maintain the session."

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
    session: "세션"
    discovery: "탐색"
  hints:
    username: "아이디를 입력해 주세요."
    password: "비밀번호를 입력해 주세요."
    timeout: "장치 검색 제한시간 (초)"
    session: "세션을 유지하기 위한 키 값입니다."
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

    <p :class="subtitleClass">{{ $t('labels.session') }}</p>
    <v-text-field
        append-outer-icon="mdi-refresh"
        dense
        persistent-hint
        type="text"
        v-model="session"
        :hint="$t('hints.session')"
        @click:append-outer="onClickSessionRefresh"
    ></v-text-field>

    <v-row class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="onClickDiscovery">
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
const DEFAULT_TIMEOUT = 3;

const HEX_REF = "0123456789abcdef";

function generateRandomSessionKey(size = 64) {
  let result = '';
  for (let n = 0; n < size; n++) {
    result += HEX_REF[Math.floor(Math.random() * 16)];
  }
  return result;
}

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class MainVmsDevicesDiscovery extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
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
      disabled: false,
      href: () => this.moveToMainVmsDevices(),
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
    this.session = generateRandomSessionKey();
  }

  updateItems() {
  }

  onClickSessionRefresh() {
    this.session = generateRandomSessionKey();
  }

  onClickDiscovery() {
  }

  onClickDevice(item: VmsDeviceA) {
  }
}
</script>
