<i18n lang="yaml">
en:
  msg:
    no_group: "Not exists group slug."

ko:
  msg:
    no_group: "그룹 슬러그가 없습니다."
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
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
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import FormGroupEdit from "@/components/FormGroupEdit.vue";
import {GroupA, UpdateGroupQ} from '@/packet/group';

@Component({
  components: {
    ToolbarNavigation,
    FormGroupEdit,
  }
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

  group_slug = '';
  group = {} as GroupA;

  showDeleteDialog = false;
  loadingDelete = false;
  loadingSubmit = false;

  created() {
    this.group_slug = this.$route.params.group;
    if (!this.group_slug) {
      this.toastError(this.$t('msg.no_group'));
      return;
    }

    this.requestGroup();
  }

  requestGroup() {
    this.$api2.getAdminGroupsPgroup(this.group_slug)
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
    this.$api2.patchAdminGroupsPgroup(this.group_slug, event)
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
    this.$api2.deleteAdminGroupsGroup(this.group_slug)
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
