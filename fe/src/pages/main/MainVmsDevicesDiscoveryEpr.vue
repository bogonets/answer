<i18n lang="yaml">
en:
  devices: 'Devices'
  discovery: 'Discovery'
  epr: 'EPR'
  headers:
    profile: 'Profile'
    token: 'Token'
    stream: 'Stream URI'
    actions: 'Actions'
  msg:
    loading: 'Loading... Please wait'
    empty: 'Empty Devices'
    left_time: 'About {0} seconds remaining'
    after_while: 'After a while it will be done.'
    image_failed: 'Image request failed.'
  labels:
    epr: 'Endpoint Reference'
    onvif_address: 'ONVIF Address'
    server_address: 'Server Address'
    username: 'Username'
    password: 'Password'
    timeout: 'Timeout'
    session: 'Session'
    submit: 'Request'
    security: 'WS-Security'
    protocol: 'Transport Protocol'
    stream: 'Stream Type'
    requesting: 'Requesting'
    cancel: 'Cancel'
    snapshot: 'Snapshot'
    reload: 'Reload'
    close: 'Close'
  security:
    digest: 'Digest'
    text: 'Text'
  hints:
    epr: 'An endpoint is any user device connected to a network.'
    onvif_address: 'ONVIF Device Manager address.'
    server_address: 'Internal server address for media streaming.'
    username: 'Username to access the device.'
    password: 'Password to access the device.'
    timeout: 'Device information request timeout (Seconds)'
    session: 'A key value to maintain the session.'

ko:
  devices: 'Devices'
  discovery: 'Discovery'
  epr: 'EPR'
  headers:
    profile: '프로필'
    token: '토큰'
    stream: '스트림 주소'
    actions: '관리'
  msg:
    loading: '불러오는중 입니다... 잠시만 기다려 주세요.'
    empty: '장치가 존재하지 않습니다.'
    left_time: '남은 시간 약 {0}초'
    after_while: '잠시 후 완료됩니다.'
    image_failed: '이미지 요청에 실패했습니다.'
  labels:
    epr: '엔드포인트 참조'
    onvif_address: 'ONVIF 주소'
    server_address: '내부 서버 주소'
    username: '사용자명'
    password: '비밀번호'
    timeout: '제한 시간'
    session: '세션'
    submit: '요청'
    security: 'WS-Security'
    protocol: '전송 프로토콜'
    stream: '스트림 유형'
    requesting: '요청중 입니다'
    cancel: '취소'
    snapshot: '스냅샷'
    reload: '새로고침'
    close: '닫기'
  security:
    digest: 'Digest'
    text: 'Text'
  hints:
    epr: '엔드포인트는 네트워크에 연결된 모든 사용자 장치입니다.'
    onvif_address: 'ONVIF 장치 관리 주소 입니다.'
    server_address: '미디어 스트리밍을 위한 내부 서버 주소 입니다.'
    username: '장치에 액세스하기 위한 사용자 이름입니다.'
    password: '장치에 액세스하기 위한 비밀번호입니다.'
    timeout: '기기 정보 요청의 제한시간 (초)'
    session: '세션을 유지하기 위한 키 값입니다.'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <p :class="subtitleClass">{{ $t('labels.epr') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="text"
      disabled
      filled
      :value="this.discoveredDevice.epr"
      :hint="$t('hints.epr')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.onvif_address') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="text"
      disabled
      filled
      :value="this.discoveredDevice.address"
      :hint="$t('hints.onvif_address')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.server_address') }}</p>
    <v-text-field
      dense
      persistent-hint
      :value="server_address"
      :hint="$t('hints.server_address')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.username') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="text"
      :disabled="discovering"
      v-model="username"
      :hint="$t('hints.username')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.password') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="password"
      :disabled="discovering"
      v-model="password"
      :hint="$t('hints.password')"
    ></v-text-field>

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

    <p :class="subtitleClass">{{ $t('labels.security') }}</p>
    <v-radio-group
      class="mt-2"
      row
      hide-details
      :disabled="discovering"
      v-model="digest"
    >
      <v-radio :label="$t('security.digest')" :value="true"></v-radio>
      <v-radio :label="$t('security.text')" :value="false"></v-radio>
    </v-radio-group>

    <p :class="subtitleClass">{{ $t('labels.stream') }}</p>
    <v-radio-group
      class="mt-2"
      row
      hide-details
      :disabled="discovering"
      v-model="stream"
    >
      <v-radio
        v-for="stream in streamTypes"
        :key="stream"
        :label="stream"
        :value="stream"
      ></v-radio>
    </v-radio-group>

    <p :class="subtitleClass">{{ $t('labels.protocol') }}</p>
    <v-radio-group
      class="mt-2"
      row
      hide-details
      :disabled="discovering"
      v-model="protocol"
    >
      <v-radio
        v-for="proto in protocols"
        :key="proto"
        :label="proto"
        :value="proto"
      ></v-radio>
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
        <v-icon
          :disabled="!!item.snapshot"
          small
          class="mr-2"
          @click="onClickPreview(item)"
        >
          mdi-image
        </v-icon>
        <v-icon small @click="onClickPickup(item)">mdi-exit-to-app</v-icon>
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
          {{ $t('labels.requesting') }}
        </div>
        <v-divider></v-divider>

        <div class="d-flex flex-column align-center justify-center mt-4">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
          <span class="text-subtitle-2 text--secondary mt-4">
            {{ requestingLabel }}
          </span>
        </div>

        <div class="d-flex flex-column align-center justify-center pa-4">
          <v-btn @click="onClickCancel">
            {{ $t('labels.cancel') }}
          </v-btn>
        </div>
      </v-card>
    </v-dialog>

    <v-dialog v-model="showSnapshotDialog" max-width="640">
      <v-card>
        <div
          class="d-flex flex-column align-center justify-center text-h6 text--secondary pa-2 orange"
        >
          {{ $t('labels.snapshot') }}
        </div>
        <v-progress-linear
          :active="loadingSnapshot"
          :indeterminate="loadingSnapshot"
          color="deep-orange accent-4"
        ></v-progress-linear>

        <div class="d-flex flex-column align-center justify-center mt-4">
          <v-img :src="snapshotData" :alt="$t('msg.image_failed')"></v-img>
        </div>

        <div class="d-flex flex-row align-center justify-center pa-4">
          <v-btn class="mr-2" @click="onClickSnapshotReload">
            <v-icon left>mdi-refresh</v-icon>
            {{ $t('labels.reload') }}
          </v-btn>
          <v-btn @click="onClickSnapshotClose">
            <v-icon left>mdi-close</v-icon>
            {{ $t('labels.close') }}
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
  VmsCreateDeviceQ,
  VmsDiscoveredDeviceA,
  VmsOnvifMediaStreamUriA,
  VmsOnvifMediaStreamUriHeartbeatQ,
  VmsOnvifMediaStreamUriQ,
  VmsOnvifMediaSnapshotQ,
} from '@/packet/vms';
import {
  STREAM_TYPE_RTP_UNICAST,
  STREAM_TYPES,
  PROTOCOL_TCP,
  PROTOCOLS,
  DISCOVERY_HEARTBEAT_INTERVAL,
  SECOND_IN_MILLISECONDS,
  DISCOVERY_LEEWAY_SECONDS,
  DEFAULT_SERVER_ADDRESS,
} from '@/packet/vms';

const ITEMS_PER_PAGE = 15;
const DEFAULT_TIMEOUT_SECONDS = 8;

@Component({
  components: {
    ToolbarBreadcrumbs,
  },
})
export default class MainVmsDevicesDiscoveryEpr extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly itemsPerPage = ITEMS_PER_PAGE;

  readonly streamTypes = STREAM_TYPES;
  readonly protocols = PROTOCOLS;

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
      disabled: false,
      href: () => this.moveToMainVmsDevicesDiscovery(),
    },
    {
      text: this.$t('epr'),
      disabled: true,
    },
  ];

  readonly headers = [
    {
      text: this.$t('headers.profile').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'profile_name',
    },
    {
      text: this.$t('headers.token').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'profile_token',
    },
    {
      text: this.$t('headers.stream').toString(),
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'stream_uri',
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

  discoveredDevice = {} as VmsDiscoveredDeviceA;
  items = [] as Array<VmsOnvifMediaStreamUriA>;

  server_address = DEFAULT_SERVER_ADDRESS;
  username = '';
  password = '';
  timeoutSeconds = DEFAULT_TIMEOUT_SECONDS;
  session = generateRandomSession();
  digest = true;
  stream = STREAM_TYPE_RTP_UNICAST;
  protocol = PROTOCOL_TCP;

  requestedStream = '';
  requestedProtocol = '';

  intervalHandle?: number = undefined;

  showSnapshotDialog = false;
  loadingSnapshot = false;
  snapshotUri = '';
  snapshotContentType = '';
  snapshotEncoding = '';
  snapshotContent = '';

  created() {
    const wds = this.$sessionStore.vmsWds;
    const wd = wds.find(i => i.epr === this.$route.params.epr);
    if (wd) {
      this.discoveredDevice = wd;
    }
  }

  get requestingLabel() {
    if (this.leftSeconds >= 1) {
      return this.$t('msg.left_time', [this.leftSeconds]);
    } else {
      return this.$t('msg.after_while');
    }
  }

  get leftTimeMilliseconds() {
    return (this.timeoutSeconds + DISCOVERY_LEEWAY_SECONDS) * SECOND_IN_MILLISECONDS;
  }

  get existsSnapshot() {
    const contentType = this.snapshotContentType;
    const encoding = this.snapshotEncoding;
    const content = this.snapshotContent;
    return contentType && encoding && content;
  }

  get snapshotData() {
    const contentType = this.snapshotContentType;
    const encoding = this.snapshotEncoding;
    const content = this.snapshotContent;
    return `data:${contentType};${encoding}, ${content}`;
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
    } as VmsOnvifMediaStreamUriHeartbeatQ;

    this.$api2
      .postVmsOnvifMediaHeartbeat(group, project, body)
      .then(item => {
        if (item.done) {
          if (item.medias) {
            this.items = item.medias;
          } else {
            this.items = [] as Array<VmsOnvifMediaStreamUriA>;
          }
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
      address: this.discoveredDevice.address,
      username: this.username,
      password: this.password,
      timeout: this.timeoutSeconds,
      session: this.session,
      digest: this.digest,
      protocol: this.protocol,
      stream: this.stream,
    } as VmsOnvifMediaStreamUriQ;

    this.loading = true;
    this.requestedStream = this.stream;
    this.requestedProtocol = this.protocol;
    this.$api2
      .postVmsOnvifMedia(group, project, body)
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

  requestSnapshot(snapshot_uri: string) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const body = {snapshot_uri: snapshot_uri} as VmsOnvifMediaSnapshotQ;
    this.showSnapshotDialog = true;
    this.loadingSnapshot = true;
    this.snapshotUri = snapshot_uri;
    this.$api2
      .postVmsOnvifMediaSnapshot(group, project, body)
      .then(item => {
        this.snapshotContentType = item.content_type;
        this.snapshotEncoding = item.encoding;
        this.snapshotContent = item.content;
        this.loadingSnapshot = false;
      })
      .catch(error => {
        this.snapshotContentType = '';
        this.snapshotEncoding = '';
        this.snapshotContent = '';
        this.loadingSnapshot = false;
        this.toastRequestFailure(error);
      });
  }

  onClickPreview(item: VmsOnvifMediaStreamUriA) {
    this.requestSnapshot(item.snapshot_uri);
  }

  onClickPickup(item: VmsOnvifMediaStreamUriA) {
    const body = {
      name: item.profile_name,
      description: this.discoveredDevice.epr,
      stream_address: item.stream_uri,
      onvif_address: this.discoveredDevice.address,
      server_address: this.server_address,
      ai_address: '',
      ices: [],
      username: this.username,
      password: this.password,
      stream: this.requestedStream,
      protocol: this.requestedProtocol,
      active: false,
      daemon: false,
    } as VmsCreateDeviceQ;

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    this.$api2
      .postVmsDevices(group, project, body)
      .then(() => {
        this.loading = false;
        this.toastRequestSuccess();
        this.moveToMainVmsDevices();
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  onClickSnapshotReload() {
    this.requestSnapshot(this.snapshotUri);
  }

  onClickSnapshotClose() {
    this.showSnapshotDialog = false;
    this.loadingSnapshot = false;
  }
}
</script>
