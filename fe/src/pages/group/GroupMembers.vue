<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
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
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import FormInviteMemberEdit from "@/components/FormInviteMemberEdit.vue";
import {CreateMemberQ, MemberA, UpdateMemberQ} from "@/packet/member";

@Component({
  components: {
    ToolbarNavigation,
    FormInviteMemberEdit,
  }
})
export default class GroupMembers extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToRootGroups(),
    },
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
  permissions = [] as Array<string>;
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
      this.usernames = await this.$api2.getMainUsernames();
      const permissions = await this.$api2.getMainPermissions();
      this.permissions = permissions.map(i => i.name || '');
      const group = this.$route.params.group;
      this.items = await this.$api2.getMainGroupsPgroupMembers(group);
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loadingMembers = false;
    }
  }

  reloadMembers() {
    this.loadingMembers = true;
    this.$api2.getMainGroupsPgroupMembers(this.$route.params.group)
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
    this.$api2.postMainGroupsPgroupMembers(this.$route.params.group, event)
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
    const group = this.$route.params.group;
    const member = event.username;
    this.loadingMembers = true;
    this.$api2.patchMainGroupsPgroupMembersPmember(group, member, event)
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
    const group = this.$route.params.group;
    const member = item.username;
    this.loadingDelete = true;
    this.$api2.deleteMainGroupsPgroupMembersPmember(group, member)
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
