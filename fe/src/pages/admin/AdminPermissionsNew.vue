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
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <left-title
        :header="$t('header')"
        :subheader="$t('subheader')"
    >
      <form-permission
          hide-origin-prefix
          :loading="submitLoading"
          @cancel="onClickCancel"
          @ok="onClickOk"
      ></form-permission>
    </left-title>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import LeftTitle from "@/components/LeftTitle.vue";
import FormPermission, {PermissionItem} from '@/components/FormPermission.vue';
import {CreatePermissionQ} from '@/packet/permission';

@Component({
  components: {
    ToolbarNavigation,
    LeftTitle,
    FormPermission,
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

  submitLoading = false;

  onClickCancel() {
    this.moveToBack();
  }

  onClickOk(event: PermissionItem) {
    const body = {
      name: event.name,
      description: event.description,
      features: event.features,
      r_layout: event.r_layout,
      w_layout: event.w_layout,
      r_storage: event.r_storage,
      w_storage: event.w_storage,
      r_manager: event.r_manager,
      w_manager: event.w_manager,
      r_graph: event.r_graph,
      w_graph: event.w_graph,
      r_member: event.r_member,
      w_member: event.w_member,
      r_setting: event.r_setting,
      w_setting: event.w_setting,
    } as CreatePermissionQ;

    this.submitLoading = true;
    this.$api2.postAdminPermissions(body)
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
