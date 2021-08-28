<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
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

<script lang='ts'>
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import FormInviteMemberEdit from '@/components/FormInviteMemberEdit.vue';
import {MemberA, CreateMemberQ, UpdateMemberQ} from '@/packet/member';

@Component({
  components: {
    ToolbarBreadcrumbs,
    FormInviteMemberEdit,
  }
})
export default class MainMembers extends VueBase {
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
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMain(),
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
      this.items = await this.$api2.getMainProjectsPgroupPprojectMembers(
          this.$route.params.group,
          this.$route.params.project,
      );
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loadingMembers = false;
    }
  }

  reloadMembers() {
    this.loadingMembers = true;
    this.$api2.getMainProjectsPgroupPprojectMembers(
        this.$route.params.group,
        this.$route.params.project,
    )
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
    this.$api2.postMainProjectsPgroupPprojectMembers(
        this.$route.params.group,
        this.$route.params.project,
        event,
    )
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
    this.$api2.patchMainProjectsPgroupPprojectMembersPmember(
        this.$route.params.group,
        this.$route.params.project,
        member,
        event,
    )
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
    this.$api2.deleteMainProjectsPgroupPprojectMembersPmember(
        this.$route.params.group,
        this.$route.params.project,
        member,
    )
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
