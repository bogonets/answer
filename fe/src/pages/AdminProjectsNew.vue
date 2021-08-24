<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <form-project-new
        request-type="admin"
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
export default class AdminProjectsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToMainAdminProjects(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];

  submitLoading = false;

  onClickCancel() {
    this.moveToBack();
  }

  onRequestSuccess() {
    this.moveToMainAdminProjects();
  }
}
</script>
