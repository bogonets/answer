<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-group-edit
      hide-features
      hide-visibility
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
export default class GroupSettings extends VueBase {
  readonly breadcrumbs = [
    {
      text: this.$route.params.group,
      disabled: false,
      href: () => this.moveToGroup(),
    },
    {
      text: 'Settings',
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
      .getMainGroupsPgroup(this.$route.params.group)
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
      .patchMainGroupsPgroup(this.$route.params.group, event)
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
      .deleteMainGroupsGroup(this.$route.params.group)
      .then(() => {
        this.loadingDelete = false;
        this.showDeleteDialog = false;
        this.toastRequestSuccess();
        this.moveToRootGroups();
      })
      .catch(error => {
        this.loadingDelete = false;
        this.showDeleteDialog = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
