<i18n lang="yaml">
en:
  title: "Tables"
  subtitle: "You can manage your project's tables."

ko:
  title: "테이블 관리자"
  subtitle: "프로젝트의 테이블을 관리할 수 있습니다."
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
export default class TablesPage extends VueBase {

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
        text: 'Tables',
        disabled: true,
      },
    ];
  }
}
</script>
