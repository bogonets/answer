<i18n lang="yaml">
en:
  title: "User Management"
  subtitle: "You can add, edit and remove users."
  new_user: "New User"
  headers:
    username: "Username"
    email: "E-Mail"
    is_admin: "Admin"
    created_at: "Created on"
    last_login: "Last sign-in"
    actions: "Actions"
  loading: "Loading... Please wait"
  empty_user: "Empty User"

ko:
  title: "사용자 관리"
  subtitle: "사용자를 추가하거나 편집 및 제거할 수 있습니다."
  new_user: "새로운 사용자"
  headers:
    username: "사용자명"
    email: "이메일"
    is_admin: "관리자"
    created_at: "생성일"
    last_login: "마지막 로그인"
    actions: "관리"
  loading: "불러오는중 입니다... 잠시만 기다려 주세요."
  empty_user: "사용자가 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <app-bar-title
        flat
        :title="$t('title')"
        :subtitle="$t('subtitle')"
    ></app-bar-title>

    <v-data-table
        :headers="headers"
        :items="users"
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
              label="Search"
              single-line
              hide-details
          ></v-text-field>

          <v-btn color="primary" @click="onClickNewUser">
            {{ $t('new_user') }}
          </v-btn>

        </v-toolbar>
      </template>

      <template v-slot:item.is_admin="{ item }">
        <v-simple-checkbox
            v-model="item.is_admin"
            disabled
        ></v-simple-checkbox>
      </template>

      <template v-slot:item.created_at="{ item }">
        {{ utcToDate(item.created_at) }}
      </template>

      <template v-slot:item.last_login="{ item }">
        {{ utcToDate(item.last_login) }}
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon @click="editUser(item)">
          mdi-pencil
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_user') }}
      </template>

    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import AppBarTitle from '@/components/AppBarTitle.vue';

@Component({
  components: {
    AppBarTitle
  }
})
export default class UsersPage extends VueBase {

  filterText = "";
  headers: object = [];
  users: object = [];
  showLoading = true;

  created() {
    this.headers = [
      {
        text: this.$t('headers.username').toString(),
        align: 'start',
        filterable: true,
        value: 'username',
      },
      {
        text: this.$t('headers.email').toString(),
        filterable: true,
        value: 'email',
      },
      {
        text: this.$t('headers.is_admin').toString(),
        filterable: false,
        value: 'is_admin',
      },
      {
        text: this.$t('headers.created_at').toString(),
        filterable: false,
        value: 'created_at',
      },
      {
        text: this.$t('headers.last_login').toString(),
        filterable: false,
        value: 'last_login',
      },
      {
        text: this.$t('headers.actions').toString(),
        align: 'end',
        filterable: false,
        sortable: false,
        value: 'actions',
      },
    ]
  }

  mounted() {
    this.$api2.getUsers()
        .then(response => {
          console.info(response);
          this.users = response;
          this.showLoading = false;
        })
        .catch(error => {
          console.error(error);
          this.showLoading = false;
        });
  }

  utcToDate(utc: string): string {
    // Note: Parsing of strings with `Date.parse` is strongly discouraged due to browser
    // differences and inconsistencies.

    // Example: 2021-07-24T08:24:29.315870
    return utc.split("T")[0];
  }

  editUser(item) {
  }

  onClickNewUser() {
  }
}
</script>
