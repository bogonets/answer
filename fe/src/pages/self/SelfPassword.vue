<i18n lang="yaml">
en:
  header:
    password: 'Password'
  subheader:
    password: >
      After a successful password update, you will be redirected to
      the login page where you can log in with your new password.
  label:
    current_password: 'Current password'
    new_password: 'New password'
    confirm_password: 'Password confirmation'
  hint:
    current_password: 'You must provide your current password in order to change it.'
    new_password: 'Please enter the password to be used when sign in.'
    confirm_password: 'Please enter your password again.'
  msg:
    confirm_password: 'Please reconfirm your password.'
  submit: 'Submit'

ko:
  header:
    password: '비밀번호'
  subheader:
    password: >
      비밀번호 업데이트에 성공하면
      새 비밀번호로 로그인할 수 있는 로그인 페이지로 리디렉션됩니다.
  label:
    current_password: '현재 비밀번호'
    new_password: '새로운 비밀번호'
    confirm_password: '새로운 비밀번호 재확인'
  hint:
    current_password: '변경하려면 현재 비밀번호를 입력해야 합니다.'
    new_password: '로그인시 사용할 비밀번호를 입력해 주세요.'
    confirm_password: '비밀번호를 한번 더 입력해 주세요.'
  msg:
    confirm_password: '비밀번호를 재확인해주세요.'
  submit: '제출'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <left-title :header="$t('header.password')" :subheader="$t('subheader.password')">
      <v-form ref="form" v-model="valid">
        <p :class="subtitleClass">{{ $t('label.current_password') }}</p>
        <v-text-field
          dense
          persistent-hint
          type="password"
          autocomplete="off"
          :value="currentPassword"
          @input="onInputCurrentPassword"
          :rules="rules.password"
          :hint="$t('hint.current_password')"
        ></v-text-field>

        <p :class="subtitleClass">{{ $t('label.new_password') }}</p>
        <v-text-field
          dense
          persistent-hint
          type="password"
          autocomplete="off"
          :value="newPassword"
          @input="onInputNewPassword"
          :rules="rules.password"
          :hint="$t('hint.new_password')"
        ></v-text-field>

        <p :class="subtitleClass">{{ $t('label.confirm_password') }}</p>
        <v-text-field
          dense
          persistent-hint
          type="password"
          autocomplete="off"
          ref="confirmPasswordField"
          :value="confirmPassword"
          @input="onInputConfirmPassword"
          :rules="rules.confirmPassword"
          :hint="$t('hint.confirm_password')"
          @keypress.enter.stop="onEnterConfirm"
        ></v-text-field>

        <v-row class="mt-4 mb-2" no-gutters>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            :loading="loadingSubmit"
            :disabled="disableSubmit"
            @click="onSubmit"
          >
            {{ $t('submit') }}
          </v-btn>
        </v-row>
      </v-form>
    </left-title>
  </v-container>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import {VForm} from 'vuetify/lib/components/VForm';
import {VTextField} from 'vuetify/lib/components/VTextField';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {PASSWORD_RULES} from '@/rules';
import {UpdatePasswordQ} from '@/packet/user';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
  },
})
export default class SelfProfile extends VueBase {
  private readonly subtitleClass = SUBTITLE_CLASS;

  private readonly rules = {
    password: PASSWORD_RULES,
    confirmPassword: [...PASSWORD_RULES, this.confirmPasswordRule],
  };

  private readonly navigationItems = [
    {
      text: 'Self',
      disabled: false,
      href: () => this.moveToSelf(),
    },
    {
      text: 'Password',
      disabled: true,
    },
  ];

  @Ref()
  readonly form!: VForm;

  @Ref()
  readonly confirmPasswordField!: VTextField;

  loadingSubmit = false;
  valid = false;

  currentPassword = '';
  newPassword = '';
  confirmPassword = '';

  onInputCurrentPassword(event: string) {
    this.currentPassword = event;
  }

  onInputNewPassword(event: string) {
    this.newPassword = event;
    this.validateConfirmPasswordField();
  }

  onInputConfirmPassword(event: string) {
    this.confirmPassword = event;
  }

  confirmPasswordRule(value: string): boolean | string {
    return this.newPassword == value || this.$t('msg.confirm_password').toString();
  }

  validateConfirmPasswordField() {
    this.confirmPasswordField['validate']();
  }

  get disableSubmit(): boolean {
    const samePassword = this.newPassword === this.confirmPassword;
    return this.loadingSubmit || !(this.valid && samePassword);
  }

  formValidate() {
    this.form['validate']();
  }

  onEnterConfirm() {
    if (this.disableSubmit) {
      return;
    }
    this.onSubmit();
  }

  onSubmit() {
    this.formValidate();
    if (!this.valid) {
      return;
    }

    const before = this.$api2.encryptPassword(this.currentPassword);
    const after = this.$api2.encryptPassword(this.newPassword);
    const body = {
      before: before,
      after: after,
    } as UpdatePasswordQ;

    this.loadingSubmit = true;
    this.$api2
      .patchSelfPassword(body)
      .then(() => {
        this.loadingSubmit = false;
        this.toastRequestSuccess();
        this.$localStore.clearSession();
        this.moveToSignin();
      })
      .catch(error => {
        this.loadingSubmit = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
