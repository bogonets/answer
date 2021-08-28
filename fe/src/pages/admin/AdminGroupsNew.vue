<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-group-new
        request-type="admin"
        @cancel="onClickCancel"
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
  }
})
export default class AdminGroupsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToAdminGroups(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];

  onClickCancel() {
    this.moveToBack();
  }

  onRequestSuccess() {
    this.moveToAdminGroups();
  }
}
</script>
