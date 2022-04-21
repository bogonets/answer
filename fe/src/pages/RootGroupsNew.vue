<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-group-new
      hide-features
      hide-visibility
      request-type="self"
      @request:success="onRequestSuccess"
    ></form-group-new>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import FormGroupNew from '@/components/FormGroupNew.vue';

@Component({
  components: {
    ToolbarBreadcrumbs,
    FormGroupNew,
  },
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
