<i18n lang="yaml">
en:
  header:
    required: "Required information"
    profile: "User profile"
    access: "Access"
    detail: "Detail"
  subheader:
    required: "This information is essential for registration."
    profile: "Although not required, the information is for convenience."
    access: "Permission to control the system."
    detail: "Detailed information about this account."
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
    delete: "Delete a user"
  hint:
    username: "ID to use when sign in."
    nickname: "Please enter your nickname that will be displayed on the screen."
    email: "Please enter the email address to be used in case of loss of ID and password."
    phone1: "This is the representative phone number."
    phone2: "Secondary phone number."
    is_admin: "Gain full control over the system."
    delete: "Please be careful! It cannot be recovered."
  delete_confirm: "Are you sure? Are you really removing this user?"
  delete: "Delete"
  cancel: "Cancel"
  clear: "Clear"
  submit: "Submit"

ko:
  header:
    required: "필수 정보"
    profile: "사용자 프로필"
    access: "접근 권한"
    detail: "상세 정보"
  subheader:
    required: "가입에 반드시 필요한 정보 입니다."
    profile: "필수 사항은 아니지만 편의성을 위한 정보입니다."
    access: "시스템을 제어할 수 있는 권한 입니다."
    detail: "이 계정에 대한 자세한 정보입니다."
  label:
    username: "사용자명"
    nickname: "별칭"
    email: "이메일"
    phone1: "전화번호1"
    phone2: "전화번호2"
    is_admin: "관리자"
    created_at: "계정 생성일"
    updated_at: "계정 갱신일"
    last_login: "마지막 로그인"
    delete: "사용자 제거"
  hint:
    username: "로그인시 사용할 아이디 입니다."
    nickname: "화면에 표시될 당신의 별명을 입력해 주세요."
    email: "아이디 및 비밀번호 분실시 사용될 이메일 주소를 입력해 주세요."
    phone1: "대표 전화번호 입니다."
    phone2: "보조 전화번호 입니다."
    is_admin: "시스템을 완전히 제어할 수 있는 권한을 획득합니다."
    delete: "주의하세요! 이 명령은 되돌릴 수 없습니다!"
  delete_confirm: "이 사용자를 정말 제거합니까?"
  delete: "제거"
  cancel: "취소"
  clear: "복구"
  submit: "제출"
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

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
      <v-form>
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

        <v-row no-gutters>
          <v-spacer></v-spacer>
          <v-btn
              color="second"
              class="mr-4"
              @click="onClickClear"
          >
            {{ $t('clear') }}
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
      </v-form>
    </left-title>

    <v-divider></v-divider>

    <left-title
        :header="$t('header.access')"
        :subheader="$t('subheader.access')"
    >
      <right-control
          :title="$t('label.is_admin')"
          :subtitle="$t('hint.is_admin')"
      >
        <v-switch
            inset
            v-model="isAdmin"
            :loading="showIsAdminLoading"
            :disabled="showIsAdminLoading"
            @change="onChangeIsAdmin"
        ></v-switch>
      </right-control>
    </left-title>

    <v-divider></v-divider>

    <left-title
        :header="$t('header.detail')"
        :subheader="$t('subheader.detail')"
    >
      <v-card outlined>
        <v-data-table
            hide-default-header
            hide-default-footer
            :headers="detailHeaders"
            :items="detailItems"
            item-key="name"
            class="elevation-1"
        ></v-data-table>
      </v-card>
    </left-title>

    <v-divider></v-divider>

    <v-alert outlined prominent type="error" class="ma-4">
      <v-row align="center" class="pl-4">
        <v-col>
          <v-row>
            <h6 class="text-h6">{{ $t('label.delete') }}</h6>
          </v-row>
          <v-row>
            <span class="text-body-2">{{ $t('hint.delete') }}</span>
          </v-row>
        </v-col>
        <v-col class="shrink">
          <v-btn
              color="error"
              @click.stop="onClickDelete"
          >
            {{ $t('delete') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Delete a user dialog. -->
    <v-dialog v-model="showDeleteUserDialog" max-width="320">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('label.delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('delete_confirm') }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickDeleteUserCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn
              :loading="showDeleteLoading"
              color="error"
              @click="onClickDeleteUserOk"
          >
            {{ $t('delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import TextFieldThreeLine from '@/components/TextFieldThreeLine.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import RightControl from '@/components/RightControl.vue';
import {User} from '@/apis/api-v2';

@Component({
  components: {
    RightControl,
    ToolbarNavigation,
    TextFieldThreeLine,
    LeftTitle,
  }
})
export default class MainAdminUsersEdit extends VueBase {
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
  private readonly detailHeaders = [
    {
      text: 'name',
      value: 'name',
      align: 'right',
    },
    {
      text: 'value',
      value: 'value',
    },
  ];

  detailItems: Array<object> = [];
  originalUser: User = {};

  nickname = '';
  email = '';
  phone1 = '';
  phone2 = '';
  isAdmin = false;

  disableSubmit = true;
  showPassword = false;
  showConfirmPassword = false;
  showIsAdminLoading = false;
  showSignupLoading = false;
  showDeleteUserDialog = false;
  showDeleteLoading = false;

  mounted() {
    const user = this.$route.params.user as User;
    const username = user?.username || '';
    if (!username) {
      console.error('Username is not exists.');
      this.moveToMainAdminUsers();
    }

    this.nickname = user.nickname || '';
    this.email = user.email || '';
    this.phone1 = user.phone1 || '';
    this.phone2 = user.phone2 || '';
    this.isAdmin = !!user.is_admin;
    const created_at = user.created_at || '';
    const updated_at = user.updated_at || '';
    const last_login = user.last_login || '';

    this.originalUser = {
      username: username,
      nickname: this.nickname,
      email: this.email,
      phone1: this.phone1,
      phone2: this.phone2,
      is_admin: this.isAdmin,
      created_at: created_at,
      updated_at: updated_at,
      last_login: last_login,
    } as User;

    this.detailItems = [
      {
        name: this.$t('label.created_at'),
        value: created_at,
      },
      {
        name: this.$t('label.updated_at'),
        value: updated_at,
      },
      {
        name: this.$t('label.last_login'),
        value: last_login,
      },
    ];
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
    return this.originalUser.phone2 != this.phone2;
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

  onChangeIsAdmin(value: boolean | null) {
    const isAdminFlag = !!value;
    const patchUser = {is_admin: isAdminFlag} as User;
    this.showIsAdminLoading = true;
    this.$api2.patchUsersUser(this.username, patchUser)
        .then(() => {
          this.isAdmin = isAdminFlag;
          this.showIsAdminLoading = false;
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.isAdmin = !isAdminFlag;
          this.showIsAdminLoading = false;
          this.toastRequestFailure(error);
        });
  }

  onClickDelete() {
    this.showDeleteUserDialog = true;
  }

  onClickClear() {
    this.nickname = this.originalUser.nickname || '';
    this.email = this.originalUser.email || '';
    this.phone1 = this.originalUser.phone1 || '';
    this.phone2 = this.originalUser.phone2 || '';
    this.validateSubmit();
  }

  onClickSubmit() {
    const patchUser = {
      nickname: this.nickname,
      email: this.email,
      phone1: this.phone1,
      phone2: this.phone2,
    } as User;

    this.showSignupLoading = true;
    this.$api2.patchUsersUser(this.username, patchUser)
        .then(() => {
          this.showSignupLoading = false;
          this.toastRequestSuccess();

          this.originalUser.nickname = patchUser.nickname;
          this.originalUser.email = patchUser.email;
          this.originalUser.phone1 = patchUser.phone1;
          this.originalUser.phone2 = patchUser.phone2;
          this.validateSubmit();
        })
        .catch(error => {
          this.showSignupLoading = false;
          this.toastRequestFailure(error);
        });
  }

  onClickDeleteUserCancel() {
    this.showDeleteUserDialog = false;
  }

  onClickDeleteUserOk() {
    this.showDeleteLoading = true;
    this.$api2.deleteUsersUser(this.username)
        .then(() => {
          this.showDeleteLoading = false;
          this.showDeleteUserDialog = false;
          this.toastRequestSuccess();
          this.moveToMainAdminUsers();
        })
        .catch(error => {
          this.showDeleteLoading = false;
          this.showDeleteUserDialog = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
