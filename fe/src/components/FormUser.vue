<i18n lang="yaml">
en:
  label:
    username: 'Username (Required)'
    password: 'Password (Required)'
    confirm_password: 'Confirm (Required)'
    nickname: 'Nickname'
    email: 'E-Mail'
    phone: 'Phone'
    is_admin: 'Administrator'
  hint:
    username: 'Please enter the ID to be used when sign in.'
    password: 'Please enter the password to be used when sign in.'
    confirm_password: 'Please enter your password again.'
    nickname: 'Please enter your nickname that will be displayed on the screen.'
    email: 'Please enter the email address to be used in case of loss of ID and password.'
    phone: 'This is the representative phone number.'
    is_admin: 'Gain full control over the system.'
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
    is_admin: '관리자'
  hint:
    username: '로그인시 사용할 아이디를 입력해 주세요.'
    password: '로그인시 사용할 비밀번호를 입력해 주세요.'
    confirm_password: '비밀번호를 한번 더 입력해 주세요.'
    nickname: '화면에 표시될 당신의 별명을 입력해 주세요.'
    email: '아이디 및 비밀번호 분실시 사용될 이메일 주소를 입력해 주세요.'
    phone: '대표 전화번호 입니다.'
    is_admin: '시스템을 완전히 제어할 수 있는 권한을 획득합니다.'
  msg:
    confirm_password: '비밀번호를 재확인해주세요.'
  cancel: '취소'
  submit: '제출'
</i18n>

<template>
  <v-form ref="form" v-model="valid">
    <p :class="subtitleClass">{{ $t('label.username') }}</p>
    <v-text-field
      dense
      type="text"
      autocomplete="off"
      :value="value.username"
      @input="onInputUsername"
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
        :value="value.password"
        @input="onInputPassword"
        :rules="rules.password"
        :hint="$t('hint.password')"
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
    </div>

    <div v-if="!hideProfile">
      <p :class="subtitleClass">{{ $t('label.nickname') }}</p>
      <v-text-field
        dense
        persistent-hint
        :value="value.nickname"
        @input="onInputNickname"
        :hint="$t('hint.nickname')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('label.email') }}</p>
      <v-text-field
        dense
        persistent-hint
        :value="value.email"
        @input="onInputEmail"
        :rules="rules.email"
        :hint="$t('hint.email')"
      ></v-text-field>

      <p :class="subtitleClass">{{ $t('label.phone') }}</p>
      <v-text-field
        dense
        persistent-hint
        :value="value.phone"
        @input="onInputPhone"
        :rules="rules.phone"
        :hint="$t('hint.phone')"
      ></v-text-field>
    </div>

    <v-row v-if="!hideAccess" class="mt-2" no-gutters>
      <div>
        <p :class="subtitleClass">{{ $t('label.is_admin') }}</p>
        <p class="text-caption text--secondary">{{ $t('hint.is_admin') }}</p>
      </div>
      <v-spacer></v-spacer>
      <div>
        <v-switch
          inset
          :disabled="disableAccess"
          :value="value.admin"
          @change="onChangeIsAdmin"
        ></v-switch>
      </div>
    </v-row>

    <v-row v-if="!hideButtons" class="mt-4 mb-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn v-if="!hideCancelButton" class="mr-4" color="second" @click="cancel">
        {{ $t('cancel') }}
      </v-btn>
      <v-btn
        v-if="!hideSubmitButton"
        color="primary"
        :loading="loading"
        :disabled="disableSubmit"
        @click="onSubmit"
      >
        {{ $t('submit') }}
      </v-btn>
    </v-row>
  </v-form>
</template>

<script lang="ts">
import {Component, Prop, Emit, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {VForm} from 'vuetify/lib/components/VForm';
import {VTextField} from 'vuetify/lib/components/VTextField';
import {USERNAME_RULES, PASSWORD_RULES, PHONE_RULES, EMAIL_RULES} from '@/rules';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

export class UserItem {
  username = '';
  password = '';
  nickname = '';
  email = '';
  phone = '';
  admin = false;

  fromObject(obj?: any) {
    this.username = obj?.username || '';
    this.password = obj?.password || '';
    this.nickname = obj?.nickname || '';
    this.email = obj?.email || '';
    this.phone = obj?.phone || '';
    this.admin = obj?.admin || false;
  }

  isEqual(obj?: any) {
    if (typeof obj !== 'object') {
      return false;
    }
    if (this.username !== obj.username) {
      return false;
    }
    if (this.password !== obj.password) {
      return false;
    }
    if (this.nickname !== obj.nickname) {
      return false;
    }
    if (this.email !== obj.email) {
      return false;
    }
    if (this.phone !== obj.phone) {
      return false;
    }
    return this.admin === obj.admin;
  }
}

@Component
export default class FormUser extends VueBase {
  private readonly subtitleClass = SUBTITLE_CLASS;

  private readonly rules = {
    username: USERNAME_RULES,
    password: PASSWORD_RULES,
    confirmPassword: [...PASSWORD_RULES, this.confirmPasswordRule],
    phone: PHONE_RULES,
    email: EMAIL_RULES,
  };

  @Prop({type: Boolean})
  readonly loading!: boolean;

  @Prop({type: Boolean})
  readonly disableUsername!: boolean;

  @Prop({type: Boolean})
  readonly disableAccess!: boolean;

  @Prop({type: Boolean})
  readonly disableSubmitButton!: boolean;

  @Prop({type: Boolean})
  readonly disableValidate!: boolean;

  @Prop({type: Boolean})
  readonly hidePassword!: boolean;

  @Prop({type: Boolean})
  readonly hideProfile!: boolean;

  @Prop({type: Boolean})
  readonly hideAccess!: boolean;

  @Prop({type: Boolean})
  readonly hideButtons!: boolean;

  @Prop({type: Boolean})
  readonly hideCancelButton!: boolean;

  @Prop({type: Boolean})
  readonly hideSubmitButton!: boolean;

  @Prop({type: Object, default: () => new UserItem()})
  readonly value!: UserItem;

  @Ref()
  readonly form!: VForm;

  @Ref()
  readonly confirmPasswordField!: VTextField;

  valid = false;
  confirmPassword = '';

  onInputUsername(event: string) {
    this.value.username = event;
    this.input();
  }

  onInputPassword(event: string) {
    this.value.password = event;
    this.validateConfirmPasswordField();
    this.input();
  }

  onInputConfirmPassword(event: string) {
    this.confirmPassword = event;
    this.input();
  }

  onInputNickname(event: string) {
    this.value.nickname = event;
    this.input();
  }

  onInputEmail(event: string) {
    this.value.email = event;
    this.input();
  }

  onInputPhone(event: string) {
    this.value.phone = event;
    this.input();
  }

  onChangeIsAdmin(event: null | boolean) {
    this.value.admin = !!event;
    this.input();
  }

  confirmPasswordRule(value: string): boolean | string {
    return this.value.password == value || this.$t('msg.confirm_password').toString();
  }

  validateConfirmPasswordField() {
    this.confirmPasswordField['validate']();
  }

  get disableSubmit(): boolean {
    const samePassword = this.value.password === this.confirmPassword;
    return this.loading || !(this.valid && samePassword) || this.disableSubmitButton;
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
    if (!this.disableValidate) {
      this.formValidate();
      if (!this.valid) {
        return;
      }
    }
    this.ok();
  }

  @Emit()
  input() {
    return this.value;
  }

  @Emit()
  cancel() {
    return this.value;
  }

  @Emit()
  ok() {
    return this.value;
  }
}
</script>
