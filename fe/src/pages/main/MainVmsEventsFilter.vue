<i18n lang="yaml">
en:
  events: "Events"
  filter: "Filter"

ko:
  events: "Events"
  filter: "Filter"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import VueBase from '@/base/VueBase';

// import type {VmsDeviceA, VmsLayoutA, VmsEventA} from '@/packet/vms';
// import moment from 'moment-timezone';

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class MainVmsEventsFilter extends VueBase {
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
      text: this.$t('events'),
      disabled: true,
    },
    {
      text: this.$t('filter'),
      disabled: true,
    },
  ];

}
</script>
