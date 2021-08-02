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
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation
  }
})
export default class LayoutsPage extends VueBase {

  navigationItems: object = [];

  created() {
    this.navigationItems = [
      {
        text: 'Projects',
        disabled: false,
        href: this.paths.mainProjects,
      },
      {
        text: '{project_name}',  // TODO
        disabled: false,
        href: this.paths.mainProjects,
      },
      {
        text: 'Layouts',
        disabled: true,
      },
    ];
  }
}
</script>
