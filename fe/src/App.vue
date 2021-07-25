<template>
  <v-app>
    <router-view />
  </v-app>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator'
import VueBase from "@/base/VueBase";
import { Extra } from "@/apis/api-v2";

@Component
export default class App extends VueBase {
  beforeCreate() {
    const dark = this.$localStore.dark;
    const lang = this.$localStore.lang;
    const api = this.$localStore.origin;

    this.$vuetify.theme.dark = dark;
    this.$vuetify.lang.current = lang;
    this.$i18n.locale = lang;
    this.$api.setUrl(api);
    this.$api2.origin = api;
  }

  created() {
    if (!this.$localStore.alreadySession) {
      return;
    }

    const access = this.$localStore.access;
    const refresh = this.$localStore.refresh;
    const user = this.$localStore.user;
    console.info(`[APP] Already session information: ${user.username}`)

    // This information is used in APIv1.
    this.$store.commit('user/login', {
      accessToken: access,
      refreshToken: refresh,
      id: user.username || '',
      email: user.email || '',
      phone: user.phone1 || '',
    });

    this.$api2.setDefaultSession(access, refresh, user);
    this.$api2.setDefaultBearerAuthorization(access);

    if (user.extra) {
      this.updateCurrentSettingsFromUserExtra(user.extra);
    } else {
      console.warn('[APP] Not exists user\'s extra information.');
    }
  }

  updateCurrentSettingsFromUserExtra(extra: Extra) {
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
      }
    }
  }
}
</script>
