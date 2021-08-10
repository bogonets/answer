<i18n lang="yaml">
en:
  title: "Groups"
  subtitle: "By creating independent teams, you can create sub-projects."

ko:
  title: "그룹 관리"
  subtitle: "독립적인 팀을 만들어 하위 프로젝트를 만들 수 있습니다."
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
export default class MainAdminGroups extends VueBase {

  navigationItems: object = [];

  created() {
    this.navigationItems = [
      {
        text: 'Admin',
        disabled: false,
        href: this.paths.mainConfigAdminOverview,
      },
      {
        text: 'Groups',
        disabled: true,
      },
    ];
  }
}
</script>
