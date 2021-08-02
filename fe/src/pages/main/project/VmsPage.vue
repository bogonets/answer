<i18n lang="yaml">
en:
  title: "Video management system"
  subtitle: "Browse the files in the project workspace."

ko:
  title: "지능형 영상 분석 시스템"
  subtitle: "프로젝트 작업공간의 파일을 탐색합니다."
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
export default class VmsPage extends VueBase {

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
        text: 'VMS',
        disabled: true,
      },
    ];
  }
}
</script>
