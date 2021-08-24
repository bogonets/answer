<i18n lang="yaml">
en:
  search_label: "You can filter by username or email."
  new_item: "New User"
  headers:
    username: "Username"
    email: "E-Mail"
    is_admin: "Admin"
    created_at: "Created at"
    last_login: "Last sign-in"
    actions: "Actions"
  loading: "Loading... Please wait"
  empty_item: "Empty User"

ko:
  search_label: "사용자명 또는 이메일을 필터링할 수 있습니다."
  new_item: "새로운 사용자"
  headers:
    username: "사용자명"
    email: "이메일"
    is_admin: "관리자"
    created_at: "생성일"
    last_login: "마지막 로그인"
    actions: "관리"
  loading: "불러오는중 입니다... 잠시만 기다려 주세요."
  empty_item: "사용자가 존재하지 않습니다."
</i18n>

<template>
  <v-container>

    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-data-table
        :headers="headers"
        :items="tableItems"
        :search="filterText"
        :loading="showLoading"
        :loading-text="$t('loading')"
    >

      <template v-slot:top>
        <v-toolbar flat>

          <v-text-field
              class="mr-4"
              v-model="filterText"
              append-icon="mdi-magnify"
              :label="$t('search_label')"
              single-line
              hide-details
          ></v-text-field>

          <v-btn color="primary" @click="onClickNew">
            {{ $t('new_item') }}
          </v-btn>

        </v-toolbar>
      </template>

      <template v-slot:item.is_admin="{ item }">
        <v-icon dense v-if="!!item.is_admin">mdi-check</v-icon>
      </template>

      <template v-slot:item.created_at="{ item }">
        {{ utcToDate(item.created_at) }}
      </template>

      <template v-slot:item.last_login="{ item }">
        {{ utcToDate(item.last_login) }}
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon small @click="onClickEdit(item)">
          mdi-pencil
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_item') }}
      </template>

    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import AppBarTitle from '@/components/AppBarTitle.vue';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import {UserA} from '@/packet/user';

@Component({
  components: {
    ToolbarNavigation,
    AppBarTitle
  }
})
export default class AdminUsers extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdminOverview(),
    },
    {
      text: 'Users',
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.username').toString(),
      align: 'start',
      filterable: true,
      value: 'username',
    },
    {
      text: this.$t('headers.email').toString(),
      align: 'center',
      filterable: true,
      value: 'email',
    },
    {
      text: this.$t('headers.is_admin').toString(),
      align: 'center',
      filterable: false,
      value: 'is_admin',
    },
    {
      text: this.$t('headers.created_at').toString(),
      align: 'center',
      filterable: false,
      value: 'created_at',
    },
    {
      text: this.$t('headers.last_login').toString(),
      align: 'center',
      filterable: false,
      value: 'last_login',
    },
    {
      text: this.$t('headers.actions').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'actions',
    },
  ]

  filterText = '';
  tableItems: Array<UserA> = [];
  showLoading = true;

  mounted() {
    this.$api2.getAdminUsers()
        .then(items => {
          this.tableItems = items;
          this.showLoading = false;
        })
        .catch(error => {
          this.showLoading = false;
          this.toastRequestFailure(error);
        });
  }

  utcToDate(utc: undefined | string): string {
    return utc?.split('T')[0] || '';
  }

  onClickNew() {
    this.moveToAdminUsersNew();
  }

  onClickEdit(item: UserA) {
    this.moveToAdminUsersEdit(item.username);
  }
}
</script>
