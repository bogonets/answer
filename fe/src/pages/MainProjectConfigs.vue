<i18n lang="yaml">
en:
  title: "Project Settings"
  subtitle: ""

ko:
  title: "프로젝트 설정"
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
    ToolbarNavigation,
  }
})
export default class MainProjectConfigs extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToMainProjects(),
    },
    {
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMainProject(),
    },
    {
      text: 'Settings',
      disabled: true,
    },
  ];
}
</script>
