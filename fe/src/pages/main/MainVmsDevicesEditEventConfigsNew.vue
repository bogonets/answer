<i18n lang="yaml">
en:
  devices: "Devices"
  new: "New"
  msg:
    enable_debugging: "Enable Device Debugging Mode"
    disable_debugging: "Disable Device Debugging Mode"
    failed_start_debugging: "Failed to switch device debugging mode."
    failed_stop_debugging: "Failed to stop device debugging mode."

ko:
  devices: "Devices"
  new: "New"
  msg:
    enable_debugging: "장치 디버깅 모드를 활성화 했습니다."
    disable_debugging: "장치 디버깅 모드를 비활성화 했습니다."
    failed_start_debugging: "장치 디버깅 모드 전환에 실패하였습니다."
    failed_stop_debugging: "장치 디버깅 모드 중단에 실패하였습니다."
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-vms-event-config
        :loading-submit="loadingSubmit"
        :device="device"
        @cancel="onClickCancel"
        @ok="onClickOk"
    ></form-vms-event-config>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import FormVmsEventConfig from '@/components/FormVmsEventConfig.vue';
import type {VmsEventConfigA, VmsCreateEventConfigQ} from '@/packet/vms';
import {VmsDeviceA} from "@/packet/vms";

@Component({
  components: {
    ToolbarBreadcrumbs,
    FormVmsEventConfig,
  }
})
export default class MainVmsDevicesEditEventConfigsNew extends VueBase {
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
      disabled: false,
      href: () => this.moveToMainVmsDevicesEditEvents(),
    },
    {
      text: this.$t('new'),
      disabled: true,
    },
  ];

  loading = false;
  loadingSubmit = false;

  // You cannot directly reference `$route` in the `beforeDestroy` event.
  currentGroup = '';
  currentProject = '';
  currentDevice = '';

  device = {} as VmsDeviceA;

  created() {
    this.requestSetup();
  }

  requestSetup() {
    this.loading = true;
    (async () => {
      await this.setup();
    })();
  }

  async setup() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;

    try {
      await this.$api2.postVmsDeviceProcessDebugStart(group, project, device);
      this.currentGroup = group;
      this.currentProject = project;
      this.currentDevice = device;
      this.toastWarning(this.$t('msg.enable_debugging'));

      this.device = await this.$api2.getVmsDevice(group, project, device);
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  beforeDestroy() {
    const group = this.currentGroup;
    const project = this.currentProject;
    const device = this.currentDevice;
    this.$api2.postVmsDeviceProcessDebugStop(group, project, device)
        .then(() => {
          this.toastSuccess(this.$t('msg.disable_debugging'));
        })
        .catch(() => {
          this.toastWarning(this.$t('msg.failed_stop_debugging'));
        });
  }

  onClickCancel() {
    this.moveToBack();
  }

  onClickOk(event: VmsEventConfigA) {
    const body = {
      sequence: 0,
      category: event.category,
      name: event.name || '',
      enable: event.enable || false,
      extra: event.extra || {},
    } as VmsCreateEventConfigQ;

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.loadingSubmit = true;
    this.$api2.postVmsDeviceEventsConfigs(group, project, device, body)
        .then(() => {
          this.loadingSubmit = false;
          this.toastRequestSuccess();
          this.moveToMainVmsDevicesEditEvents();
        })
        .catch(error => {
          this.loadingSubmit = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
