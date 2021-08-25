<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <form-group-new
        request-type="self"
        @request:success="onRequestSuccess"
    ></form-group-new>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import FormGroupNew from '@/components/FormGroupNew.vue';

@Component({
  components: {
    ToolbarNavigation,
    FormGroupNew,
  }
})
export default class RootGroupsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToRootGroups(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];

  onRequestSuccess() {
    this.moveToRootGroups();
  }
}
</script>
