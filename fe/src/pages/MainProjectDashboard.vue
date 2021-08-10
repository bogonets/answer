<i18n lang="yaml">
en:
  title: "Project Dashboard"
  subtitle: ""

ko:
  title: "프로젝트 대시보드"
  subtitle: ""
</i18n>

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
    ToolbarNavigation
  }
})
export default class MainProjectDashboard extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToMainProjects(),
    },
    {
      text: this.currentProjectName,
      disabled: false,
      href: () => this.moveToMainProjects(),
    },
    {
      text: 'Dashboard',
      disabled: true,
    },
  ];
}
</script>
