<i18n lang="yaml">
en:
  header:
    basic: "Edit user"
    detail: "Detail"
  subheader:
    basic: "You can edit the user's basic properties."
    detail: "Detailed information about this account."
  label:
    created_at: "Created At"
    updated_at: "Updated At"
    last_login: "Last signin"
    delete: "Delete a user"
  hint:
    delete: "Please be careful! It cannot be recovered."
  delete_confirm: "Are you sure? Are you really removing this user?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  header:
    basic: "사용자 편집"
    detail: "상세 정보"
  subheader:
    basic: "사용자의 기본 속성을 편집할 수 있습니다."
    detail: "이 계정에 대한 자세한 정보입니다."
  label:
    created_at: "계정 생성일"
    updated_at: "계정 갱신일"
    last_login: "마지막 로그인"
    delete: "사용자 제거"
  hint:
    delete: "주의하세요! 이 명령은 되돌릴 수 없습니다!"
  delete_confirm: "이 사용자를 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <left-title
        :header="$t('header.basic')"
        :subheader="$t('subheader.basic')"
    >
      <form-user
          disable-username
          hide-password
          hide-cancel-button
          :disable-submit-button="!modified"
          :value="current"
          @input="inputCurrent"
          :loading="showSubmitLoading"
          @ok="onClickOk"
      ></form-user>
    </left-title>

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
          <v-btn color="error" @click.stop="onClickDelete">
            {{ $t('delete') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="320">
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
          <v-btn @click="onClickDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn :loading="showDeleteLoading" color="error" @click="onClickDeleteOk">
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
import LeftTitle from '@/components/LeftTitle.vue';
import FormUser, {UserItem} from '@/components/FormUser.vue';
import {UserA, UpdateUserQ} from '@/packet/user';
import * as _ from 'lodash';

@Component({
  components: {
    ToolbarNavigation,
    LeftTitle,
    FormUser,
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

  detailItems = [] as Array<object>;
  current = new UserItem();
  original = new UserItem();

  modified = false;
  showSubmitLoading = false;
  showDeleteDialog = false;
  showDeleteLoading = false;

  get username(): string {
    return this.$route.params.username;
  }

  created() {
    this.requestUser();
  }

  requestUser() {
    this.$api2.getUsersPuser(this.username)
        .then(body => {
          this.updateUser(body);
        })
        .catch(error => {
          this.toastRequestFailure(error);
          this.moveToBack();
        });
  }

  updateUser(user: UserA) {
    const nickname = user.nickname || '';
    const email = user.email || '';
    const phone1 = user.phone1 || '';
    const phone2 = user.phone2 || '';
    const isAdmin = !!user.is_admin;
    const createdAt = user.created_at || '';
    const updatedAt = user.updated_at || '';
    const lastLogin = user.last_login || '';

    this.current.username = this.username;
    this.current.password = '';
    this.current.nickname = nickname;
    this.current.email = email;
    this.current.phone1 = phone1;
    this.current.phone2 = phone2;
    this.current.isAdmin = isAdmin;
    this.original.fromObject(this.current);
    this.modified = !_.isEqual(this.original, this.current);

    this.detailItems = [
      {
        name: this.$t('label.created_at'),
        value: createdAt,
      },
      {
        name: this.$t('label.updated_at'),
        value: updatedAt,
      },
      {
        name: this.$t('label.last_login'),
        value: lastLogin,
      },
    ];
  }

  inputCurrent(value: UserItem) {
    this.current = value;
    this.modified = !_.isEqual(this.original, this.current);
  }

  onClickOk(event: UserItem) {
    const body = {
      nickname: event.nickname,
      email: event.email,
      phone1: event.phone1,
      phone2: event.phone2,
      is_admin: event.isAdmin,
    } as UpdateUserQ;

    this.showSubmitLoading = true;
    this.$api2.patchUsersPuser(this.username, body)
        .then(() => {
          this.showSubmitLoading = false;
          this.toastRequestSuccess();
          this.requestUser();
        })
        .catch(error => {
          this.showSubmitLoading = false;
          this.toastRequestFailure(error);
        });
  }

  // ------
  // Delete
  // ------

  onClickDelete() {
    this.showDeleteDialog = true;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk() {
    this.showDeleteLoading = true;
    this.$api2.deleteUsersPuser(this.username)
        .then(() => {
          this.showDeleteLoading = false;
          this.showDeleteDialog = false;
          this.toastRequestSuccess();
          this.moveToMainAdminUsers();
        })
        .catch(error => {
          this.showDeleteLoading = false;
          this.showDeleteDialog = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
