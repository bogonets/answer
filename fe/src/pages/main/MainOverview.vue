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
export default class MainOverview extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Overview',
      disabled: true,
    },
  ];
}
</script>
