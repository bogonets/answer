<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <form-group-new
        request-type="self"
        @cancel="onClickCancel"
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
export default class MainGroupsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToMainGroups(),
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
    this.moveToMainGroups();
  }
}
</script>
