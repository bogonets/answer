<i18n lang="yaml">
en:
  title: "Task Manager"
  subtitle: "You can manage your own tasks."

ko:
  title: "테스크 관리자"
  subtitle: "테스크를 직접 관리할수 있습니다."
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
export default class MainProjectTasks extends VueBase {
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
      text: 'Tasks',
      disabled: true,
    },
  ];
}
</script>
