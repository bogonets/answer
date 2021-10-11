<i18n lang="yaml">
en:
  label:
    member: "Member"
    permission: "Permission"
  hint:
    member: "Search for members to update or invite"
    permission: "Choose a role permission."
  cancel: "Cancel"
  invite: "Invite"

ko:
  label:
    member: "회원"
    permission: "권한"
  hint:
    member: "업데이트하거나 초대할 회원 검색."
    permission: "권한을 선택합니다."
  cancel: "취소"
  invite: "초대"
</i18n>

<template>
  <v-form ref="form" v-model="valid">

    <p :class="subtitleClass">{{ $t('label.member') }}</p>
    <v-combobox
        dense
        persistent-hint
        v-model="username"
        :rules="rules.username"
        :items="usernames"
        :hint="$t('hint.member')"
    ></v-combobox>

    <p :class="subtitleClass">{{ $t('label.permission') }}</p>
    <v-select
        dense
        persistent-hint
        v-model="permission"
        :rules="rules.permission"
        :items="visiblePermissionNames"
        :hint="$t('hint.permission')"
    ></v-select>

    <v-row v-if="!hideButtons" class="mt-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn
          v-if="!hideCancelButton"
          class="mr-4"
          color="second"
          @click="cancel"
      >
        {{ $t('cancel') }}
      </v-btn>
      <v-btn
          v-if="!hideSubmitButton"
          color="primary"
          :loading="loading"
          :disabled="disableSubmit"
          @click="onInvite"
      >
        {{ $t('invite') }}
      </v-btn>
    </v-row>

  </v-form>
</template>

<script lang="ts">
import {Component, Prop, Ref, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {USERNAME_RULES, PERMISSION_SLUG_RULES} from '@/rules';
import type {CreateMemberQ} from '@/packet/member';
import type {PermissionA} from '@/packet/permission';

@Component
export default class FormInviteMember extends VueBase {
  private readonly subtitleClass = SUBTITLE_CLASS;
  private readonly rules = {
    username: USERNAME_RULES,
    permission: PERMISSION_SLUG_RULES,
  };

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean})
  readonly disableSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Array, default: () => new Array<string>()})
  readonly usernames!: Array<string>;

  @Prop({type: Array, default: () => new Array<PermissionA>()})
  readonly permissions!: Array<PermissionA>;

  @Ref()
  readonly form!: VForm;

  visiblePermissionNames = [] as Array<string>;
  valid = false;
  username = '';
  permission = '';

  created() {
    this.updateVisiblePermissionNames();
  }

  @Watch('permissions')
  onWatchPermissions(value) {
    this.updateVisiblePermissionNames();
  }

  updateVisiblePermissionNames() {
    const names = [] as Array<string>;
    for (const permission of this.permissions) {
      if (!permission.hidden) {
        names.push(permission.slug);
      }
    }
    this.visiblePermissionNames = names;
  }

  get disableSubmit(): boolean {
    return this.loading || !this.valid || this.disableSubmitButton;
  }

  formValidate() {
    this.form['validate']();
  }

  onInvite() {
    if (!this.disableValidate) {
      this.formValidate();
      if (!this.valid) {
        return;
      }
    }
    this.ok();
  }

  @Emit()
  cancel() {
    // EMPTY
  }

  @Emit()
  ok() {
    return {
      username: this.username,
      permission: this.permission,
    } as CreateMemberQ;
  }
}
</script>
