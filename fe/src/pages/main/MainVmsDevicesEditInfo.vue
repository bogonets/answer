<template>
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
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import FormVmsDevice from '@/components/FormVmsDevice.vue';
import type {VmsDeviceA, VmsUpdateDeviceQ} from '@/packet/vms';
import * as _ from 'lodash';

@Component({
  components: {
    FormVmsDevice,
  },
})
export default class MainVmsDevicesEditInfo extends VueBase {
  loading = false;
  original = {} as VmsDeviceA;
  current = {} as VmsDeviceA;
  loadingSubmit = false;
  modified = false;

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
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  requestDevice() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.loading = true;
    this.$api2
      .getVmsDevice(group, project, device)
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
    this.$api2
      .patchVmsDevice(group, project, device, body)
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
    this.$api2
      .deleteVmsDevice(group, project, device)
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
}
</script>
