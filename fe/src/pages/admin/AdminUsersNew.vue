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
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <left-title
        :header="$t('header')"
        :subheader="$t('subheader')"
    >
      <form-user
          :loading="submitLoading"
          @cancel="onClickCancel"
          @ok="onClickOk"
      ></form-user>
    </left-title>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import FormUser, {UserItem} from '@/components/FormUser.vue';
import {SignupQ} from '@/packet/user';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
    FormUser,
  }
})
export default class AdminUsersNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Users',
      disabled: false,
      href: () => this.moveToAdminUsers(),
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

  onClickOk(event: UserItem) {
    const body = {
      username: event.username,
      password: this.$api2.encryptPassword(event.password),
      nickname: event.nickname,
      email: event.email,
      phone1: event.phone1,
      phone2: event.phone1,
      is_admin: event.isAdmin,
    } as SignupQ;

    this.submitLoading = true;
    this.$api2.postAdminUsers(body)
        .then(() => {
          this.submitLoading = false;
          this.moveToAdminUsers();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.submitLoading = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
