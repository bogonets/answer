<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-invite-member-edit
      :show-delete-dialog="showDeleteDialog"
      :loading-delete="loadingDelete"
      :loading-invite="loadingInvite"
      :loading-members="loadingMembers"
      :items="items"
      :permissions="permissions"
      :usernames="usernames"
      @invite="onClickInvite"
      @change="onChangeMember"
      @delete:show="onClickDelete"
      @delete:cancel="onClickDeleteCancel"
      @delete:ok="onClickDeleteOk"
    ></form-invite-member-edit>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import FormInviteMemberEdit from '@/components/FormInviteMemberEdit.vue';
import type {MemberA, CreateMemberQ, UpdateMemberQ} from '@/packet/member';
import type {RoleA} from '@/packet/role';

@Component({
  components: {
    ToolbarBreadcrumbs,
    FormInviteMemberEdit,
  },
})
export default class GroupMembers extends VueBase {
  readonly breadcrumbs = [
    {
      text: this.$route.params.group,
      disabled: false,
      href: () => this.moveToGroup(),
    },
    {
      text: 'Members',
      disabled: true,
    },
  ];

  showDeleteDialog = false;
  loadingDelete = false;
  loadingInvite = false;
  loadingMembers = false;

  items = [] as Array<MemberA>;
  permissions = [] as Array<RoleA>;
  usernames = [] as Array<string>;

  created() {
    this.requestSetup();
  }

  requestSetup() {
    this.loadingMembers = true;
    (async () => {
      await this.onRequestSetupDatas();
    })();
  }

  private async onRequestSetupDatas() {
    try {
      const group = this.$route.params.group;
      const usernames = await this.$api2.getMainUsernames();
      this.permissions = await this.$api2.getMainRoles();
      this.items = await this.$api2.getMainGroupsPgroupMembers(group);
      this.usernames = usernames.filter(name => {
        return this.items.findIndex(i => i.username === name) === -1;
      });
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loadingMembers = false;
    }
  }

  reloadMembers() {
    this.loadingMembers = true;
    this.$api2
      .getMainGroupsPgroupMembers(this.$route.params.group)
      .then(items => {
        this.loadingMembers = false;
        this.items = items;
      })
      .catch(error => {
        this.loadingMembers = false;
        this.toastRequestFailure(error);
      });
  }

  onClickInvite(event: CreateMemberQ) {
    this.loadingInvite = true;
    this.$api2
      .postMainGroupsPgroupMembers(this.$route.params.group, event)
      .then(() => {
        this.loadingInvite = false;
        this.toastRequestSuccess();
        this.reloadMembers();
      })
      .catch(error => {
        this.loadingInvite = false;
        this.toastRequestFailure(error);
      });
  }

  onChangeMember(event: UpdateMemberQ) {
    const member = event.username;
    this.loadingMembers = true;
    this.$api2
      .patchMainGroupsPgroupMembersPmember(this.$route.params.group, member, event)
      .then(() => {
        this.loadingMembers = false;
        this.toastRequestSuccess();
      })
      .catch(error => {
        this.loadingInvite = false;
        this.toastRequestFailure(error);
        this.reloadMembers();
      });
  }

  onClickDelete() {
    this.showDeleteDialog = true;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk(item: MemberA) {
    const member = item.username;
    this.loadingDelete = true;
    this.$api2
      .deleteMainGroupsPgroupMembersPmember(this.$route.params.group, member)
      .then(() => {
        this.loadingDelete = false;
        this.showDeleteDialog = false;
        this.toastRequestSuccess();
        this.reloadMembers();
      })
      .catch(error => {
        this.loadingDelete = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
