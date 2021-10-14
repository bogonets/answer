<i18n lang="yaml">
en:
  devices: "VMS Devices"
  new: "New"
  labels:
    url: "URL"
    username: "Username"
    password: "Password"
    submit: "Submit"
  hints:
    url: "Enter the address of the device to be connected."
    username: "Please enter the ID."
    password: "Please enter the password."

ko:
  devices: "VMS Devices"
  new: "New"
  labels:
    url: "URL"
    username: "사용자명"
    password: "비밀번호"
    submit: "제출"
  hints:
    url: "연결할 장치의 주소를 입력해 주세요."
    username: "아이디를 입력해 주세요."
    password: "비밀번호를 입력해 주세요."
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

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
    <v-text-field
        dense
        persistent-hint
        type="password"
        autocomplete="off"
        v-model="password"
        :hint="$t('hints.password')"
    ></v-text-field>

    <v-row class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn color="primary" @click="onClickSubmit">
        {{ $t('labels.submit') }}
      </v-btn>
    </v-row>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import type {VmsCreateDeviceQ} from '@/packet/vms';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

const ITEMS_PER_PAGE = 15;

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class AdminVmsDevicesNew extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly itemsPerPage = ITEMS_PER_PAGE;
  readonly breadcrumbs = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: this.$t('devices'),
      disabled: false,
      href: () => this.moveToAdminVmsDevices(),
    },
    {
      text: this.$t('new'),
      disabled: true,
    },
  ];

  url = '';
  username = '';
  password = '';

  onClickSubmit() {
    const body = {
      url: this.url,
      username: this.username,
      password: this.password,
    } as VmsCreateDeviceQ;
  }
}
</script>
