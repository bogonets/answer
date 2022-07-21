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
    secession: 'Secession User'
  hint:
    secession: 'Please be careful! It cannot be recovered.'
  secession_confirm: 'Are you sure? Are you sure you want to secession?'
  cancel: 'Cancel'
  secession: 'Secession'

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
    secession: '사용자 탈퇴'
  hint:
    secession: '주의하세요! 이 명령은 되돌릴 수 없습니다!'
  secession_confirm: '정말로 탈퇴합니까?'
  cancel: '취소'
  secession: '탈퇴'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <left-title :header="$t('header.basic')" :subheader="$t('subheader.basic')">
      <form-user
        disable-username
        disable-access
        hide-password
        hide-cancel-button
        hide-access
        :disable-submit-button="!modified"
        :value="current"
        @input="onInputCurrent"
        :loading="showSubmitLoading"
        @ok="onClickOk"
      ></form-user>
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
            <h6 class="text-h6">{{ $t('label.secession') }}</h6>
          </v-row>
          <v-row>
            <span class="text-body-2">{{ $t('hint.secession') }}</span>
          </v-row>
        </v-col>
        <v-col class="shrink">
          <v-btn color="error" @click.stop="onClickDelete">
            {{ $t('secession') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Secession dialog. -->
    <v-dialog v-model="showSecessionDialog" :max-width="dialogMaxWidth">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('label.secession') }}
        </v-card-title>
        <v-card-text>
          {{ $t('secession_confirm') }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn :loading="loadingSecession" color="error" @click="onClickDeleteOk">
            {{ $t('secession') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import {Component, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import FormUser, {UserItem} from '@/components/FormUser.vue';
import type {UpdateUserQ, UserA} from '@recc/api/dist/packet/user';
import {iso8601ToLocal} from '@/chrono/iso8601';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
    FormUser,
  },
})
export default class SelfProfile extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Self',
      disabled: false,
      href: () => this.moveToSelf(),
    },
    {
      text: 'Profile',
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

  @Prop({type: Number, default: 320})
  readonly dialogMaxWidth!: number;

  detailItems = [] as Array<object>;
  current = new UserItem();
  original = new UserItem();

  modified = false;
  showSubmitLoading = false;
  showSecessionDialog = false;
  loadingSecession = false;

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
    const nickname = user.nickname;
    const email = user.email || '';
    const phone = user.phone || '';
    const admin = user.admin;
    const createdAt = user.created_at;
    const updatedAt = user.updated_at;
    const lastLogin = user.last_login || '';

    this.current.username = user.username;
    this.current.password = '';
    this.current.nickname = nickname;
    this.current.email = email;
    this.current.phone = phone;
    this.current.admin = admin;
    this.original.fromObject(this.current);
    this.modified = !this.original.isEqual(this.current);

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

  onInputCurrent(value: UserItem) {
    this.current = value;
    this.modified = !this.original.isEqual(this.current);
  }

  onClickOk(event: UserItem) {
    const body = {
      nickname: event.nickname,
      email: event.email,
      phone: event.phone,
      admin: event.admin,
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
    this.showSecessionDialog = true;
  }

  onClickDeleteCancel() {
    this.showSecessionDialog = false;
  }

  onClickDeleteOk() {
    this.loadingSecession = true;
    this.$api2
      .deleteSelf()
      .then(() => {
        this.loadingSecession = false;
        this.showSecessionDialog = false;
        this.toastRequestSuccess();
        this.$localStore.clearSession();
        this.moveToSignin();
      })
      .catch(error => {
        this.loadingSecession = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
