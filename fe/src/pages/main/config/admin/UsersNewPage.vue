<i18n lang="yaml">
en:
  title: "Add user"
  subtitle: "Register a new user"
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
  cancel: "Cancel"
  signup: "Signup"

ko:
  title: "사용자 추가"
  subtitle: "새로운 사용자를 등록합니다."
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
    confirmPassword: "비밀번호를 다시 입력해 주세요."
    nickname: "화면에 표시될 당신의 별명을 입력해 주세요."
    email: "아이디 및 비밀번호 분실시 사용될 이메일 주소를 입력해 주세요."
    phone1: "대표 전화번호 입니다."
    phone2: "보조 전화번호 입니다."
    is_admin: "시스템을 완전히 제어할 수 있는 권한을 획득합니다."
  cancel: "취소"
  signup: "가입"
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

      <v-list flat>
        <v-subheader>{{ $t('header.required') }}</v-subheader>

        <v-list-item>
          <v-text-field
              dense
              outlined
              persistent-hint
              type="text"
              autocomplete="off"
              ref="usernameField"
              v-model="username"
              :label="$t('label.username')"
              :hint="$t('hint.username')"
          ></v-text-field>
        </v-list-item>

        <v-list-item>
          <v-text-field
              dense
              outlined
              persistent-hint
              type="password"
              autocomplete="off"
              ref="password"
              v-model="password"
              :label="$t('label.password')"
              :hint="$t('hint.password')"
          ></v-text-field>
        </v-list-item>

        <v-list-item>
          <v-text-field
              dense
              outlined
              persistent-hint
              type="password"
              autocomplete="off"
              ref="password"
              v-model="confirmPassword"
              :label="$t('label.confirmPassword')"
              :hint="$t('hint.confirmPassword')"
          ></v-text-field>
        </v-list-item>

        <v-divider></v-divider>
        <v-subheader>{{ $t('header.profile') }}</v-subheader>

        <v-list-item>
          <v-text-field
              dense
              outlined
              persistent-hint
              type="text"
              autocomplete="off"
              ref="nicknameField"
              v-model="nickname"
              :label="$t('label.nickname')"
              :hint="$t('hint.nickname')"
          ></v-text-field>
        </v-list-item>

        <v-list-item>
          <v-text-field
              dense
              outlined
              persistent-hint
              type="text"
              autocomplete="off"
              ref="emailField"
              v-model="email"
              :label="$t('label.email')"
              :hint="$t('hint.email')"
          ></v-text-field>
        </v-list-item>

        <v-list-item>
          <v-text-field
              dense
              outlined
              persistent-hint
              type="text"
              autocomplete="off"
              ref="phone1Field"
              v-model="phone1"
              :label="$t('label.phone1')"
              :hint="$t('hint.phone1')"
          ></v-text-field>
        </v-list-item>

        <v-list-item>
          <v-text-field
              dense
              outlined
              persistent-hint
              type="text"
              autocomplete="off"
              ref="phone2Field"
              v-model="phone2"
              :label="$t('label.phone2')"
              :hint="$t('hint.phone2')"
          ></v-text-field>
        </v-list-item>

        <v-divider></v-divider>
        <v-subheader>{{ $t('header.access') }}</v-subheader>

        <v-list-item three-line>
          <v-list-item-content>
            <v-list-item-title>{{ $t('label.is_admin') }}</v-list-item-title>
            <v-list-item-subtitle>{{ $t('hint.is_admin') }}</v-list-item-subtitle>
          </v-list-item-content>

          <v-switch
              inset
              v-model="isAdmin"
          ></v-switch>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item three-line>
          <v-spacer></v-spacer>
          <v-btn color="second" class="mr-4">{{ $t('cancel') }}</v-btn>
          <v-btn color="primary">{{ $t('signup') }}</v-btn>
        </v-list-item>

      </v-list>

  </v-container>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation
  }
})
export default class UsersNewPage extends VueBase {

  navigationItems: object = [];
  username = '';
  password = '';
  confirmPassword = '';
  nickname = '';
  email = '';
  phone1 = '';
  phone2 = '';
  isAdmin = false;

  created() {
    this.navigationItems = [
      {
        text: 'Admin',
        disabled: false,
        href: this.paths.mainConfigAdminOverview,
      },
      {
        text: 'Users',
        disabled: false,
        href: this.paths.mainConfigAdminUsers,
      },
      {
        text: 'New',
        disabled: true,
      },
    ];
  }
}
</script>
