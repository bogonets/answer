<i18n lang="yaml">
en:
  devices: 'Devices'
  headers:
    detail: 'Detail'
  subheaders:
    detail: 'Detailed information about this config.'
  labels:
    created_at: 'Created At'
    updated_at: 'Updated At'
    delete: 'Delete a config'
  hints:
    delete: 'Please be careful! It cannot be recovered.'
  msg:
    enable_debugging: 'Enable Device Debugging Mode'
    disable_debugging: 'Disable Device Debugging Mode'
    failed_start_debugging: 'Failed to switch device debugging mode.'
    failed_stop_debugging: 'Failed to stop device debugging mode.'
    delete_confirm: 'Are you sure? Are you really removing this config?'
  cancel: 'Cancel'
  delete: 'Delete'

ko:
  devices: 'Devices'
  headers:
    detail: '상세 정보'
  subheaders:
    detail: '이 설정에 대한 자세한 정보입니다.'
  labels:
    created_at: '설정 생성일'
    updated_at: '설정 갱신일'
    delete: '설정 제거'
  hints:
    delete: '주의하세요! 이 명령은 되돌릴 수 없습니다!'
  msg:
    enable_debugging: '장치 디버깅 모드를 활성화 했습니다.'
    disable_debugging: '장치 디버깅 모드를 비활성화 했습니다.'
    failed_start_debugging: '장치 디버깅 모드 전환에 실패하였습니다.'
    failed_stop_debugging: '장치 디버깅 모드 중단에 실패하였습니다.'
    delete_confirm: '이 설정을 정말 제거합니까?'
  cancel: '취소'
  delete: '제거'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-vms-event-config
      disable-category
      :loading-submit="loadingSubmit"
      :disable-submit-button="!modified"
      :device="device"
      :value="current"
      @input="onInputCurrent"
      @cancel="onClickCancel"
      @ok="onClickOk"
    ></form-vms-event-config>

    <left-title :header="$t('headers.detail')" :subheader="$t('subheaders.detail')">
      <v-card outlined>
        <v-simple-table class="elevation-1">
          <template v-slot:default>
            <tbody>
              <tr>
                <td>{{ $t('labels.created_at') }}</td>
                <td>{{ createdAt }}</td>
              </tr>
              <tr>
                <td>{{ $t('labels.updated_at') }}</td>
                <td>{{ updatedAt }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card>
    </left-title>

    <v-alert outlined prominent class="ma-4" type="error">
      <v-row align="center" class="pl-4">
        <v-col>
          <v-row>
            <h6 class="text-h6">{{ $t('labels.delete') }}</h6>
          </v-row>
          <v-row>
            <span class="text-body-2">{{ $t('hints.delete') }}</span>
          </v-row>
        </v-col>
        <v-col class="shrink">
          <v-btn color="error" @click.stop="onClickDelete">
            {{ $t('delete') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="320">
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
          <v-btn @click="onClickDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn :loading="loadingDelete" color="error" @click="onClickDeleteOk">
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
import FormVmsEventConfig from '@/components/FormVmsEventConfig.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import type {VmsEventConfigA} from '@/packet/vms';
import {iso8601ToLocal} from '@/chrono/iso8601';
import * as _ from 'lodash';
import {VmsDeviceA} from '@/packet/vms';

@Component({
  components: {
    ToolbarBreadcrumbs,
    FormVmsEventConfig,
    LeftTitle,
  },
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
      text: this.$route.params.device,
      disabled: false,
      href: () => this.moveToMainVmsDevicesEditEvents(),
    },
    {
      text: this.$route.params.config,
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

  current = {} as VmsEventConfigA;
  original = {} as VmsEventConfigA;
  modified = false;

  showDeleteDialog = false;
  loadingDelete = false;

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
    const config = this.$route.params.config;

    try {
      await this.$api2.postVmsDeviceProcessDebugStart(group, project, device);
      this.currentGroup = group;
      this.currentProject = project;
      this.currentDevice = device;
      this.toastWarning(this.$t('msg.enable_debugging'));

      this.device = await this.$api2.getVmsDevice(group, project, device);
      this.original = await this.$api2.getVmsDeviceEventsConfigsPconfig(
        group,
        project,
        device,
        config,
      );
      this.current = _.cloneDeep(this.original);
      this.modified = false;
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
    this.$api2
      .postVmsDeviceProcessDebugStop(group, project, device)
      .then(() => {
        this.toastSuccess(this.$t('msg.disable_debugging'));
      })
      .catch(() => {
        this.toastWarning(this.$t('msg.failed_stop_debugging'));
      });
  }

  get createdAt() {
    return iso8601ToLocal(this.original.created_at || '');
  }

  get updatedAt() {
    return iso8601ToLocal(this.original.updated_at || '');
  }

  onInputCurrent(item: VmsEventConfigA) {
    this.current = item;
    this.modified = !_.isEqual(this.original, this.current);
  }

  onClickCancel() {
    this.moveToBack();
  }

  onClickOk(item: VmsEventConfigA) {
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
    //       this.moveToMainVmsDevicesEditEvents();
    //     })
    //     .catch(error => {
    //       this.loadingSubmit = false;
    //       this.toastRequestFailure(error);
    //     });
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
    const config = this.$route.params.config;

    this.loadingDelete = true;
    this.$api2
      .deleteVmsDeviceEventsConfigsPconfig(group, project, device, config)
      .then(() => {
        this.loadingDelete = false;
        this.showDeleteDialog = false;
        this.toastRequestSuccess();
        this.moveToMainVmsDevicesEditEvents();
      })
      .catch(error => {
        this.loadingDelete = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
