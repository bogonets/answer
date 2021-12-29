<i18n lang="yaml">
en:
  header: "New permission"
  subheader: "You can control the level of access to your project."

ko:
  header: "새로운 권한"
  subheader: "프로젝트에 접근할 수 있는 수준을 제어할 수 있습니다."
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <left-title
        :header="$t('header')"
        :subheader="$t('subheader')"
    >
      <form-role
          :loading="submitLoading"
          :permissions="permissions"
          @cancel="onClickCancel"
          @submit="onClickSubmit"
      ></form-role>
    </left-title>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from "@/components/LeftTitle.vue";
import FormRole from '@/components/FormRole.vue';
import {RoleA, CreateRoleQ} from '@/packet/role';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
    FormRole,
  }
})
export default class AdminPermissionsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Permissions',
      disabled: false,
      href: () => this.moveToAdminPermissions(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];

  permissions = [] as Array<string>;
  submitLoading = false;

  created() {
    this.requestPermission();
  }

  requestPermission() {
    this.$api2.getMainPermissions()
        .then(items => {
          this.permissions = items;
        })
        .catch(error => {
          this.toastRequestFailure(error);
          this.moveToBack();
        });
  }


  onClickCancel() {
    this.moveToBack();
  }

  onClickSubmit(event: RoleA) {
    const body = {
      slug: event.slug,
      name: event.name,
      description: event.description,
      hidden: event.hidden,
      lock: event.lock,
      permissions: event.permissions,
    } as CreateRoleQ;

    this.submitLoading = true;
    this.$api2.postAdminRoles(body)
        .then(() => {
          this.submitLoading = false;
          this.moveToAdminPermissions();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.submitLoading = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
