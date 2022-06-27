<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-group-edit
      :value="group"
      :loading-submit="loadingSubmit"
      :loading-delete="loadingDelete"
      :show-delete-dialog="showDeleteDialog"
      @ok="onClickOk"
      @delete:show="onClickDelete"
      @delete:cancel="onClickDeleteCancel"
      @delete:ok="onClickDeleteOk"
    ></form-group-edit>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import FormGroupEdit from '@/components/FormGroupEdit.vue';
import {GroupA, UpdateGroupQ} from '@recc/api/dist/packet/group';

@Component({
  components: {
    ToolbarBreadcrumbs,
    FormGroupEdit,
  },
})
export default class AdminGroupsEdit extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToAdminGroups(),
    },
    {
      text: 'Edit',
      disabled: true,
    },
  ];

  group = {} as GroupA;

  showDeleteDialog = false;
  loadingDelete = false;
  loadingSubmit = false;

  created() {
    this.requestGroup();
  }

  requestGroup() {
    this.$api2
      .getAdminGroupsPgroup(this.$route.params.group)
      .then(item => {
        this.group = item;
      })
      .catch(error => {
        this.toastRequestFailure(error);
        this.moveToBack();
      });
  }

  onClickOk(event: UpdateGroupQ) {
    this.loadingSubmit = true;
    this.$api2
      .patchAdminGroupsPgroup(this.$route.params.group, event)
      .then(() => {
        this.loadingSubmit = false;
        this.toastRequestSuccess();
        this.requestGroup();
      })
      .catch(error => {
        this.loadingSubmit = false;
        this.toastRequestFailure(error);
      });
  }

  onClickDelete() {
    this.showDeleteDialog = true;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk() {
    this.loadingDelete = true;
    this.$api2
      .deleteAdminGroupsGroup(this.$route.params.group)
      .then(() => {
        this.loadingDelete = false;
        this.showDeleteDialog = false;
        this.toastRequestSuccess();
        this.moveToAdminGroups();
      })
      .catch(error => {
        this.loadingDelete = false;
        this.showDeleteDialog = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
