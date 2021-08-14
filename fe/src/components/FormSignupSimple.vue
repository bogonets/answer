<i18n lang="yaml">
en:
  header:
    required: "Required information"
    profile: "User profile"
    access: "Access"
  label:
    username: "Username"
    password: "Password"
    confirmPassword: "Confirm"
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
  header:
    required: "필수 정보"
    profile: "사용자 프로필"
    access: "접근 권한"
  label:
    username: "사용자명"
    password: "비밀번호"
    confirmPassword: "비밀번호 확인"
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
  <v-form
      ref="form"
      v-model="valid"
  >
    <v-subheader v-if="!hideSubheader">{{ $t('header.required') }}</v-subheader>
    <v-divider v-if="!hideSubheader"></v-divider>
    <v-list flat>
      <v-list-item>
        <v-text-field
            dense
            outlined
            type="text"
            autocomplete="off"
            prepend-icon="mdi-account"
            v-model="username"
            :rules="rules.username"
            :label="$t('label.username')"
            :hint="$t('hint.username')"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-text-field
            dense
            outlined
            autocomplete="off"
            prepend-icon="mdi-lock"
            type="password"
            v-model="password"
            :rules="rules.password"
            :label="$t('label.password')"
            :hint="$t('hint.password')"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-text-field
            dense
            outlined
            autocomplete="off"
            prepend-icon="mdi-lock-check"
            ref="confirmPasswordField"
            type="password"
            v-model="confirmPassword"
            :rules="rules.confirmPassword"
            :label="$t('label.confirmPassword')"
            :hint="$t('hint.confirmPassword')"
        ></v-text-field>
      </v-list-item>
    </v-list>

    <v-subheader v-if="!hideProfile && !hideSubheader">{{ $t('header.profile') }}</v-subheader>
    <v-divider v-if="!hideProfile && !hideSubheader"></v-divider>
    <v-list v-if="!hideProfile" flat>
      <v-list-item>
        <v-text-field
            dense
            outlined
            type="text"
            autocomplete="off"
            prepend-icon="mdi-account-outline"
            v-model="nickname"
            :label="$t('label.nickname')"
            :hint="$t('hint.nickname')"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-text-field
            dense
            outlined
            type="text"
            autocomplete="off"
            prepend-icon="mdi-email"
            v-model="email"
            :rules="rules.email"
            :label="$t('label.email')"
            :hint="$t('hint.email')"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-text-field
            dense
            outlined
            type="text"
            autocomplete="off"
            prepend-icon="mdi-phone"
            v-model="phone1"
            :rules="rules.phone"
            :label="$t('label.phone1')"
            :hint="$t('hint.phone1')"
        ></v-text-field>
      </v-list-item>

      <v-list-item>
        <v-text-field
            dense
            outlined
            type="text"
            autocomplete="off"
            prepend-icon="mdi-phone"
            v-model="phone2"
            :rules="rules.phone"
            :label="$t('label.phone2')"
            :hint="$t('hint.phone2')"
        ></v-text-field>
      </v-list-item>
    </v-list>

    <v-subheader v-if="!hideAccess && !hideSubheader">{{ $t('header.access') }}</v-subheader>
    <v-divider v-if="!hideAccess && !hideSubheader"></v-divider>
    <v-list v-if="!hideAccess" flat>
      <v-list-item three-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('label.is_admin') }}</v-list-item-title>
          <v-list-item-subtitle>{{ $t('hint.is_admin') }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-switch inset v-model="isAdmin"></v-switch>
      </v-list-item>
    </v-list>

    <v-divider></v-divider>

    <v-list flat>
      <v-list-item :three-line="!denseFooter">
        <v-spacer></v-spacer>
        <v-btn
            color="second"
            class="mr-4"
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
      </v-list-item>
    </v-list>
  </v-form>
</template>

<script lang="ts">
import {Component, Prop, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {User} from '@/apis/api-v2';
import {USERNAME_RULES, PASSWORD_RULES, PHONE_RULES, EMAIL_RULES} from '@/rules';

@Component
export default class FormSignupSimple extends VueBase {
  private readonly rules = {
    username: USERNAME_RULES,
    password: PASSWORD_RULES,
    confirmPassword: [...PASSWORD_RULES, this.samePasswordRule],
    phone: PHONE_RULES,
    email: EMAIL_RULES,
  };

  @Prop({type: String, default: ''})
  readonly title!: string;

  @Prop({type: String, default: ''})
  readonly subtitle!: string;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideProfile!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideAccess!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideSubheader!: boolean;

  @Prop({type: Boolean, default: false})
  readonly denseFooter!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disableValidate!: boolean;

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
    const result = this.loading || !(this.valid && filledRequired && samePassword);
    console.debug(`disableSignup -> ${result}`);
    return result;
  }

  get form() {
    return this.$refs.form;
  }

  get confirmPasswordField() {
    return this.$refs.confirmPasswordField;
  }

  validate() {
    this.form['validate']();
  }

  validateConfirmPasswordField() {
    this.confirmPasswordField['validate']();
  }

  reset() {
    this.form['reset']();
  }

  resetValidation() {
    this.form['resetValidation']();
  }

  @Watch('password')
  onChangePassword(value) {
    this.validateConfirmPasswordField();
  }

  @Emit()
  cancel() {
    // EMPTY.
  }

  @Emit()
  ok() {
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
    } as User;
  }

  submit() {
    if (!this.disableValidate) {
      this.validate();
      if (!this.valid) {
        return;
      }
    }

    this.ok();
  }
}
</script>
