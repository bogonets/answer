<i18n lang="yaml">
en:
  unknown_user: "Unknown"
  user_setting: "Account setting"
  admin_setting: "Setting"
  development_tools: "DevTools"
  about_answer: "About Answer"
  signout: "Sign out"

ko:
  unknown_user: "알수없음"
  user_setting: "개인 설정"
  admin_setting: "관리자 설정"
  development_tools: "개발 도구"
  about_answer: "엔서에 대해"
  signout: "로그아웃"
</i18n>

<template>
  <v-menu
      left
      bottom
      offset-y
      open-on-click
      transition="slide-y-transition"
      :close-on-content-click="true"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon v-bind="attrs" v-on="on">
        <v-icon role="img" aria-hidden="false">
          {{ icons.accountCircle }}
        </v-icon>
      </v-btn>
    </template>

    <v-list dense>

      <v-list-item>
        <v-list-item-avatar>
          <v-avatar color="accent" size="24">{{ usernameAvatar }}</v-avatar>
        </v-list-item-avatar>
        <v-list-item-title>
          {{ username }}
        </v-list-item-title>
      </v-list-item>

      <v-divider></v-divider>

      <v-list-item @click="onClickAccountConfig">
        <v-list-item-icon>
          <v-icon role="img" aria-hidden="false">
            {{ icons.accountCogOutline }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('user_setting') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item v-if="hasAdminPermission" @click="onClickAdminConfig">
        <v-list-item-icon>
          <v-icon role="img" aria-hidden="false">
            {{ icons.cogOutline }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('admin_setting') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item v-if="isDeveloperMode" @click="onClickDevelopmentTools">
        <v-list-item-icon>
          <v-icon role="img" aria-hidden="false">
            {{ icons.devTo }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('development_tools') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item @click="onClickAboutAnswer">
        <v-list-item-icon>
          <v-icon role="img" aria-hidden="false">
            {{ icons.informationOutline }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('about_answer') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list-item @click="onClickLogout">
        <v-list-item-icon>
          <v-icon role="img" aria-hidden="false">
            {{ icons.logout }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('signout') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import VueI18n from '@/translations/VueI18n';
import { Component } from 'vue-property-decorator';
import {
  mdiAccountCircle,
  mdiAccountCogOutline,
  mdiCogOutline,
  mdiDevTo,
  mdiLogout,
  mdiInformationOutline,
} from '@mdi/js';

@Component
export default class MenuAccount extends VueI18n {

  readonly icons = {
    accountCircle: mdiAccountCircle,
    accountCogOutline: mdiAccountCogOutline,
    cogOutline: mdiCogOutline,
    devTo: mdiDevTo,
    informationOutline: mdiInformationOutline,
    logout: mdiLogout,
  };

  // Computed

  get hasAdminPermission(): boolean {
    return this.$localStore.user.is_admin || false;
  }

  get isDeveloperMode(): boolean {
    return process.env.NODE_ENV !== 'production';
  }

  get usernameAvatar(): string {
    const username = this.$localStore.user.username;
    if (username) {
      return username[0].toUpperCase();
    }
    return '';
  }

  get username(): string {
    const username = this.$localStore.user.username;
    if (username) {
      return username;
    }
    return this.$t('unknown_user').toString();
  }

  // Method.

  onClickAccountConfig() {
    this.$router.push('/main/config/account');
  }

  onClickAdminConfig() {
    this.$router.push('/main/config/admin');
  }

  onClickDevelopmentTools() {
    this.$router.push('/main/dev');
  }

  onClickAboutAnswer() {
    this.$router.push('/main/about');
  }

  onClickLogout() {
    this.$localStore.clearSession();
    this.$store.commit('user/logout');
    this.$router.push('/');
  }
}
</script>