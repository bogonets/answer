<i18n lang="yaml">
en:
  groups: "Groups"
  devices: "VMS Devices"
  edit: "Edit"
  tab:
    info: "Information"
    live: "Live"
    record: "Record"
    event: "Event"

ko:
  groups: "Groups"
  devices: "VMS Devices"
  edit: "Edit"
  tab:
    info: "정보"
    live: "실시간"
    record: "녹화"
    event: "이벤트"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row>
      <v-col>
        <v-tabs v-model="tabIndex">
          <v-tab>{{ $t('tab.info') }}</v-tab>
          <v-tab>{{ $t('tab.live') }}</v-tab>
          <v-tab v-show="false">{{ $t('tab.record') }}</v-tab>
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
            <!-- To release MediaPlayer memory, `v-if` must be used. -->
            <media-player
                v-if="tabIndex === 1"
                hover-system-bar
                hide-controller
                min-height="400px"
                :value="original"
                :group="$route.params.group"
                :project="$route.params.project"
                :device="$route.params.device"
            ></media-player>
          </v-tab-item>

          <v-tab-item>
            <!-- TODO: Record Tab -->
          </v-tab-item>

          <v-tab-item>
<!--            <form-vms-event-configs></form-vms-event-configs>-->
            <table-vms-event-configs
                :items="eventConfigs"
                @click:new="onClickEventConfigNew"
                @click:active="onClickEventConfigItemActive"
                @click:edit="onClickEventConfigEdit"
                @click:delete="onClickEventConfigDelete"
            ></table-vms-event-configs>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import MediaPlayer from '@/media/MediaPlayer.vue';
import FormVmsDevice from '@/components/FormVmsDevice.vue';
import FormVmsEventConfigs from '@/components/FormVmsEventConfigs.vue';
import TableVmsEventConfigs from '@/components/TableVmsEventConfigs.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import type {VmsDeviceA, VmsUpdateDeviceQ} from '@/packet/vms';
import * as _ from 'lodash';
import {VmsEventConfigA, VmsUpdateEventConfigQ} from "@/packet/vms";

@Component({
  components: {
    ToolbarBreadcrumbs,
    MediaPlayer,
    FormVmsDevice,
    FormVmsEventConfigs,
    TableVmsEventConfigs,
  }
})
export default class MainVmsDevicesEdit extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
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
      text: this.$t('edit'),
      disabled: true,
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

  eventConfigs = [] as Array<VmsEventConfigA>;

  showDeleteDialog = false;
  loadingDelete = false;

  created() {
    this.setup();
    this.requestDevice();
  }

  setup() {
    this.loading = true;
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
    const evnet = item.event_config_uid.toString();
    const updateEnableFlag = !item.enable;
    const body = {
      enable: updateEnableFlag,
    } as VmsUpdateEventConfigQ;
    this.$api2.patchVmsEventsConfigsPconfig(group, project, evnet, body)
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
    const evnet = item.event_config_uid.toString();
    this.moveToMainVmsDevicesEditEventConfigsEdit(group, project, device, evnet);
  }

  onClickEventConfigDelete(item: VmsEventConfigA) {
  }
}
</script>
