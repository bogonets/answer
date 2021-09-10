<i18n lang="yaml">
en:
  airjoy: "Airjoy"
  devices: "Devices"

ko:
  airjoy: "에어조이"
  devices: "장치 관리"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class AdminAirjoyDevices extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: this.$t('airjoy').toString(),
      disabled: true,
    },
    {
      text: this.$t('devices').toString(),
      disabled: true,
    },
  ];
}
</script>
