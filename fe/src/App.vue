<template>
  <v-app>
    <router-view></router-view>
  </v-app>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator'
import VueBase from '@/base/VueBase';
import type {UserExtraA} from '@/packet/user';
import moment from 'moment-timezone';

@Component
export default class App extends VueBase {
  beforeCreate() {
    const dark = this.$localStore.dark;
    const lang = this.$localStore.lang;
    const api = this.$localStore.origin;
    const timezone = this.$localStore.timezone;

    this.$vuetify.theme.dark = dark;
    this.$vuetify.lang.current = lang;
    this.$i18n.locale = lang;
    this.$api.setUrl(api);
    this.$api2.origin = api;
    moment.tz.setDefault(timezone);
    moment.locale(lang);
  }

  created() {
    if (!this.$localStore.alreadySession) {
      return;
    }

    const access = this.$localStore.access;
    const refresh = this.$localStore.refresh;
    const user = this.$localStore.user;
    const preference = this.$localStore.preference;
    console.info(`[APP] Already session information: ${user.username}`)

    // This information is used in APIv1.
    this.$store.commit('user/login', {
      accessToken: access,
      refreshToken: refresh,
      id: user.username || '',
      email: user.email || '',
      phone: user.phone1 || '',
    });

    this.$api2.setDefaultSession(access, refresh, user, preference);
    this.$api2.setDefaultBearerAuthorization(access);

    if (user.extra) {
      this.updateCurrentSettingsFromUserExtra(user.extra);
    } else {
      console.warn('[APP] Not exists user\'s extra information.');
    }
  }

  updateCurrentSettingsFromUserExtra(extra: UserExtraA) {
    if (extra.dark === undefined) {
      console.warn('[APP] Not exists user\'s extra.dark information.');
    } else {
      const dark = extra.dark;
      console.debug(`[APP] User's extra.dark is ${dark}`);
      if (this.$vuetify.theme.dark != dark) {
        this.$vuetify.theme.dark = dark
      }
    }

    if (extra.lang === undefined) {
      console.warn('[APP] Not exists user\'s extra.lang information.');
    } else {
      const lang = extra.lang;
      console.debug(`[APP] User's extra.lang is ${lang}`);
      if (this.$vuetify.lang.current != lang) {
        this.$vuetify.lang.current = lang;
        this.$i18n.locale = lang;
        moment.locale(lang);
      }
    }

    if (extra.timezone === undefined) {
      console.warn('[APP] Not exists user\'s extra.timezone information.');
    } else {
      const timezone = extra.timezone;
      console.debug(`[APP] User's extra.timezone is ${timezone}`);
      moment.tz.setDefault(timezone);
    }
  }
}
</script>
