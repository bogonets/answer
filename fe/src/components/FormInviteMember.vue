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
        :rules="usernameRules"
        :items="usernames"
        :hint="$t('hint.member')"
    ></v-combobox>

    <p :class="subtitleClass">{{ $t('label.permission') }}</p>
    <v-select
        dense
        persistent-hint
        v-model="rule"
        :rules="permissionRules"
        :items="visibleRules"
        :hint="$t('hint.permission')"
        item-value="slug"
        item-disabled="hidden"
        return-object
    >
      <template v-slot:item="{ item }">
        {{ item.name }}
        <v-chip class="ml-2" x-small outlined color="primary">
          <v-icon left>mdi-identifier</v-icon>
          {{ item.slug }}
        </v-chip>
      </template>

      <template v-slot:selection="{ item }">
        {{ item.name }}
        <v-chip class="ml-2" x-small outlined color="primary">
          <v-icon left>mdi-identifier</v-icon>
          {{ item.slug }}
        </v-chip>
      </template>
    </v-select>

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
import {USERNAME_RULES} from '@/rules';
import type {CreateMemberQ} from '@/packet/member';
import type {RuleA} from '@/packet/rule';
import requiredField from '@/rules/required';
import slugFormat from '@/rules/slug';

@Component
export default class FormInviteMember extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly usernameRules = USERNAME_RULES;
  readonly permissionRules = [
    value => requiredField(value.slug),
    value => slugFormat(value.slug),
  ];

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

  @Prop({type: Array, default: () => new Array<RuleA>()})
  readonly permissions!: Array<RuleA>;

  @Ref()
  readonly form!: VForm;

  visibleRules = [] as Array<RuleA>;
  valid = false;
  username = '';
  rule = {} as RuleA;

  created() {
    this.updateVisiblePermissionNames();
  }

  @Watch('permissions')
  onWatchPermissions(value) {
    this.updateVisiblePermissionNames();
  }

  updateVisiblePermissionNames() {
    const result = [] as Array<RuleA>;
    for (const permission of this.permissions) {
      if (!permission.hidden) {
        result.push(permission);
      }
    }
    this.visibleRules = result;
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
      rule: this.rule.slug,
    } as CreateMemberQ;
  }
}
</script>
