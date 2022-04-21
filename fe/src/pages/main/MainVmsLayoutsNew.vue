<i18n lang="yaml">
en:
  groups: 'Groups'
  layouts: 'VMS Layouts'
  new: 'New'
  labels:
    name: 'Name'
    description: 'Description'
    index: 'Layout Index'
    device_uid: 'Device UID'
    submit: 'Submit'
  hints:
    name: 'The device name to display on the screen.'
    description: 'Detailed human-readable description.'
    index: 'The order of the layout.'
    device_uid: 'The UID of the device to assign to the layout.'

ko:
  groups: 'Groups'
  layouts: 'VMS Layouts'
  new: 'New'
  labels:
    name: '이름'
    description: '상세 정보'
    index: '배치 순서'
    device_uid: '장치 UID'
    submit: '제출'
  hints:
    name: '화면에 표시할 장치 이름 입니다.'
    description: '사람이 읽을 수 있는 상세한 설명.'
    index: '레이아웃이 배치되는 순서입니다.'
    device_uid: '레이아웃에 할당할 장치의 UID.'
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
      v-model="name"
      :hint="$t('hints.name')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.description') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="text"
      autocomplete="off"
      v-model="description"
      :hint="$t('hints.description')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.index') }}</p>
    <v-text-field
      dense
      persistent-hint
      type="number"
      autocomplete="off"
      v-model="index"
      :hint="$t('hints.index')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.device_uid') }}</p>
    <v-select
      dense
      outlined
      v-model="device"
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
        :disabled="loading"
        :loading="loading"
        @click="onClickSubmit"
      >
        {{ $t('labels.submit') }}
      </v-btn>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import type {VmsDeviceA, VmsCreateLayoutQ} from '@/packet/vms';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

@Component({
  components: {
    ToolbarBreadcrumbs,
  },
})
export default class MainVmsLayoutsNew extends VueBase {
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
      text: this.$t('new'),
      disabled: true,
    },
  ];

  loading = false;
  name = '';
  description = '';
  index = 0;

  device = {} as VmsDeviceA;
  devices = [] as Array<VmsDeviceA>;

  created() {
    this.updateDevices();
  }

  updateDevices() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    this.$api2
      .getVmsDevices(group, project)
      .then(items => {
        this.loading = false;
        this.devices = items;
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  onClickSubmit() {
    if (typeof this.device.device_uid === 'undefined') {
      throw TypeError('Device is not selected.');
    }

    const body = {
      name: this.name,
      description: this.description,
      index: this.index,
      device_uid: this.device.device_uid,
    } as VmsCreateLayoutQ;

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    this.$api2
      .postVmsLayouts(group, project, body)
      .then(() => {
        this.loading = false;
        this.toastRequestSuccess();
        this.moveToBack();
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
