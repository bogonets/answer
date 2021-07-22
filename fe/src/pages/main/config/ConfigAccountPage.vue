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

        <v-list-item link @click.stop="onClickAppearance">
          <v-list-item-icon>
            <v-icon>{{ icons.eye }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('config.account.appearance.title') }}
          </v-list-item-title>
        </v-list-item>

      </v-list>
    </v-navigation-drawer>

    <router-view>
    </router-view>

  </v-container>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { mdiChevronLeft, mdiEye } from '@mdi/js';

@Component
export default class ConfigAccountPage extends Vue {
  readonly icons = {
    chevronLeft: mdiChevronLeft,
    eye: mdiEye,
  };

  miniNavigation = false;

  mounted() {
    this.$router.push('/main/config/account/appearance');
  }

  get username(): string {
    const username = this.$localStore.user.username;
    if (username) {
      return username;
    }
    return this.$t('config.account.unknown_user').toString();
  }

  get usernameAvatar(): string {
    return this.username[0].toUpperCase();
  }

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickAppearance() {
    this.$router.push('/main/config/account/appearance');
  }
}
</script>
