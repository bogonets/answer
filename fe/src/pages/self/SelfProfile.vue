<i18n lang="yaml">
en:
  header:
    basic: 'Edit user'
    detail: 'Detail'
  subheader:
    basic: "You can edit the user's basic properties."
    detail: 'Detailed information about this account.'
  label:
    created_at: 'Created At'
    updated_at: 'Updated At'
    last_login: 'Last signin'
    delete: 'Delete User'
  hint:
    delete: 'Please be careful! It cannot be recovered.'
  delete_confirm: 'Are you sure? Are you sure you want to secession?'
  cancel: 'Cancel'
  submit: 'Submit'
  delete: 'Delete'

ko:
  header:
    basic: '사용자 편집'
    detail: '상세 정보'
  subheader:
    basic: '사용자의 기본 속성을 편집할 수 있습니다.'
    detail: '이 계정에 대한 자세한 정보입니다.'
  label:
    created_at: '계정 생성일'
    updated_at: '계정 갱신일'
    last_login: '마지막 로그인'
    delete: '사용자 탈퇴'
  hint:
    delete: '주의하세요! 이 명령은 되돌릴 수 없습니다!'
  delete_confirm: '정말로 탈퇴합니까?'
  cancel: '취소'
  submit: '제출'
  delete: '탈퇴'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <left-title :header="$t('header.basic')" :subheader="$t('subheader.basic')">
      <form-user
        disable-username
        disable-admin
        hide-password
        hide-admin
        :username.sync="current.username"
        :nickname.sync="current.nickname"
        :email.sync="current.email"
        :phone.sync="current.phone"
        :admin.sync="current.admin"
      ></form-user>

      <v-row class="mt-4 mb-2" no-gutters>
        <v-spacer></v-spacer>
        <v-btn color="primary" :disabled="!modified" @click="onSubmit">
          {{ $t('submit') }}
        </v-btn>
      </v-row>
    </left-title>

    <left-title :header="$t('header.detail')" :subheader="$t('subheader.detail')">
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

    <!-- Delete User dialog. -->
    <v-dialog v-model="showDeleteDialog" :max-width="dialogMaxWidth">
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
          <v-btn :loading="loadingDelete" color="error" @click="onClickDeleteOk">
            {{ $t('delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import {Component, Prop, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import FormUser from '@/forms/FormUser.vue';
import type {UpdateUserQ, UserA} from '@recc/api/dist/packet/user';
import {iso8601ToLocal} from '@/chrono/iso8601';
import _ from 'lodash';

interface UserItem {
  username: string;
  nickname: string;
  email: string;
  phone: string;
  admin: boolean;
}

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
    FormUser,
  },
})
export default class SelfProfile extends VueBase {
  readonly navigationItems = [
    {
      text: 'Self',
      disabled: true,
    },
    {
      text: 'Profile',
      disabled: true,
    },
  ];

  readonly detailHeaders = [
    {
      text: 'name',
      value: 'name',
      align: 'right',
    },
    {
      text: 'value',
      value: 'value',
      align: 'left',
    },
  ];

  @Prop({type: Number, default: 320})
  readonly dialogMaxWidth!: number;

  original = {} as UserItem;
  current = {} as UserItem;

  detailItems = [] as Array<object>;

  modified = false;
  showSubmitLoading = false;
  showDeleteDialog = false;
  loadingDelete = false;

  created() {
    this.requestUser();
  }

  requestUser() {
    this.$api2
      .getSelf()
      .then(body => {
        this.updateUser(body);
      })
      .catch(error => {
        this.toastRequestFailure(error);
        // this.moveToBack();
      });
  }

  updateUser(user: UserA) {
    const username = user.username;
    const nickname = user.nickname;
    const email = user.email;
    const phone = user.phone;
    const admin = user.admin;

    this.current = {
      username,
      nickname,
      email,
      phone,
      admin,
    };
    this.original = _.clone(this.current);
    this.modified = false;

    const createdAt = user.created_at;
    const updatedAt = user.updated_at;
    const lastLogin = user.last_login || '';

    this.detailItems = [
      {
        name: this.$t('label.created_at'),
        value: iso8601ToLocal(createdAt),
      },
      {
        name: this.$t('label.updated_at'),
        value: iso8601ToLocal(updatedAt),
      },
      {
        name: this.$t('label.last_login'),
        value: iso8601ToLocal(lastLogin),
      },
    ];
  }

  @Watch('current', {deep: true})
  onWatchCurrent(newValue) {
    this.modified = !_.isEqual(this.original, newValue);
  }

  onSubmit() {
    const body = {
      nickname: this.current.nickname,
      email: this.current.email,
      phone: this.current.phone,
      admin: this.current.admin,
    } as UpdateUserQ;

    this.showSubmitLoading = true;
    this.$api2
      .patchSelf(body)
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
    this.loadingDelete = true;
    this.$api2
      .deleteSelf()
      .then(() => {
        this.loadingDelete = false;
        this.showDeleteDialog = false;
        this.toastRequestSuccess();
        this.$localStore.clearSession();
        this.moveToSignin();
      })
      .catch(error => {
        this.loadingDelete = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
