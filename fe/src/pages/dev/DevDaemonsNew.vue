<i18n lang="yaml">
en:
  new: "New"

ko:
  new: "New"
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
import type {DaemonA} from '@/packet/daemon';

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class DevDaemonsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Dev',
      disabled: false,
      href: () => this.moveToDev(),
    },
    {
      text: 'Daemons',
      disabled: false,
      href: () => this.moveToDevDaemons(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];
}
</script>
