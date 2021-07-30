<i18n lang="yaml">
en:
  appearance: "Appearance"
  unknown_user: "[Unknown User]"

ko:
  appearance: "외관"
  unknown_user: "[알수없는 사용자]"
</i18n>

<template>
  <v-container>

    <v-navigation-drawer
        app
        clipped
        permanent
        stateless
        touchless
        :mini-variant.sync="miniNavigation"
    >
      <v-list nav dense>

        <!-- User Profile -->
        <v-list-item link @click.stop="onClickFoldNavigation">
          <v-list-item-avatar>
            <v-avatar color="accent" size="24">{{ usernameAvatar }}</v-avatar>
          </v-list-item-avatar>
          <v-list-item-title>
            {{ username }}
          </v-list-item-title>
          <v-btn icon @click.stop="onClickFoldNavigation">
            <v-icon>{{ icons.chevronLeft }}</v-icon>
          </v-btn>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item-group
            mandatory
            color="primary"
            :value="currentSubpageIndex"
        >

          <v-list-item link @click.stop="onClickAppearance">
            <v-list-item-icon>
              <v-icon>{{ icons.eye }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('appearance') }}
            </v-list-item-title>
          </v-list-item>

        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <router-view>
    </router-view>

  </v-container>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import { mdiChevronLeft, mdiEye } from '@mdi/js';

@Component
export default class ConfigAccountPage extends VueBase {

  readonly icons = {
    chevronLeft: mdiChevronLeft,
    eye: mdiEye,
  };

  currentSubpageIndex = 0;
  miniNavigation = false;

  mounted() {
    this.moveAppearance();
  }

  get username(): string {
    const username = this.$localStore.user.username;
    if (username) {
      return username;
    }
    return this.$t('unknown_user').toString();
  }

  get usernameAvatar(): string {
    return this.username[0].toUpperCase();
  }

  moveAppearance() {
    this.push('/main/config/account/appearance');
  }

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickAppearance() {
    this.moveAppearance();
  }
}
</script>
