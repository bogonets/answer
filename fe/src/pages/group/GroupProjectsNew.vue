<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <form-project-new
        @cancel="onClickCancel"
        @request:success="onRequestSuccess"
    ></form-project-new>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import FormProjectNew from "@/components/FormProjectNew.vue";

@Component({
  components: {
    ToolbarNavigation,
    FormProjectNew,
  }
})
export default class GroupProjectsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToRootGroups(),
    },
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToGroup(),
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
    this.moveToMainProjects();
  }
}
</script>
