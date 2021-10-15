<i18n lang="yaml">
en:
  devices: "VMS Devices"
  new: "New"
  labels:
    name: "Name"
    url: "URL"
    username: "Username"
    password: "Password"
    stream: "Stream"
    protocol: "Protocol"
    test: "Connection Test"
    save: "Save"
  hints:
    name: "The device name to display on the screen."
    url: "Enter the address of the device to be connected."
    username: "Please enter the ID."
    password: "Please enter the password."

ko:
  devices: "VMS Devices"
  new: "New"
  labels:
    name: "이름"
    url: "URL"
    username: "사용자명"
    password: "비밀번호"
    stream: "스트림"
    protocol: "프로토콜"
    test: "연결 확인"
    save: "저장"
  hints:
    name: "화면에 표시할 장치 이름 입니다."
    url: "연결할 장치의 주소를 입력해 주세요."
    username: "아이디를 입력해 주세요."
    password: "비밀번호를 입력해 주세요."
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

    <p :class="subtitleClass">{{ $t('labels.url') }}</p>
    <v-text-field
        dense
        persistent-hint
        type="text"
        autocomplete="off"
        v-model="url"
        :hint="$t('hints.url')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.username') }}</p>
    <v-text-field
        dense
        persistent-hint
        type="text"
        autocomplete="off"
        v-model="username"
        :hint="$t('hints.username')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('labels.password') }}</p>
    <v-text-fieleprd
        dense
        persistent-hint
        type="password"
        autocomplete="off"
        v-model="password"
        :hint="$t('hints.password')"
    ></v-text-fieleprd>

    <p :class="subtitleClass">{{ $t('labels.stream') }}</p>
    <v-radio-group class="mt-2" row hide-details v-model="stream">
      <v-radio
          v-for="stream in streamTypes"
          :key="stream"
          :label="stream"
          :value="stream"
      ></v-radio>
    </v-radio-group>

    <p :class="subtitleClass">{{ $t('labels.protocol') }}</p>
    <v-radio-group class="mt-2" row hide-details v-model="protocol">
      <v-radio
          v-for="proto in protocols"
          :key="proto"
          :label="proto"
          :value="proto"
      ></v-radio>
    </v-radio-group>

    <v-row class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn disabled @click="onClickTest">
        {{ $t('labels.test') }}
      </v-btn>
      <v-btn
          class="ml-2"
          color="primary"
          :disabled="loading"
          :loading="loading"
          @click="onClickSubmit"
      >
        {{ $t('labels.save') }}
      </v-btn>
    </v-row>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import type {VmsCreateDeviceQ} from '@/packet/vms';
import {STREAM_TYPES, PROTOCOLS} from '@/packet/vms';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

const ITEMS_PER_PAGE = 15;

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class MainVmsDevicesNew extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly itemsPerPage = ITEMS_PER_PAGE;
  readonly streamTypes = STREAM_TYPES;
  readonly protocols = PROTOCOLS;

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
      text: this.$t('new'),
      disabled: true,
    },
  ];

  loading = false;
  name = '';
  url = '';
  username = '';
  password = '';
  stream = STREAM_TYPES[0];
  protocol = PROTOCOLS[0];

  onClickTest() {
  }

  onClickSubmit() {
    const body = {
      name: this.name,
      description: '',
      url: this.url,
      onvif_url: '',
      username: this.username,
      password: this.password,
      stream: this.stream,
      protocol: this.protocol,
      active: false,
      daemon: false,
    } as VmsCreateDeviceQ;

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    this.$api2.postVmsDevices(group, project, body)
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
