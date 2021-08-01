<i18n lang="yaml">
en:
  title: "Settings"
  subtitle: "Modify environment variables used in the system."

ko:
  title: "환경설정"
  subtitle: "시스템에서 사용되는 환경변수를 수정합니다."
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
    ToolbarNavigation,
  }
})
export default class SettingsPage extends VueBase {

  navigationItems: object = [];

  created() {
    this.navigationItems = [
      {
        text: 'Admin',
        disabled: false,
        href: this.paths.mainConfigAdminOverview,
      },
      {
        text: 'Settings',
        disabled: true,
      },
    ];
  }
}
</script>
