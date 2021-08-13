<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <form-user-new
        :loading="showSignupLoading"
        @cancel="onClickCancel"
        @ok="onClickOk"
    ></form-user-new>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import FormUserNew from "@/components/FormUserNew.vue";

@Component({
  components: {
    ToolbarNavigation,
    FormUserNew,
  }
})
export default class MainAdminUsersNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Users',
      disabled: false,
      href: () => this.moveToMainAdminUsers(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];

  showSignupLoading = false;

  onClickCancel() {
    this.moveToMainAdminUsers();
  }

  onClickOk(user) {
    this.showSignupLoading = true;
    this.$api2.postUsers(user)
        .then(() => {
          this.showSignupLoading = false;
          this.moveToMainAdminUsers();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.showSignupLoading = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
