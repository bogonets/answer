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
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation
  }
})
export default class MainProjectDashboard extends VueBase {

  navigationItems: object = [];

  get group(): string {
    return this.$route.params.group;
  }

  get project(): string {
    return this.$route.params.project;
  }

  created() {
    this.navigationItems = [
      {
        text: 'Projects',
        disabled: false,
        href: this.paths.mainProjects,
      },
      {
        text: this.project,
        disabled: false,
        href: this.paths.mainProjects,
      },
      {
        text: 'Dashboard',
        disabled: true,
      },
    ];
  }
}
</script>
