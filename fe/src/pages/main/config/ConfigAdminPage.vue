<i18n lang="yaml">
en:
  title: "Admin Preference"
  overview: "Overview"
  users: "Users"
  groups: "Groups"

ko:
  title: "관리자 설정"
  overview: "개요"
  users: "사용자"
  groups: "그룹"
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

        <v-list-item link @click.stop="onClickFoldNavigation">
          <v-list-item-icon>
            <v-icon>{{ icons.cogOutline }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('title') }}
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

          <v-list-item link @click.stop="onClickOverview">
            <v-list-item-icon>
              <v-icon>{{ icons.viewList }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('overview') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickUsers">
            <v-list-item-icon>
              <v-icon>{{ icons.account }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('users') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickGroups">
            <v-list-item-icon>
              <v-icon>{{ icons.accountGroup }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('groups') }}
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
import VueI18n from '@/translations/VueI18n';
import { Component } from 'vue-property-decorator';
import {
  mdiCogOutline,
  mdiChevronLeft,
  mdiViewList,
  mdiAccount,
  mdiAccountGroup,
} from '@mdi/js';

@Component
export default class ConfigAdminPage extends VueI18n {

  readonly icons = {
    cogOutline: mdiCogOutline,
    chevronLeft: mdiChevronLeft,
    viewList: mdiViewList,
    account: mdiAccount,
    accountGroup: mdiAccountGroup,
  };

  currentSubpageIndex = 0;
  miniNavigation = false;

  mounted() {
    this.moveOverview();
  }

  private movePage(path: string) {
    if (this.$router.currentRoute.path !== path) {
      this.$router.push(path);
    }
  }

  moveOverview() {
    this.movePage('/main/config/admin/overview');
  }

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickOverview() {
    this.moveOverview();
  }

  onClickUsers() {
    this.movePage('/main/config/admin/users');
  }

  onClickGroups() {
    this.movePage('/main/config/admin/groups');
  }
}
</script>
