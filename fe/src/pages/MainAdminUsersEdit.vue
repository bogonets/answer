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
    nickname: "Nickname"
    email: "E-Mail"
    phone1: "Phone1"
    phone2: "Phone2"
    is_admin: "Administrator"
  hint:
    username: "Please enter the ID to be used when sign in."
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
  update: "Update"

ko:
  title: "사용자 추가"
  subtitle: "새로운 사용자를 등록합니다."
  header:
    required: "필수 정보"
    profile: "사용자 프로필"
    access: "접근 권한"
  label:
    username: "사용자명"
    nickname: "별칭"
    email: "이메일"
    phone1: "전화번호1"
    phone2: "전화번호2"
    is_admin: "관리자"
  hint:
    username: "로그인시 사용할 아이디를 입력해 주세요."
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
  update: "갱신"
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
              disabled
              type="text"
              autocomplete="off"
              prepend-icon="mdi-account"
              v-model="username"
              :label="$t('label.username')"
              :hint="$t('hint.username')"
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
            {{ $t('update') }}
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
import {User} from "@/apis/api-v2";

const V_TEXT_FIELD_VALIDATE = 'validate';

@Component({
  components: {
    ToolbarNavigation,
  }
})
export default class MainAdminUsersEdit extends VueBase {

  private readonly rules = {
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
      text: 'Edit',
      disabled: true,
    },
  ];

  originalUser: User = {};

  username = '';
  nickname = '';
  email = '';
  phone1 = '';
  phone2 = '';
  isAdmin = false;
  createdAt = '';
  updatedAt = '';
  lastLogin = '';

  showPassword = false;
  showConfirmPassword = false;
  showSignupLoading = false;

  mounted() {
    // this.originalUser = this.routeParamToUser(this.$route.params);
    // console.debug(`Edit User: ${this.$route.params}`)
  }

  validateForms(): boolean {
    const fields = [
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

    // const user = {
    //   username: this.username,
    //   nickname: this.nickname,
    //   email: this.email,
    //   phone1: this.phone1,
    //   phone2: this.phone2,
    //   is_admin: this.isAdmin,
    // } as User;
    //
    // this.showSignupLoading = true;
    // this.$api2.postUsers(user)
    //     .then(() => {
    //       this.showSignupLoading = false;
    //       this.moveToMainConfigAdminUsers();
    //     })
    //     .catch(error => {
    //       this.showSignupLoading = false;
    //     });
  }
}
</script>
