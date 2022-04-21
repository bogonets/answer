<i18n lang="yaml">
en:
  groups: 'Groups'
  layouts: 'VMS Layouts'
  edit: 'Edit'
  labels:
    name: 'Name'
    description: 'Description'
    index: 'Layout Index'
    device_uid: 'Device UID'
    submit: 'Submit'
    delete: 'Delete a layout'
  hints:
    name: 'The device name to display on the screen.'
    description: 'Detail description.'
    index: 'The order of the layout.'
    device_uid: 'Device UID'
    delete: 'Please be careful! It cannot be recovered.'
  msg:
    delete_confirm: 'Are you sure? Are you really removing this layout?'
  cancel: 'Cancel'
  delete: 'Delete'

ko:
  groups: 'Groups'
  layouts: 'VMS Layouts'
  edit: 'Edit'
  labels:
    name: '이름'
    description: '상세 정보'
    index: '배치 순서'
    device_uid: 'Device UID'
    submit: '제출'
    delete: '레이아웃 제거'
  hints:
    name: '화면에 표시할 장치 이름 입니다.'
    description: '상세한 정보 입니다.'
    index: '레이아웃이 배치되는 순서입니다.'
    device_uid: 'Device UID'
    delete: '주의하세요! 이 명령은 되돌릴 수 없습니다!'
  msg:
    delete_confirm: '이 레이아웃을 정말 제거합니까?'
  cancel: '취소'
  delete: '제거'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <p :class="subtitleClass">{{ $t('labels.name') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="text"
      autocomplete="off"
      :disabled="loading"
      :value="current.name"
      @input="onInputName"
      :hint="$t('hints.name')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.description') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="text"
      autocomplete="off"
      :disabled="loading"
      :value="current.description"
      @input="onInputDescription"
      :hint="$t('hints.description')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.index') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="number"
      autocomplete="off"
      :disabled="loading"
      :value="current.index"
      @input="onInputIndex"
      :hint="$t('hints.index')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.device_uid') }}</p>
    <v-select
      dense
      outlined
      :disabled="loading"
      :value="device"
      @input="onInputDevice"
      :items="devices"
      item-text="name"
      item-value="device_uid"
      return-object
    >
      <template v-slot:item="{item}">
        {{ item.name }}
        <v-chip class="ml-2" x-small outlined color="primary">
          <v-icon left>mdi-identifier</v-icon>
          {{ item.device_uid }}
        </v-chip>
      </template>

      <template v-slot:selection="{item}">
        {{ item.name }}
        <v-chip class="ml-2" x-small outlined color="primary">
          <v-icon left>mdi-identifier</v-icon>
          {{ item.device_uid }}
        </v-chip>
      </template>
    </v-select>

    <v-row class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn
        class="ml-2"
        color="primary"
        :disabled="!modified"
        :loading="loading"
        @click="onClickSubmit"
      >
        {{ $t('labels.submit') }}
      </v-btn>
    </v-row>

    <v-alert class="mt-6" outlined prominent type="error">
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
import type {VmsDeviceA, VmsLayoutA, VmsUpdateLayoutQ} from '@/packet/vms';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import * as _ from 'lodash';

@Component({
  components: {
    ToolbarBreadcrumbs,
  },
})
export default class MainVmsLayoutsEdit extends VueBase {
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
      text: this.$t('layouts'),
      disabled: false,
      href: () => this.moveToMainVmsLayouts(),
    },
    {
      text: this.$t('edit'),
      disabled: true,
    },
    {
      text: this.$route.params.layout,
      disabled: true,
    },
  ];

  loading = false;
  modified = false;

  original = {} as VmsLayoutA;
  current = {} as VmsLayoutA;

  device = {} as VmsDeviceA;
  devices = [] as Array<VmsDeviceA>;

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
    try {
      const group = this.$route.params.group;
      const project = this.$route.params.project;
      const layout = this.$route.params.layout;

      this.devices = await this.$api2.getVmsDevices(group, project);
      const vmsLayout = await this.$api2.getVmsLayout(group, project, layout);

      const findDevice = this.devices.find(i => i.device_uid == vmsLayout.device_uid);
      if (typeof findDevice === 'undefined') {
        this.device = {} as VmsDeviceA;
      } else {
        this.device = findDevice;
      }

      this.original = _.cloneDeep(vmsLayout);
      this.current = _.cloneDeep(vmsLayout);
      this.modified = false;
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  updateModified() {
    this.modified = !_.isEqual(this.original, this.current);
    console.log(`updateModified() -> ${this.modified}`);
  }

  onInputName(value: string) {
    this.current.name = value;
    this.updateModified();
  }

  onInputDescription(value: string) {
    this.current.description = value;
    this.updateModified();
  }

  onInputIndex(value: string) {
    this.current.index = Number.parseInt(value);
    this.updateModified();
  }

  onInputDevice(value: VmsDeviceA) {
    this.device = value;
    this.current.device_uid = value.device_uid;
    this.updateModified();
  }

  onClickSubmit() {
    const body = {
      group_slug: undefined,
      project_slug: undefined,
      name: this.current.name,
      description: this.current.description,
      index: this.current.index,
      device_uid: this.current.device_uid,
    } as VmsUpdateLayoutQ;

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const layout = this.$route.params.layout;
    this.loading = true;
    this.$api2
      .patchVmsLayout(group, project, layout, body)
      .then(() => {
        this.loading = false;
        this.toastRequestSuccess();
        this.original = _.cloneDeep(this.current);
        this.modified = false;
      })
      .catch(error => {
        this.loading = false;
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
    const layout = this.$route.params.layout;
    this.loadingDelete = true;
    this.$api2
      .deleteVmsLayout(group, project, layout)
      .then(() => {
        this.loadingDelete = false;
        this.showDeleteDialog = false;
        this.toastRequestSuccess();
        this.moveToMainVmsLayouts();
      })
      .catch(error => {
        this.loadingDelete = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
