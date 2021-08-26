<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation,
  }
})
export default class MainDashboard extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
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
      text: 'Dashboard',
      disabled: true,
    },
  ];
}
</script>
