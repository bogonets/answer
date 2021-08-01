<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

  </v-container>
</template>

<script lang="ts">
import { Component, Prop } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation,
  }
})
export default class UserEditPage extends VueBase {

  @Prop({type: String, default: ''})
  readonly username!: string;

  navigationItems: object = [];

  created() {
    this.navigationItems = [
      {
        text: 'Admin',
        disabled: false,
        href: this.paths.mainConfigAdminOverview,
      },
      {
        text: 'Users',
        disabled: false,
        href: this.paths.mainConfigAdminUsers,
      },
      {
        text: 'Edit',
        disabled: true,
      },
    ];
  }
}
</script>
