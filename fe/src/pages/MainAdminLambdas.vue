<i18n lang="yaml">
en:
  title: "Lambdas"
  subtitle: "You can add, edit and remove lambdas."

ko:
  title: "람다 관리"
  subtitle: "람다를 추가하거나 편집 및 제거할 수 있습니다."
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
    ToolbarNavigation,
  }
})
export default class MainAdminLambdas extends VueBase {

  navigationItems: object = [];

  created() {
    this.navigationItems = [
      {
        text: 'Admin',
        disabled: false,
        href: this.paths.mainConfigAdminOverview,
      },
      {
        text: 'Lambdas',
        disabled: true,
      },
    ];
  }
}
</script>
