<i18n lang="yaml">
en:
  title: "Layout Manager"
  subtitle: "Manage customizable widgets."

ko:
  title: "레이아웃 관리자"
  subtitle: "사용자 정의 가능한 위젯을 관리합니다."
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
export default class MainProjectLayouts extends VueBase {
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
      text: 'Layouts',
      disabled: true,
    },
  ];
}
</script>
