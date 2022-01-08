<i18n lang="yaml">
en:
  groups: "Groups"
  devices: "VMS Devices"
  edit: "Edit/{0}"
  msg:
    enable_debugging: "Enable Device Debugging Mode"
    disable_debugging: "Disable Device Debugging Mode"
    failed_start_debugging: "Failed to switch device debugging mode."
    failed_stop_debugging: "Failed to stop device debugging mode."

ko:
  groups: "Groups"
  devices: "VMS Devices"
  edit: "Edit/{0}"
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
        disable-device
        :device="device"
        :devices="devices"
        :loading-submit="loadingSubmit"
        @cancel="onClickCancel"
        @ok="onClickOk"
    ></form-vms-event-config>

  </v-container>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import FormVmsEventConfig from '@/components/FormVmsEventConfig.vue';
import type {VmsEventConfigA} from '@/packet/vms';
import {VmsCreateEventConfigQ, VmsDeviceA} from "@/packet/vms";

@Component({
  components: {
    ToolbarBreadcrumbs,
    FormVmsEventConfig,
  }
})
export default class MainVmsDevicesEditEventConfigsEdit extends VueBase {
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
      text: this.$t('edit', [this.$route.params.device]),
      disabled: true,
    },
    {
      text: this.$t('event_config'),
      disabled: false,
      href: () => this.moveToMainVmsDevicesEditEventConfigs(),
    },
    {
      text: this.$t('edit', [this.$route.params.event]),
      disabled: true,
    },
  ];

  loading = false;
  loadingSubmit = false;
  device = {} as VmsDeviceA;
  devices = [] as Array<VmsDeviceA>;

  // You cannot directly reference `$route` in the `beforeDestroy` event.
  currentGroup = '';
  currentProject = '';
  currentDevice = '';

  current = {} as VmsEventConfigA;
  original = {} as VmsEventConfigA;
  modified = false;

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
      this.devices = await this.$api2.getVmsDevices(group, project);
      const device_uid = Number.parseInt(device);
      const findDevice = this.devices.find(i => i.device_uid == device_uid);
      if (typeof findDevice === 'undefined') {
        this.device = {} as VmsDeviceA;
      } else {
        this.device = findDevice;
      }

      await this.$api2.postVmsDeviceProcessDebugStart(group, project, device);
      this.currentGroup = this.$route.params.group;
      this.currentProject = this.$route.params.project;
      this.currentDevice = this.$route.params.device;
      this.toastWarning(this.$t('msg.enable_debugging'));
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
    // const body = {
    //   sequence: 0,
    //   device_uid: this.device.device_uid,
    //   category: event.category,
    //   name: event.name || '',
    //   enable: event.enable || false,
    //   extra: event.extra || {},
    // } as VmsCreateEventConfigQ;
    //
    // const group = this.$route.params.group;
    // const project = this.$route.params.project;
    // const device = this.$route.params.device;
    // this.loadingSubmit = true;
    // this.$api2.postVmsDeviceEventsConfigs(group, project, device, body)
    //     .then(() => {
    //       this.loadingSubmit = false;
    //       this.toastRequestSuccess();
    //       this.moveToMainVmsDevicesEditEventConfigs();
    //     })
    //     .catch(error => {
    //       this.loadingSubmit = false;
    //       this.toastRequestFailure(error);
    //     });
  }
}
</script>
