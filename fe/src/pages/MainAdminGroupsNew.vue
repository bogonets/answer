<i18n lang="yaml">
en:
  header: "New group"
  subheader: >
    Groups allow you to manage and collaborate across multiple projects.
    Members of a group have access to all of its projects.

ko:
  header: "새로운 그룹"
  subheader: >
    여러 프로젝트를 관리하고 공동 작업할 수 있습니다.
    그룹의 구성원은 모든 프로젝트에 접근할 수 있습니다.
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <left-title
        :header="$t('header')"
        :subheader="$t('subheader')"
    >
      <form-group
          @cancel="onClickCancel"
          @ok="onClickOk"
      ></form-group>
    </left-title>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import FormGroup from '@/components/FormGroup.vue';
import LeftTitle from "@/components/LeftTitle.vue";

@Component({
  components: {
    LeftTitle,
    FormGroup,
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
