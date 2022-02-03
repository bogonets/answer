<i18n lang="yaml">
en:
  devices: "Devices"
  edit: "Edit"
  tab:
    info: "Information"
    live: "Live"
    record: "Record"
    event: "Event"
  labels:
    delete: "Delete a config"
  msg:
    delete_confirm: "Are you sure? Are you really removing this config?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  devices: "Devices"
  edit: "Edit"
  tab:
    info: "정보"
    live: "실시간"
    record: "녹화"
    event: "이벤트"
  labels:
    delete: "설정 제거"
  msg:
    delete_confirm: "이 설정을 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-tabs v-model="tabIndex">
      <v-tab>{{ $t('tab.info') }}</v-tab>
      <v-tab>{{ $t('tab.live') }}</v-tab>
      <v-tab>{{ $t('tab.record') }}</v-tab>
      <v-tab>{{ $t('tab.event') }}</v-tab>
    </v-tabs>
    <v-divider></v-divider>

    <v-tabs-items v-model="tabIndex">
      <v-tab-item>
        <form-vms-device
            hide-cancel-button
            :disabled="loading"
            :disable-submit-button="!modified"
            :loading-submit="loadingSubmit"
            :show-delete-dialog="showDeleteDialog"
            :loading-delete="loadingDelete"
            :value="current"
            @input="onUpdateCurrent"
            @ok="onClickOk"
            @delete:show="onClickDelete"
            @delete:cancel="onClickDeleteCancel"
            @delete:ok="onClickDeleteOk"
        ></form-vms-device>
      </v-tab-item>

      <v-tab-item>
        <!-- [IMPORTANT] To release MediaPlayer memory, `v-if` must be used. -->
        <media-player
            v-if="tabIndex === 1"
            hover-system-bar
            hide-controller
            :value="original"
            :group="$route.params.group"
            :project="$route.params.project"
            :device="$route.params.device"
        ></media-player>
      </v-tab-item>

      <v-tab-item>
        <form-vms-record
            :group="$route.params.group"
            :project="$route.params.project"
            :device="$route.params.device"
        ></form-vms-record>
      </v-tab-item>

      <v-tab-item>
        <table-vms-event-configs
            :items="eventConfigs"
            :loading="loadingEventConfigs"
            @click:new="onClickEventConfigNew"
            @click:active="onClickEventConfigItemActive"
            @click:edit="onClickEventConfigEdit"
            @click:delete="onClickEventConfigDelete"
        ></table-vms-event-configs>
      </v-tab-item>
    </v-tabs-items>

    <!-- Delete dialog. -->
    <v-dialog v-model="showEventConfigDeleteDialog" max-width="320">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('labels.delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('msg.delete_confirm') }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickEventConfigDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn
              color="error"
              :loading="loadingEventConfigDelete"
              @click="onClickEventConfigDeleteOk"
          >
            {{ $t('delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import MediaPlayer from '@/media/MediaPlayer.vue';
import FormVmsDevice from '@/components/FormVmsDevice.vue';
import FormVmsRecord from '@/components/FormVmsRecord.vue';
import TableVmsEventConfigs from '@/components/TableVmsEventConfigs.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import type {
  VmsDeviceA,
  VmsUpdateDeviceQ,
  VmsEventConfigA,
  VmsUpdateEventConfigQ,
} from '@/packet/vms';
import * as _ from 'lodash';

@Component({
  components: {
    ToolbarBreadcrumbs,
    MediaPlayer,
    FormVmsDevice,
    FormVmsRecord,
    TableVmsEventConfigs,
  }
})
export default class MainVmsDevicesEdit extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
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
      text: this.$route.params.device,
      disabled: true,
    },
  ];

  tabIndex = 0;

  loading = false;
  original = {} as VmsDeviceA;
  current = {} as VmsDeviceA;
  loadingSubmit = false;
  modified = false;

  loadingEventConfigs = false;
  eventConfigs = [] as Array<VmsEventConfigA>;

  showDeleteDialog = false;
  loadingDelete = false;

  showEventConfigDeleteDialog = false;
  loadingEventConfigDelete = false;
  eventConfigCandidate = 0;

  created() {
    this.setup();
    this.requestDevice();
  }

  mounted() {
    if (this.$route.params.tab) {
      try {
        this.tabIndex = Number.parseInt(this.$route.params.tab);
      } catch (error) {
        this.tabIndex = 0;
      }
    } else {
      this.tabIndex = 0;
    }
  }

  setup() {
    this.loading = true;
    this.loadingEventConfigs = true;
    (async () => {
      await this.requestSetup();
    })();
  }

  async requestSetup() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;

    try {
      this.original = await this.$api2.getVmsDevice(group, project, device);
      this.current = _.cloneDeep(this.original);
      this.modified = false;

      this.eventConfigs = await this.$api2.getVmsDeviceEventsConfigs(
          group, project, device
      );
    } catch (error) {
    } finally {
      this.loading = false;
      this.loadingEventConfigs = false;
    }
  }

  requestDevice() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.loading = true;
    this.$api2.getVmsDevice(group, project, device)
        .then(item => {
          this.original = _.cloneDeep(item);
          this.current = _.cloneDeep(item);
          this.loading = false;
          this.modified = false;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  requestEventConfigs() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;

    this.loadingEventConfigs = true;
    this.$api2.getVmsDeviceEventsConfigs(group, project, device)
        .then(items => {
          this.loadingEventConfigs = false;
          this.eventConfigs = items;
        })
        .catch(error => {
          this.loadingEventConfigs = false;
          this.toastRequestFailure(error);
        });
  }

  onUpdateCurrent(value: VmsDeviceA) {
    this.current = value;
    this.modified = !_.isEqual(this.original, this.current);
  }

  onClickOk(value: VmsDeviceA) {
    const body = {
      name: value.name,
      description: value.description,
      stream_address: value.stream_address,
      onvif_address: value.onvif_address,
      server_address: value.server_address,
      ai_address: value.ai_address,
      ices: value.ices,
      username: value.username,
      password: value.password,
      stream: value.stream,
      protocol: value.protocol,
      active: value.active,
      daemon: value.daemon,
    } as VmsUpdateDeviceQ;

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.loadingSubmit = true;
    this.$api2.patchVmsDevice(group, project, device, body)
        .then(() => {
          this.loadingSubmit = true;
          this.toastRequestSuccess();
          this.requestDevice();
        })
        .catch(error => {
          this.loadingSubmit = false;
          this.toastRequestFailure(error);
        });
  }

  onClickDelete() {
    this.showDeleteDialog = true;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.loadingDelete = true;
    this.$api2.deleteVmsDevice(group, project, device)
        .then(() => {
          this.loadingDelete = false;
          this.showDeleteDialog = false;
          this.toastRequestSuccess();
          this.moveToMainVmsDevices();
        })
        .catch(error => {
          this.loadingDelete = false;
          this.toastRequestFailure(error);
        });
  }

  onClickEventConfigNew() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.moveToMainVmsDevicesEditEventConfigsNew(group, project, device);
  }

  onClickEventConfigItemActive(item: VmsEventConfigA) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const config = item.event_config_uid.toString();
    const updateEnableFlag = !item.enable;
    const body = {
      enable: updateEnableFlag,
    } as VmsUpdateEventConfigQ;
    this.$api2.patchVmsDeviceEventsConfigsPconfig(group, project, device, config, body)
        .then(() => {
          item.enable = updateEnableFlag;
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  onClickEventConfigEdit(item: VmsEventConfigA) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const config = item.event_config_uid.toString();
    this.moveToMainVmsDevicesEditEventConfigsEdit(group, project, device, config);
  }

  onClickEventConfigDelete(item: VmsEventConfigA) {
    this.showEventConfigDeleteDialog = true;
    this.eventConfigCandidate = item.event_config_uid;
  }

  onClickEventConfigDeleteCancel() {
    this.showEventConfigDeleteDialog = false;
  }

  onClickEventConfigDeleteOk() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const config = this.eventConfigCandidate.toString();

    this.loadingEventConfigDelete = true;
    this.$api2.deleteVmsDeviceEventsConfigsPconfig(group, project, device, config)
        .then(() => {
          this.showEventConfigDeleteDialog = false;
          this.loadingEventConfigDelete = false;
          this.toastRequestSuccess();
          this.requestEventConfigs();
        })
        .catch(error => {
          this.loadingEventConfigDelete = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
