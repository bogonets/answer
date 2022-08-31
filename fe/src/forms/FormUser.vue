<i18n lang="yaml">
en:
  label:
    username: 'Username (Required)'
    password: 'Password (Required)'
    confirm_password: 'Confirm (Required)'
    nickname: 'Nickname'
    email: 'E-Mail'
    phone: 'Phone'
    admin: 'Administrator'
  hint:
    username: 'Please enter the ID to be used when sign in.'
    password: 'Please enter the password to be used when sign in.'
    confirm_password: 'Please enter your password again.'
    nickname: 'Please enter your nickname that will be displayed on the screen.'
    email: 'Please enter the email address to be used in case of loss of ID and password.'
    phone: 'This is the representative phone number.'
    admin: 'Gain full control over the system.'
  msg:
    confirm_password: 'Please reconfirm your password.'
  cancel: 'Cancel'
  submit: 'Submit'

ko:
  label:
    username: '사용자명 (필수)'
    password: '비밀번호 (필수)'
    confirm_password: '비밀번호 확인 (필수)'
    nickname: '별칭'
    email: '이메일'
    phone: '전화번호'
    admin: '관리자'
  hint:
    username: '로그인시 사용할 아이디를 입력해 주세요.'
    password: '로그인시 사용할 비밀번호를 입력해 주세요.'
    confirm_password: '비밀번호를 한번 더 입력해 주세요.'
    nickname: '화면에 표시될 당신의 별명을 입력해 주세요.'
    email: '아이디 및 비밀번호 분실시 사용될 이메일 주소를 입력해 주세요.'
    phone: '대표 전화번호 입니다.'
    admin: '시스템을 완전히 제어할 수 있는 권한을 획득합니다.'
  msg:
    confirm_password: '비밀번호를 재확인해주세요.'
  cancel: '취소'
  submit: '제출'
</i18n>

<template>
  <div>
    <p :class="subtitleClass">{{ $t('label.username') }}</p>
    <v-text-field
      dense
      type="text"
      autocomplete="off"
      :value="username"
      @input="onUpdateUsername"
      :rules="rules.username"
      :disabled="disableUsername"
      :filled="disableUsername"
      :persistent-hint="!disableUsername"
      :hide-details="disableUsername"
      :hint="$t('hint.username')"
    ></v-text-field>

    <div v-if="!hidePassword">
      <p :class="subtitleClass">{{ $t('label.password') }}</p>
      <v-text-field
        dense
        persistent-hint
        type="password"
        autocomplete="off"
        :value="password"
        @input="onUpdatePassword"
        :rules="rules.password"
        :hint="$t('hint.password')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('label.confirm_password') }}</p>
      <v-text-field
        dense
        persistent-hint
        type="password"
        autocomplete="off"
        ref="confirm-field"
        :value="confirm"
        @input="onUpdateConfirm"
        :rules="rules.confirmPassword"
        :hint="$t('hint.confirm_password')"
        @keypress.enter.stop="onEnterConfirm"
      ></v-text-field>
    </div>

    <div v-if="!hideProfile">
      <p :class="subtitleClass">{{ $t('label.nickname') }}</p>
      <v-text-field
        dense
        persistent-hint
        :value="nickname"
        @input="onUpdateNickname"
        :hint="$t('hint.nickname')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('label.email') }}</p>
      <v-text-field
        dense
        persistent-hint
        :value="email"
        @input="onUpdateEmail"
        :rules="rules.email"
        :hint="$t('hint.email')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('label.phone') }}</p>
      <v-text-field
        dense
        persistent-hint
        :value="phone"
        @input="onUpdatePhone"
        :rules="rules.phone"
        :hint="$t('hint.phone')"
      ></v-text-field>
    </div>

    <v-row v-if="!hideAdmin" class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('label.admin') }}</p>
        <p class="text-caption text--secondary">{{ $t('hint.admin') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch
          inset
          :disabled="disableAdmin"
          :value="admin"
          @change="onChangeAdmin"
        ></v-switch>
      </div>
    </v-row>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Emit, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VTextField} from 'vuetify/lib/components/VTextField';
import {USERNAME_RULES, PASSWORD_RULES, PHONE_RULES, EMAIL_RULES} from '@/rules';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

@Component
export default class FormUser extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;

  readonly rules = {
    username: USERNAME_RULES,
    password: PASSWORD_RULES,
    confirmPassword: [...PASSWORD_RULES, this.confirmPasswordRule],
    phone: PHONE_RULES,
    email: EMAIL_RULES,
  };

  @Prop({type: Boolean})
  readonly disableUsername!: boolean;

  @Prop({type: Boolean})
  readonly disableAdmin!: boolean;

  @Prop({type: Boolean})
  readonly hidePassword!: boolean;

  @Prop({type: Boolean})
  readonly hideProfile!: boolean;

  @Prop({type: Boolean})
  readonly hideAdmin!: boolean;

  @Prop({type: String, default: ''})
  readonly username!: string;

  @Prop({type: String, default: ''})
  readonly password!: string;

  @Prop({type: String, default: ''})
  readonly confirm!: string;

  @Prop({type: String, default: ''})
  readonly nickname!: string;

  @Prop({type: String, default: ''})
  readonly email!: string;

  @Prop({type: String, default: ''})
  readonly phone!: string;

  @Prop({type: Boolean, default: false})
  readonly admin!: boolean;

  @Ref('confirm-field')
  readonly confirmField!: VTextField;

  confirmPasswordRule(value: string): boolean | string {
    return this.password == value || this.$t('msg.confirm_password').toString();
  }

  validateConfirmField() {
    this.confirmField['validate']();
  }

  @Emit('update:username')
  onUpdateUsername(value: string) {
    return value;
  }

  @Emit('update:password')
  onUpdatePassword(value: string) {
    this.validateConfirmField();
    return value;
  }

  @Emit('update:confirm')
  onUpdateConfirm(value: string) {
    return value;
  }

  @Emit('update:nickname')
  onUpdateNickname(value: string) {
    return value;
  }

  @Emit('update:email')
  onUpdateEmail(value: string) {
    return value;
  }

  @Emit('update:phone')
  onUpdatePhone(value: string) {
    return value;
  }

  @Emit('update:admin')
  onChangeAdmin(value: null | boolean) {
    return !!value;
  }
}
</script>
