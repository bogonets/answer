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
        <v-list-item-icon>
          <v-icon role="img" aria-hidden="false">
            {{ icons.accountCircle }}
          </v-icon>
        </v-list-item-icon>
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
          <v-list-item-title>{{ $t('menu.user.user_setting') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item v-if="hasAdminPermission" @click="onClickAdminConfig">
        <v-list-item-icon>
          <v-icon role="img" aria-hidden="false">
            {{ icons.cogOutline }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('menu.user.admin_setting') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item v-if="isDeveloperMode" @click="onClickDevelopmentTools">
        <v-list-item-icon>
          <v-icon role="img" aria-hidden="false">
            {{ icons.devTo }}
          </v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title>{{ $t('menu.user.development_tools') }}</v-list-item-title>
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
          <v-list-item-title>{{ $t('menu.user.signout') }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import {
  mdiAccountCircle,
  mdiAccountCogOutline,
  mdiCogOutline,
  mdiDevTo,
  mdiLogout,
} from '@mdi/js';

@Component
export default class MenuSelf extends Vue {

  readonly icons = {
    accountCircle: mdiAccountCircle,
    accountCogOutline: mdiAccountCogOutline,
    cogOutline: mdiCogOutline,
    devTo: mdiDevTo,
    logout: mdiLogout,
  };

  // Computed

  get hasAdminPermission(): boolean {
    return this.$localStore.user.is_admin || false;
  }

  get isDeveloperMode(): boolean {
    return process.env.NODE_ENV !== 'production';
  }

  get username(): string {
    const username = this.$localStore.user.username;
    if (username) {
      return username;
    }
    return this.$t('menu.user.unknown_user').toString();
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

  onClickLogout() {
    this.$localStore.clearSession();
    this.$store.commit('user/logout');
    this.$router.push('/');
  }
}
</script>
