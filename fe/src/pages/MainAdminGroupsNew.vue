<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <form-group-new
        @cancel="onClickCancel"
        @ok="onClickOk"
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
    FormGroupNew,
    ToolbarNavigation,
  }
})
export default class MainAdminGroupsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToMainAdminGroups(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];

  showNewGroupLoading = false;

  onClickCancel() {
    this.moveToMainAdminGroups();
  }

  onClickOk(group) {
    this.showNewGroupLoading = true;
    this.$api2.postGroups(group)
        .then(() => {
          this.showNewGroupLoading = false;
          this.moveToMainAdminGroups();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.showNewGroupLoading = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
