<i18n lang="yaml">
en:
  title: "File Browser"
  subtitle: "Browse the files in the project workspace."

ko:
  title: "파일 탐색기"
  subtitle: "프로젝트 작업공간의 파일을 탐색합니다."
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
export default class MainProjectFiles extends VueBase {
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
      text: 'Files',
      disabled: true,
    },
  ];
}
</script>
