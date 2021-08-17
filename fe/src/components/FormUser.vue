<i18n lang="yaml">
en:
  label:
    username: "Username (Required)"
    password: "Password (Required)"
    confirmPassword: "Confirm (Required)"
    nickname: "Nickname"
    email: "E-Mail"
    phone1: "Phone1"
    phone2: "Phone2"
    is_admin: "Administrator"
  hint:
    username: "Please enter the ID to be used when sign in."
    password: "Please enter the password to be used when sign in."
    confirmPassword: "Please enter your password again."
    nickname: "Please enter your nickname that will be displayed on the screen."
    email: "Please enter the email address to be used in case of loss of ID and password."
    phone1: "This is the representative phone number."
    phone2: "Secondary phone number."
    is_admin: "Gain full control over the system."
  msg:
    confirm_password: "Please reconfirm your password."
  cancel: "Cancel"
  signup: "Signup"

ko:
  label:
    username: "사용자명 (필수)"
    password: "비밀번호 (필수)"
    confirmPassword: "비밀번호 확인 (필수)"
    nickname: "별칭"
    email: "이메일"
    phone1: "전화번호1"
    phone2: "전화번호2"
    is_admin: "관리자"
  hint:
    username: "로그인시 사용할 아이디를 입력해 주세요."
    password: "로그인시 사용할 비밀번호를 입력해 주세요."
    confirmPassword: "비밀번호를 한번 더 입력해 주세요."
    nickname: "화면에 표시될 당신의 별명을 입력해 주세요."
    email: "아이디 및 비밀번호 분실시 사용될 이메일 주소를 입력해 주세요."
    phone1: "대표 전화번호 입니다."
    phone2: "보조 전화번호 입니다."
    is_admin: "시스템을 완전히 제어할 수 있는 권한을 획득합니다."
  msg:
    confirm_password: "비밀번호를 재확인해주세요."
  cancel: "취소"
  signup: "가입"
</i18n>

<template>
  <v-form ref="form" v-model="valid">

    <p :class="subtitleClass">{{ $t('label.username') }}</p>
    <v-text-field
        dense
        persistent-hint
        type="text"
        autocomplete="off"
        v-model="username"
        :rules="rules.username"
        :hint="$t('hint.username')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('label.password') }}</p>
    <v-text-field
        dense
        persistent-hint
        type="password"
        autocomplete="off"
        v-model="password"
        :rules="rules.password"
        :hint="$t('hint.password')"
    ></v-text-field>

    <p :class="subtitleClass">{{ $t('label.confirmPassword') }}</p>
    <v-text-field
        dense
        persistent-hint
        type="password"
        autocomplete="off"
        ref="confirmPasswordField"
        v-model="confirmPassword"
        :rules="rules.confirmPassword"
        :hint="$t('hint.confirmPassword')"
    ></v-text-field>

    <div v-if="!hideProfile">
      <p :class="subtitleClass">{{ $t('label.nickname') }}</p>
      <v-text-field
          dense
          persistent-hint
          v-model="nickname"
          :hint="$t('hint.nickname')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('label.email') }}</p>
      <v-text-field
          dense
          persistent-hint
          v-model="email"
          :rules="rules.email"
          :hint="$t('hint.email')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('label.phone1') }}</p>
      <v-text-field
          dense
          persistent-hint
          v-model="phone1"
          :rules="rules.phone"
          :hint="$t('hint.phone1')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('label.phone2') }}</p>
      <v-text-field
          dense
          persistent-hint
          v-model="phone2"
          :rules="rules.phone"
          :hint="$t('hint.phone2')"
      ></v-text-field>
    </div>

    <v-row v-if="!hideAccess" class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('label.is_admin') }}</p>
        <p class="text-caption text--secondary">{{ $t('hint.is_admin') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch inset v-model="isAdmin"></v-switch>
      </div>
    </v-row>

    <v-row class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn
          class="mr-4"
          color="second"
          @click="cancel"
      >
        {{ $t('cancel') }}
      </v-btn>
      <v-btn
          color="primary"
          :loading="loading"
          :disabled="disableSignup"
          @click="submit"
      >
        {{ $t('signup') }}
      </v-btn>
    </v-row>

  </v-form>
</template>

<script lang="ts">
import {Component, Prop, Watch, Emit, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import {VTextField} from 'vuetify/lib/components/VTextField';
import {UserA} from '@/packet/user';
import {USERNAME_RULES, PASSWORD_RULES, PHONE_RULES, EMAIL_RULES} from '@/rules';

const SUBTITLE_CLASSES = [
  'text-subtitle-2',
  'text--secondary',
  'font-weight-bold',
  'my-2',
];
const SUBTITLE_CLASS = SUBTITLE_CLASSES.join(' ');

@Component
export default class FormUser extends VueBase {
  private readonly subtitleClass = SUBTITLE_CLASS
  private readonly rules = {
    username: USERNAME_RULES,
    password: PASSWORD_RULES,
    confirmPassword: [...PASSWORD_RULES, this.samePasswordRule],
    phone: PHONE_RULES,
    email: EMAIL_RULES,
  };

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideProfile!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideAccess!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disableValidate!: boolean;

  @Ref()
  readonly form!: VForm;

  @Ref()
  readonly confirmPasswordField!: VTextField;

  valid = false;
  username = '';
  password = '';
  confirmPassword = '';
  nickname = '';
  email = '';
  phone1 = '';
  phone2 = '';
  isAdmin = false;

  samePasswordRule(value: string): boolean | string {
    return this.password === value || this.$t('msg.confirm_password').toString();
  }

  get disableSignup(): boolean {
    const filledRequired = !!this.username && !!this.password && !!this.confirmPassword;
    const samePassword = this.password === this.confirmPassword;
    return this.loading || !(this.valid && filledRequired && samePassword);
  }

  validateConfirmPasswordField() {
    this.confirmPasswordField['validate']();
  }

  formValidate() {
    this.form['validate']();
  }

  get formsResult(): UserA {
    const required = {
      username: this.username,
      password: this.$api2.encryptPassword(this.password),
    };
    const profile = {
      nickname: this.nickname,
      email: this.email,
      phone1: this.phone1,
      phone2: this.phone2,
    };
    const access = {
      is_admin: this.isAdmin,
    };

    return {
      ... required,
      ... (this.hideProfile ? undefined : profile),
      ... (this.hideAccess ? undefined : access),
    } as UserA;
  }

  @Watch('password')
  onChangePassword() {
    this.validateConfirmPasswordField();
  }

  @Emit()
  cancel() {
    return this.formsResult;
  }

  @Emit()
  ok() {
    return this.formsResult;
  }

  submit() {
    if (!this.disableValidate) {
      this.formValidate();
      if (!this.valid) {
        return;
      }
    }
    this.ok();
  }
}
</script>
