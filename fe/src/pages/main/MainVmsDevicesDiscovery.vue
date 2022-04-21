<i18n lang="yaml">
en:
  devices: 'Devices'
  discovery: 'Discovery'
  headers:
    epr: 'EndPoint Reference (EPR)'
    address: 'Address'
    actions: 'Actions'
  msg:
    loading: 'Loading... Please wait'
    empty: 'Empty Devices'
    left_time: 'About {0} seconds remaining'
    after_while: 'After a while it will be done.'
  labels:
    timeout: 'Timeout'
    session: 'Session'
    ip_ver: 'IP Version'
    submit: 'Discovery'
    exploring: 'Exploring'
    cancel: 'Cancel'
  hints:
    timeout: 'Device discovery timeout (Seconds)'
    session: 'A key value to maintain the session.'
  ip_ver:
    ipv4: 'IPv4'
    ipv6: 'IPv6'

ko:
  devices: 'Devices'
  discovery: 'Discovery'
  headers:
    epr: '엔드포인트 참조 (EPR)'
    address: '주소'
    actions: '관리'
  msg:
    loading: '불러오는중 입니다... 잠시만 기다려 주세요.'
    empty: '장치가 존재하지 않습니다.'
    left_time: '남은 시간 약 {0}초'
    after_while: '잠시 후 완료됩니다.'
  labels:
    timeout: '검색 시간'
    session: '세션'
    ip_ver: 'IP 버전'
    submit: '탐색'
    exploring: '탐색중 입니다'
    cancel: '취소'
  hints:
    timeout: '장치 검색 제한시간 (초)'
    session: '세션을 유지하기 위한 키 값입니다.'
  ip_ver:
    ipv4: 'IPv4'
    ipv6: 'IPv6'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <p :class="subtitleClass">{{ $t('labels.timeout') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="number"
      :disabled="discovering"
      v-model="timeoutSeconds"
      :hint="$t('hints.timeout')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.session') }}</p>
    <v-text-field
      append-outer-icon="mdi-refresh"
      dense
      persistent-hint
      type="text"
      :disabled="discovering"
      v-model="session"
      :hint="$t('hints.session')"
      @click:append-outer="onClickSessionRefresh"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.ip_ver') }}</p>
    <v-radio-group class="mt-2" row hide-details :disabled="discovering" v-model="ipv6">
      <v-radio :label="$t('ip_ver.ipv4')" :value="false"></v-radio>
      <v-radio :label="$t('ip_ver.ipv6')" :value="true"></v-radio>
    </v-radio-group>

    <v-row class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn
        color="primary"
        :disabled="discovering"
        :loading="discovering"
        @click="onClickDiscovery"
      >
        {{ $t('labels.submit') }}
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
      <template v-slot:item.actions="{item}">
        <v-icon small class="mr-2" @click="onClickDevice(item)">mdi-exit-to-app</v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('msg.empty') }}
      </template>
    </v-data-table>

    <v-dialog v-model="discovering" max-width="320">
      <v-card>
        <div
          class="d-flex flex-column align-center justify-center text-h6 text--secondary pa-2 orange"
        >
          {{ $t('labels.exploring') }}
        </div>
        <v-divider></v-divider>

        <div class="d-flex flex-column align-center justify-center mt-4">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
          <span class="text-subtitle-2 text--secondary mt-4">
            {{ exploringLabel }}
          </span>
        </div>

        <div class="d-flex flex-column align-center justify-center pa-4">
          <v-btn @click="onClickCancel">
            {{ $t('labels.cancel') }}
          </v-btn>
        </div>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {generateRandomSession} from '@/crypto/session';
import type {
  VmsDiscoveryQ,
  VmsDiscoveredDeviceA,
  VmsDiscoveredHeartbeatQ,
} from '@/packet/vms';
import {
  DISCOVERY_HEARTBEAT_INTERVAL,
  SECOND_IN_MILLISECONDS,
  DISCOVERY_LEEWAY_SECONDS,
} from '@/packet/vms';

const ITEMS_PER_PAGE = 15;
const DEFAULT_TIMEOUT_SECONDS = 3;

@Component({
  components: {
    ToolbarBreadcrumbs,
  },
})
export default class MainVmsDevicesDiscovery extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
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
      text: this.$t('headers.epr').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'epr',
    },
    {
      text: this.$t('headers.address').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'address',
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
  discovering = false;
  beginTime = 0;
  leftSeconds = 0;

  items = [] as Array<VmsDiscoveredDeviceA>;

  session = generateRandomSession();
  timeoutSeconds = DEFAULT_TIMEOUT_SECONDS;
  ipv6 = false;

  intervalHandle?: number = undefined;

  created() {
    this.items = this.$sessionStore.vmsWds;
  }

  beforeDestroy() {
    this.stopHeartbeat();
  }

  get exploringLabel() {
    if (this.leftSeconds >= 1) {
      return this.$t('msg.left_time', [this.leftSeconds]);
    } else {
      return this.$t('msg.after_while');
    }
  }

  get leftTimeMilliseconds() {
    return (this.timeoutSeconds + DISCOVERY_LEEWAY_SECONDS) * SECOND_IN_MILLISECONDS;
  }

  startHeartbeat() {
    this.leftSeconds = Math.floor(this.leftTimeMilliseconds / SECOND_IN_MILLISECONDS);
    if (this.intervalHandle) {
      window.clearInterval(this.intervalHandle);
    }
    this.intervalHandle = window.setInterval(() => {
      this.heartbeat();
    }, DISCOVERY_HEARTBEAT_INTERVAL);
  }

  stopHeartbeat() {
    if (this.intervalHandle) {
      window.clearInterval(this.intervalHandle);
      this.intervalHandle = undefined;
    }
    this.loading = false;
    this.discovering = false;
  }

  heartbeat() {
    const duration = this.leftTimeMilliseconds - (Date.now() - this.beginTime);
    this.leftSeconds = Math.floor(duration / SECOND_IN_MILLISECONDS);

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const body = {
      session: this.session,
    } as VmsDiscoveredHeartbeatQ;

    this.$api2
      .postVmsDiscoveryHeartbeat(group, project, body)
      .then(item => {
        if (item.done) {
          if (item.devices) {
            this.items = item.devices;
          } else {
            this.items = [] as Array<VmsDiscoveredDeviceA>;
          }
          this.$sessionStore.vmsWds = this.items;
          this.stopHeartbeat();
        }
      })
      .catch(error => {
        this.stopHeartbeat();
        this.toastRequestFailure(error);
      });
  }

  onClickSessionRefresh() {
    this.session = generateRandomSession();
  }

  onClickDiscovery() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const body = {
      timeout: this.timeoutSeconds,
      session: this.session,
      ipv6: this.ipv6,
    } as VmsDiscoveryQ;

    this.loading = true;
    this.$api2
      .postVmsDiscovery(group, project, body)
      .then(() => {
        this.loading = false;
        this.discovering = true;
        this.beginTime = Date.now();
        this.startHeartbeat();
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  onClickCancel() {
    this.stopHeartbeat();
  }

  onClickDevice(item: VmsDiscoveredDeviceA) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const epr = item.epr;
    this.moveToMainVmsDevicesDiscoveryEpr(group, project, epr);
  }
}
</script>
