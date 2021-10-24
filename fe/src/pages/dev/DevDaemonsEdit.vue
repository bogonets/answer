<i18n lang="yaml">
en:
  edit: "Edit"

ko:
  edit: "Edit"
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
export default class DevDaemonsEdit extends VueBase {
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
      text: 'Edit',
      disabled: true,
    },
    {
      text: this.$route.params.daemon,
      disabled: true,
    },
  ];
}
</script>
