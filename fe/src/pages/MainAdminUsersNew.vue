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
  msg:
    required_field: "Required field."
    at_least: "At least {0} characters."
    email_format: "Email format is incorrect."
    phone_format: "Phone format is incorrect."
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
  msg:
    required_field: "공백을 허용하지 않습니다."
    at_least: "최소 {0}자 이상 허용됩니다."
    email_format: "이메일 형식이 올바르지 않습니다."
    phone_format: "전화번호 형식이 올바르지 않습니다."
  cancel: "취소"
  signup: "가입"
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-form>
      <v-subheader>{{ $t('header.required') }}</v-subheader>
      <v-divider></v-divider>

      <v-list flat>
        <v-list-item>
          <v-text-field
              dense
              outlined
              type="text"
              autocomplete="off"
              prepend-icon="mdi-account"
              ref="usernameField"
              v-model="username"
              :rules="[rules.required, rules.at_least]"
              :label="$t('label.username')"
              :hint="$t('hint.username')"
          ></v-text-field>
        </v-list-item>

        <v-list-item>
          <v-text-field
              dense
              outlined
              counter
              autocomplete="off"
              prepend-icon="mdi-lock"
              ref="passwordField"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[rules.required, rules.at_least]"
              :label="$t('label.password')"
              :hint="$t('hint.password')"
              @click:append="showPassword = !showPassword"
          ></v-text-field>
        </v-list-item>

        <v-list-item>
          <v-text-field
              dense
              outlined
              counter
              autocomplete="off"
              prepend-icon="mdi-lock-check"
              ref="confirmPasswordField"
              v-model="confirmPassword"
              :type="showConfirmPassword ? 'text' : 'password'"
              :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
              :rules="[rules.required, rules.at_least]"
              :label="$t('label.confirmPassword')"
              :hint="$t('hint.confirmPassword')"
              @click:append="showConfirmPassword = !showConfirmPassword"
          ></v-text-field>
        </v-list-item>
      </v-list>

      <v-subheader>{{ $t('header.profile') }}</v-subheader>
      <v-divider></v-divider>

      <v-list flat>
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
              ref="emailField"
              v-model="email"
              :rules="[rules.email]"
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
              ref="phone1Field"
              v-model="phone1"
              :rules="[rules.phone]"
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
              ref="phone2Field"
              v-model="phone2"
              :rules="[rules.phone]"
              :label="$t('label.phone2')"
              :hint="$t('hint.phone2')"
          ></v-text-field>
        </v-list-item>
      </v-list>

      <v-subheader>{{ $t('header.access') }}</v-subheader>
      <v-divider></v-divider>

      <v-list flat>
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
      </v-list>

      <v-divider></v-divider>

      <v-list flat>
        <v-list-item three-line>
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
              @click="onClickOk"
          >
            {{ $t('signup') }}
          </v-btn>
        </v-list-item>
      </v-list>
    </v-form>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import {User} from '@/apis/api-v2';

const V_TEXT_FIELD_VALIDATE = 'validate';
const AT_LEAST = 4;

@Component({
  components: {
    ToolbarNavigation
  }
})
export default class MainAdminUsersNew extends VueBase {

  private readonly rules = {
    required: (value) => {
      return !!value || this.$t('msg.required_field');
    },
    at_least: (value) => {
      return value.length >= AT_LEAST || this.$t('msg.at_least', [AT_LEAST]);
    },
    email: (value) => {
      if (value) {
        return /^\S+@\S+\.\S+$/.test(value) || this.$t('msg.email_format');
      } else {
        return true;
      }
    },
    phone: (value) => {
      if (value) {
        return /^[-+0-9]+$/.test(value) || this.$t('msg.phone_format');
      } else {
        return true;
      }
    },
  };

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
      text: 'New',
      disabled: true,
    },
  ];

  username = '';
  password = '';
  confirmPassword = '';
  nickname = '';
  email = '';
  phone1 = '';
  phone2 = '';
  isAdmin = false;

  showPassword = false;
  showConfirmPassword = false;
  showSignupLoading = false;

  validateForms(): boolean {
    const fields = [
      this.$refs.usernameField,
      this.$refs.passwordField,
      this.$refs.confirmPasswordField,
      this.$refs.emailField,
      this.$refs.phone1Field,
      this.$refs.phone2Field,
    ];
    let result = true;
    for (const key in fields) {
      const field = fields[key];
      if (!field) {
        continue;
      }

      const validate = field[V_TEXT_FIELD_VALIDATE];
      if (validate === undefined) {
        continue;
      }

      // You need to repeat the validation function for every field.
      if (!validate(true)) {
        result = false;
      }
    }
    return result;
  }

  onClickCancel() {
    this.$router.back();
  }

  onClickOk() {
    if (!this.validateForms()) {
      return;
    }

    const user = {
      username: this.username,
      password: this.$api2.encryptPassword(this.password),
      nickname: this.nickname,
      email: this.email,
      phone1: this.phone1,
      phone2: this.phone2,
      is_admin: this.isAdmin,
    } as User;

    this.showSignupLoading = true;
    this.$api2.postUsers(user)
        .then(() => {
          this.showSignupLoading = false;
          this.moveToMainAdminUsers();
        })
        .catch(error => {
          this.showSignupLoading = false;
        });
  }
}
</script>
