<i18n lang="yaml">
en:
  title: "Overview"
  subtitle: "Prints a summary of the system status."

ko:
  title: "개요"
  subtitle: "시스템의 상태를 요약하여 출력합니다."
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

  </v-container>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation
  }
})
export default class OverviewPage extends VueBase {

  navigationItems: object = [];

  created() {
    this.navigationItems = [
      {
        text: 'Admin',
        disabled: false,
        href: this.paths.mainConfigAdminOverview,
      },
      {
        text: 'Overview',
        disabled: true,
      },
    ];
  }
}
</script>
