<i18n lang="yaml">
en:
  unknown_user: 'Unknown'
  user_setting: 'Account setting'
  admin_setting: 'Admin setting'
  development_tools: 'DevTools'
  about_answer: 'About Answer'
  signout: 'Sign out'

ko:
  unknown_user: '알수없음'
  user_setting: '개인 설정'
  admin_setting: '관리자 설정'
  development_tools: '개발 도구'
  about_answer: '엔서에 대해'
  signout: '로그아웃'
</i18n>

<template>
  <v-menu
    left
    bottom
    offset-y
    :z-index="menuZIndex"
    open-on-click
    transition="slide-y-transition"
    :close-on-content-click="true"
  >
    <template v-slot:activator="{on, attrs}">
      <v-btn icon v-bind="attrs" v-on="on">
        <v-icon>mdi-account-circle</v-icon>
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
          <v-icon>mdi-account-cog-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('user_setting') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item v-if="hasAdminPermission" @click="onClickAdminConfig">
        <v-list-item-icon>
          <v-icon>mdi-cog-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('admin_setting') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item
        v-if="hasAdminPermission && isDeveloperMode"
        @click="onClickDevelopmentTools"
      >
        <v-list-item-icon>
          <v-icon>mdi-dev-to</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('development_tools') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item @click="onClickAboutAnswer">
        <v-list-item-icon>
          <v-icon>mdi-information-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('about_answer') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

      <v-list-item @click="onClickLogout">
        <v-list-item-icon>
          <v-icon>mdi-logout</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('signout') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {onSignoutEvent} from '@/event/session';

@Component
export default class MenuAccount extends VueBase {
  private readonly menuZIndex = 100;

  get hasAdminPermission(): boolean {
    return this.$localStore.user.admin || false;
  }

  get isDeveloperMode(): boolean {
    return this.hasAdminPermission && this.$localStore.devEnable;
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
    this.moveToSelf();
  }

  onClickAdminConfig() {
    this.moveToAdmin();
  }

  onClickDevelopmentTools() {
    this.moveToDev();
  }

  onClickAboutAnswer() {
    this.moveToRootAbout();
  }

  onClickLogout() {
    onSignoutEvent(this);
    this.moveToSignin();
  }
}
</script>
