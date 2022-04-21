<i18n lang="yaml">
en:
  devices: 'Devices'
  edit: 'Edit'
  tab:
    info: 'Information'
    live: 'Live'
    record: 'Record'
    events: 'Events'

ko:
  devices: 'Devices'
  edit: 'Edit'
  tab:
    info: '정보'
    live: '실시간'
    record: '녹화'
    events: '이벤트'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-tabs>
      <v-tab to="info">{{ $t('tab.info') }}</v-tab>
      <v-tab to="live">{{ $t('tab.live') }}</v-tab>
      <v-tab to="record">{{ $t('tab.record') }}</v-tab>
      <v-tab to="events">{{ $t('tab.events') }}</v-tab>
    </v-tabs>
    <v-divider></v-divider>

    <router-view></router-view>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';

@Component({
  components: {
    ToolbarBreadcrumbs,
  },
})
export default class MainVmsDevicesEdit extends VueBase {
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
}
</script>
