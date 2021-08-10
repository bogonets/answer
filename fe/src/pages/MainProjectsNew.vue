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
export default class MainProjectsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToMainProjects(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];
}
</script>
