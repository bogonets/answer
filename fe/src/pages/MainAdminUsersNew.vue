<i18n lang="yaml">
en:
  header: "New user"
  subheader: "Register a new member."

ko:
  header: "새로운 사용자"
  subheader: "새로운 구성원을 등록합니다."
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <left-title
        :header="$t('header')"
        :subheader="$t('subheader')"
    >
      <form-user
          :loading="showSignupLoading"
          @cancel="onClickCancel"
          @ok="onClickOk"
      ></form-user>
    </left-title>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import LeftTitle from "@/components/LeftTitle.vue";
import FormUser from "@/components/FormUser.vue";

@Component({
  components: {
    ToolbarNavigation,
    LeftTitle,
    FormUser,
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
