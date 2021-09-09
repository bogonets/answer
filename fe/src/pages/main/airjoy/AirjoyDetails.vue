<i18n lang="yaml">
en:
  groups: "Groups"
  airjoy_table: "Table"

ko:
  groups: "Groups"
  airjoy_table: "Table"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"
    ></toolbar-breadcrumbs>
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
export default class AirjoyDetails extends VueBase {
  private readonly breadcrumbs = [
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
      text: this.$t('airjoy_table'),
      disabled: false,
      href: () => this.moveToMainAirjoyTable(),
    },
    {
      text: this.$route.params.airjoy,
      disabled: true,
    },
  ];
}
</script>
