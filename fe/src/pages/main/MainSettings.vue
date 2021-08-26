<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

<!--    <form-project-edit-->
<!--        :value="group"-->
<!--        :loading-submit="loadingSubmit"-->
<!--        :loading-delete="loadingDelete"-->
<!--        :show-delete-dialog="showDeleteDialog"-->
<!--        @ok="onClickOk"-->
<!--        @delete:show="onClickDelete"-->
<!--        @delete:cancel="onClickDeleteCancel"-->
<!--        @delete:ok="onClickDeleteOk"-->
<!--    ></form-project-edit>-->

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import {GroupA, UpdateGroupQ} from '@/packet/group';

@Component({
  components: {
    ToolbarNavigation,
  }
})
export default class GroupSettings extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToRootGroups(),
    },
    {
      text: 'Settings',
      disabled: true,
    },
  ];

  // group = {} as GroupA;
  //
  // showDeleteDialog = false;
  // loadingDelete = false;
  // loadingSubmit = false;
  //
  // created() {
  //   this.requestGroup();
  // }
  //
  // requestGroup() {
  //   this.$api2.getMainGroupsPgroup(this.$route.params.group)
  //       .then(item => {
  //         this.group = item;
  //       })
  //       .catch(error => {
  //         this.toastRequestFailure(error);
  //         this.moveToBack();
  //       });
  // }
  //
  // onClickOk(event: UpdateGroupQ) {
  //   this.loadingSubmit = true;
  //   this.$api2.patchMainGroupsPgroup(this.$route.params.group, event)
  //       .then(() => {
  //         this.loadingSubmit = false;
  //         this.toastRequestSuccess();
  //         this.requestGroup();
  //       })
  //       .catch(error => {
  //         this.loadingSubmit = false;
  //         this.toastRequestFailure(error);
  //       });
  // }
  //
  // onClickDelete() {
  //   this.showDeleteDialog = true;
  // }
  //
  // onClickDeleteCancel() {
  //   this.showDeleteDialog = false;
  // }
  //
  // onClickDeleteOk() {
  //   this.loadingDelete = true;
  //   this.$api2.deleteMainGroupsGroup(this.$route.params.group)
  //       .then(() => {
  //         this.loadingDelete = false;
  //         this.showDeleteDialog = false;
  //         this.toastRequestSuccess();
  //         this.moveToAdminGroups();
  //       })
  //       .catch(error => {
  //         this.loadingDelete = false;
  //         this.showDeleteDialog = false;
  //         this.toastRequestFailure(error);
  //       });
  // }
}
</script>
