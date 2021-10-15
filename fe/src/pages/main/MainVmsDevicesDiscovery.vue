<i18n lang="yaml">
en:
  devices: "VMS Devices"
  discovery: "Discovery"
  on: "ON"
  off: "OFF"
  headers:
    epr: "EndPoint Reference (EPR)"
    address: "Address"
  msg:
    loading: "Loading... Please wait"
    empty: "Empty Devices"
    left_time: "About {0} seconds remaining"
    after_while: "After a while it will be done."
  labels:
    timeout: "Timeout"
    session: "Session"
    ipv6: "IPv6"
    discovery: "Discovery"
    exploring: "Exploring"
    cancel: "Cancel"
  hints:
    timeout: "Device discovery timeout (Seconds)"
    session: "A key value to maintain the session."

ko:
  devices: "VMS Devices"
  discovery: "Discovery"
  on: "ON"
  off: "OFF"
  headers:
    epr: "엔드포인트 참조 (EPR)"
    address: "주소"
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "장치가 존재하지 않습니다."
    left_time: "남은 시간 약 {0}초"
    after_while: "잠시 후 완료됩니다."
  labels:
    timeout: "검색 시간"
    session: "세션"
    ipv6: "IPv6"
    discovery: "탐색"
    exploring: "탐색중 입니다"
    cancel: "취소"
  hints:
    timeout: "장치 검색 제한시간 (초)"
    session: "세션을 유지하기 위한 키 값입니다."
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

    <p :class="subtitleClass">{{ $t('labels.ipv6') }}</p>
    <v-radio-group
        class="mt-2"
        row
        hide-details
        :disabled="discovering"
        v-model="ipv6"
    >
      <v-radio :label="$t('off')" :value="false"></v-radio>
      <v-radio :label="$t('on')" :value="true"></v-radio>
    </v-radio-group>

    <v-row class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn
          color="primary"
          :disabled="discovering"
          :loading="discovering"
          @click="onClickDiscovery">
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

    <v-dialog v-model="discovering" max-width="320">
      <v-card>
        <div class="d-flex flex-column align-center justify-center text-h6 text--secondary pa-2 orange">
          {{ $t('labels.exploring') }}
        </div>
        <v-divider></v-divider>

        <div class="d-flex flex-column align-center justify-center mt-4">
          <v-progress-circular
              indeterminate
              color="primary"
          ></v-progress-circular>
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
  ];

  loading = false;
  discovering = false;
  beginTime = 0;
  leftSeconds = 0;

  items = [] as Array<VmsDiscoveredDeviceA>;

  exploring = false;
  session = '';
  timeoutSeconds = DEFAULT_TIMEOUT_SECONDS;
  ipv6 = false;

  intervalHandle?: number = undefined;

  created() {
    this.session = generateRandomSessionKey();
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

    this.$api2.postVmsDiscoveryHeartbeat(group, project, body)
        .then(item => {
          if (item.done) {
            this.stopHeartbeat();
            if (item.devices) {
              this.items = item.devices;
            } else {
              this.items = [] as Array<VmsDiscoveredDeviceA>;
            }
          }
        })
        .catch(error => {
          this.stopHeartbeat();
          this.toastRequestFailure(error);
        });
  }

  onClickSessionRefresh() {
    this.session = generateRandomSessionKey();
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
    this.$api2.postVmsDiscovery(group, project, body)
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

  onClickDevice(item) {
  }
}
</script>
