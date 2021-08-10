<i18n lang="yaml">
en:
  title: "Features"
  subtitle: "Add or remove extensible features."

ko:
  title: "기능 관리"
  subtitle: "확장 가능한 기능을 추가하거나 제거합니다."
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
export default class MainAdminFeatures extends VueBase {

  navigationItems: object = [];

  created() {
    this.navigationItems = [
      {
        text: 'Admin',
        disabled: false,
        href: this.paths.mainConfigAdminOverview,
      },
      {
        text: 'Features',
        disabled: true,
      },
    ];
  }
}
</script>
