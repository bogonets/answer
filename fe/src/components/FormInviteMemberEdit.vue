<i18n lang="yaml">
en:
  header:
    invite: "Invite member"
    members: "Existing members"
  subheader:
    invite: "You can invite a new member."
  label:
    delete: "Delete a member"
  delete_confirm: "Are you sure? Are you really removing this member?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  header:
    invite: "회원 초대"
    members: "기존 회원 목록"
  subheader:
    invite: "새로운 회원을 초대할 수 있습니다."
  label:
    delete: "회원 제거"
  delete_confirm: "이 회원을 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <div>
    <v-container>
      <p :class="titleClass">{{ $t('header.invite') }}</p>
      <v-divider></v-divider>
      <form-invite-member
          hide-cancel-button
          :loading="loadingInvite"
          :usernames="usernames"
          :permissions="permissions"
          @ok="invite"
      ></form-invite-member>

      <p :class="titleClass">{{ $t('header.members') }}</p>
      <v-divider></v-divider>

      <table-members
          :loading="loadingMembers"
          :items="items"
          :permissions="permissions"
          @change="change"
          @click:delete="onClickDelete"
      ></table-members>
    </v-container>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="320">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('label.delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('delete_confirm') }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn :loading="loadingDelete" color="error" @click="onClickDeleteOk">
            {{ $t('delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import LeftTitle from '@/components/LeftTitle.vue';
import FormInviteMember from '@/components/FormInviteMember.vue';
import TableMembers from "@/components/TableMembers.vue";
import type {MemberA, CreateMemberQ, UpdateMemberQ} from "@/packet/member";
import type {RoleA} from '@/packet/role';
import {TITLE_CLASS} from '@/styles/title';

@Component({
  components: {
    TableMembers,
    LeftTitle,
    FormInviteMember,
  }
})
export default class FormInviteMemberEdit extends VueBase {
  private readonly titleClass = TITLE_CLASS;

  @Prop({type: Boolean, default: false})
  readonly hideDelete!: boolean;

  @Prop({type: Boolean, default: false})
  readonly showDeleteDialog!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loadingDelete!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loadingInvite!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loadingMembers!: boolean;

  @Prop({type: Array, default: () => new Array<MemberA>()})
  readonly items!: Array<MemberA>;

  @Prop({type: Array, default: () => new Array<RoleA>()})
  readonly permissions!: Array<RoleA>;

  @Prop({type: Array, default: () => new Array<string>()})
  readonly usernames!: Array<string>;

  deleteCandidate?: MemberA;

  @Emit()
  invite(event: CreateMemberQ) {
    return event;
  }

  @Emit()
  change(event: UpdateMemberQ) {
    return event;
  }

  @Emit('delete:show')
  onClickDelete(item: MemberA) {
    this.deleteCandidate = item;
    return item;
  }

  @Emit('delete:cancel')
  onClickDeleteCancel() {
    return this.deleteCandidate;
  }

  @Emit('delete:ok')
  onClickDeleteOk() {
    return this.deleteCandidate;
  }
}
</script>
