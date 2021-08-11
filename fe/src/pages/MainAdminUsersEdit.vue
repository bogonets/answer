<i18n lang="yaml">
en:
  title: "Add user"
  subtitle: "Register a new user"
  header:
    required: "Required information"
    profile: "User profile"
    access: "Access"
    status: "Status"
  subheader:
    required: "This information is essential for registration."
    profile: "Although not required, the information is for convenience."
    access: "Permission to control the system."
    status: "Information that can check the status of your account."
  label:
    username: "Username"
    nickname: "Nickname"
    email: "E-Mail"
    phone1: "Phone1"
    phone2: "Phone2"
    is_admin: "Administrator"
    created_at: "Created At"
    updated_at: "Updated At"
    last_login: "Last signin"
  hint:
    username: "ID to use when sign in."
    nickname: "Please enter your nickname that will be displayed on the screen."
    email: "Please enter the email address to be used in case of loss of ID and password."
    phone1: "This is the representative phone number."
    phone2: "Secondary phone number."
    is_admin: "Gain full control over the system."
  msg:
    required_field: "Required field."
    at_least: "At least {0} characters."
    email_format: "Email format is incorrect."
    phone_format: "Phone format is incorrect."
  cancel: "Cancel"
  submit: "Submit"

ko:
  title: "사용자 추가"
  subtitle: "새로운 사용자를 등록합니다."
  header:
    required: "필수 정보"
    profile: "사용자 프로필"
    access: "접근 권한"
    status: "상태 정보"
  subheader:
    required: "가입에 반드시 필요한 정보 입니다."
    profile: "필수 사항은 아니지만 편의성을 위한 정보입니다."
    access: "시스템을 제어할 수 있는 권한 입니다."
    status: "계정 상태를 확인할 수 있는 정보 입니다."
  label:
    username: "사용자명"
    nickname: "별칭"
    email: "이메일"
    phone1: "전화번호1"
    phone2: "전화번호2"
    is_admin: "관리자"
    created_at: "생성일"
    updated_at: "갱신일"
    last_login: "마지막 로그인"
  hint:
    username: "로그인시 사용할 아이디 입니다."
    nickname: "화면에 표시될 당신의 별명을 입력해 주세요."
    email: "아이디 및 비밀번호 분실시 사용될 이메일 주소를 입력해 주세요."
    phone1: "대표 전화번호 입니다."
    phone2: "보조 전화번호 입니다."
    is_admin: "시스템을 완전히 제어할 수 있는 권한을 획득합니다."
  msg:
    required_field: "공백을 허용하지 않습니다."
    at_least: "최소 {0}자 이상 허용됩니다."
    email_format: "이메일 형식이 올바르지 않습니다."
    phone_format: "전화번호 형식이 올바르지 않습니다."
  cancel: "취소"
  submit: "제출"
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-form>
      <left-title
          :header="$t('header.required')"
          :subheader="$t('subheader.required')"
      >
        <text-field-three-line
            disabled
            :label="$t('label.username')"
            :hint="$t('hint.username')"
            :value="originalUser.username"
        ></text-field-three-line>
      </left-title>

      <v-divider></v-divider>

      <left-title
          :header="$t('header.profile')"
          :subheader="$t('subheader.profile')"
      >
        <text-field-three-line
            :label="$t('label.nickname')"
            :hint="$t('hint.nickname')"
            :value="nickname"
            @input="onInputNickname"
        ></text-field-three-line>
        <text-field-three-line
            :label="$t('label.email')"
            :hint="$t('hint.email')"
            :value="email"
            @input="onInputEmail"
        ></text-field-three-line>
        <text-field-three-line
            :label="$t('label.phone1')"
            :hint="$t('hint.phone1')"
            :value="phone1"
            @input="onInputPhone1"
        ></text-field-three-line>
        <text-field-three-line
            :label="$t('label.phone2')"
            :hint="$t('hint.phone2')"
            :value="phone2"
            @input="onInputPhone2"
        ></text-field-three-line>
      </left-title>

      <v-divider></v-divider>

      <left-title
          :header="$t('header.access')"
          :subheader="$t('subheader.access')"
      >
        <right-switch
            inset
            :title="$t('label.is_admin')"
            :subtitle="$t('hint.is_admin')"
            :value="isAdmin"
            @input="onInputIsAdmin"
        ></right-switch>
      </left-title>

      <v-divider></v-divider>

      <left-title
          :header="$t('header.status')"
          :subheader="$t('subheader.status')"
      >

        <text-field-three-line
            disabled
            :label="$t('label.created_at')"
            :value="originalUser.created_at"
        ></text-field-three-line>

        <text-field-three-line
            disabled
            :label="$t('label.updated_at')"
            :value="originalUser.updated_at"
        ></text-field-three-line>

        <text-field-three-line
            disabled
            :label="$t('label.last_login')"
            :value="originalUser.last_login"
        ></text-field-three-line>
      </left-title>

      <v-divider></v-divider>

      <v-container class="mt-4">
        <v-row>
          <v-spacer></v-spacer>
          <v-btn
              color="second"
              class="mr-4"
              @click="onClickCancel"
          >
            {{ $t('cancel') }}
          </v-btn>
          <v-btn
              color="primary"
              :loading="showSignupLoading"
              :disabled="disableSubmit"
              @click="onClickSubmit"
          >
            {{ $t('submit') }}
          </v-btn>
        </v-row>
      </v-container>
    </v-form>

    <v-snackbar
        v-model="showRequestErrorSnackbar"
        :timeout="snackbarTimeout"
    >
      {{ requestErrorMessage }}
    </v-snackbar>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import TextFieldThreeLine from '@/components/TextFieldThreeLine.vue';
import LeftTitle from "@/components/LeftTitle.vue";
import RightSwitch from "@/components/RightSwitch.vue";
import {User} from "@/apis/api-v2";

@Component({
  components: {
    ToolbarNavigation,
    TextFieldThreeLine,
    LeftTitle,
    RightSwitch,
  }
})
export default class MainAdminUsersEdit extends VueBase {
  private readonly snackbarTimeout = 4000;
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Users',
      disabled: false,
      href: () => this.moveToMainAdminUsers(),
    },
    {
      text: 'Edit',
      disabled: true,
    },
  ];

  originalUser: User = {};

  nickname = '';
  email = '';
  phone1 = '';
  phone2 = '';
  isAdmin = false;

  disableSubmit = true;
  showPassword = false;
  showConfirmPassword = false;
  showSignupLoading = false;

  showRequestErrorSnackbar = false;
  requestErrorMessage = '';

  mounted() {
    const user = this.$route.params.user as User;

    this.nickname = user.nickname || '';
    this.email = user.email || '';
    this.phone1 = user.phone1 || '';
    this.phone2 = user.phone2 || '';
    this.isAdmin = !!user.is_admin;

    this.originalUser = {
      username: user.username || '',
      nickname: this.nickname,
      email: this.email,
      phone1: this.phone1,
      phone2: this.phone2,
      is_admin: this.isAdmin,
      created_at: user.created_at || '',
      updated_at: user.updated_at || '',
      last_login: user.last_login || '',
    } as User;
    this.validateSubmit();
  }

  get username(): string {
    return this.originalUser.username || '';
  }

  get modified(): boolean {
    if (this.originalUser.nickname != this.nickname) {
      return true;
    }
    if (this.originalUser.email != this.email) {
      return true;
    }
    if (this.originalUser.phone1 != this.phone1) {
      return true;
    }
    if (this.originalUser.phone2 != this.phone2) {
      return true;
    }
    return this.originalUser.is_admin != this.isAdmin;
  }

  showSnackbar(message: string) {
    this.requestErrorMessage = message;
    this.showRequestErrorSnackbar = true;
  }

  validateSubmit() {
    this.disableSubmit = !this.modified;
  }

  onInputNickname(value: string) {
    this.nickname = value;
    this.validateSubmit();
  }

  onInputEmail(value: string) {
    this.email = value;
    this.validateSubmit();
  }

  onInputPhone1(value: string) {
    this.phone1 = value;
    this.validateSubmit();
  }

  onInputPhone2(value: string) {
    this.phone2 = value;
    this.validateSubmit();
  }

  onInputIsAdmin(value: boolean) {
    this.isAdmin = value;
    this.validateSubmit();
  }

  onClickCancel() {
    this.moveToBack();
  }

  onClickSubmit() {
    const username = this.username;
    if (!username) {
      throw Error('Username is not exists.');
    }

    const patchUser = {
      nickname: this.nickname,
      email: this.email,
      phone1: this.phone1,
      phone2: this.phone2,
      is_admin: this.isAdmin,
    } as User;

    this.showSignupLoading = true;
    this.$api2.patchUsersUser(username, patchUser)
        .then(() => {
          this.showSignupLoading = false;
          this.moveToMainAdminUsers();
          this.showSnackbar('Request successful');
        })
        .catch(error => {
          this.showSignupLoading = false;
          const code = error.request.status;
          const reason = error.request.statusText;
          this.showSnackbar(`Request error(${code}) ${reason}`);
        });
  }
}
</script>
