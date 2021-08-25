<i18n lang="yaml">
en:
  title: "Visual Programming"
  subtitle: "Graph-based visual programming."

ko:
  title: "시각 프로그래밍"
  subtitle: "그래프 기반 시각 프로그래밍."
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
export default class MainProjectVisualProgramming extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToMainProjects(),
    },
    {
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMainProjects(),
    },
    {
      text: 'Visual Programming',
      disabled: true,
    },
  ];

}
</script>
