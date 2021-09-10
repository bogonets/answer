<i18n lang="yaml">
en:
  admin: "Admin"
  plugins: "Plugins"

ko:
  admin: "Admin"
  plugins: "Plugins"
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
export default class AdminPlugins extends VueBase {
  private readonly navigationItems = [
    {
      text: this.$t('admin'),
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: this.$t('plugins'),
      disabled: true,
    },
  ];
}
</script>
