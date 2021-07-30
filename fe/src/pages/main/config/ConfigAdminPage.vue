<i18n lang="yaml">
en:
  title: "Admin Preference"
  overview: "Overview"
  users: "Users"
  groups: "Groups"
  lambdas: "Lambdas"
  features: "Features"
  settings: "Settings"

ko:
  title: "관리자 설정"
  overview: "개요"
  users: "사용자"
  groups: "그룹"
  lambdas: "람다 관리"
  features: "기능 설정"
  settings: "환경 설정"
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
              <v-icon>{{ icons.developerBoard }}</v-icon>
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

          <v-list-item link @click.stop="onClickLambdas">
            <v-list-item-icon>
              <v-icon>{{ icons.lambda }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('lambdas') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickFeatures">
            <v-list-item-icon>
              <v-icon>{{ icons.formatListChecks }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('features') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickSettings">
            <v-list-item-icon>
              <v-icon>{{ icons.cogs }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('settings') }}
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
import {
  mdiCogOutline,
  mdiChevronLeft,
  mdiDeveloperBoard,
  mdiAccount,
  mdiAccountGroup,
  mdiLambda,
  mdiFormatListChecks,
  mdiCogs,
} from '@mdi/js';

@Component
export default class ConfigAdminPage extends VueBase {

  readonly icons = {
    cogOutline: mdiCogOutline,
    chevronLeft: mdiChevronLeft,
    developerBoard: mdiDeveloperBoard,
    account: mdiAccount,
    accountGroup: mdiAccountGroup,
    lambda: mdiLambda,
    formatListChecks: mdiFormatListChecks,
    cogs: mdiCogs,
  };

  currentSubpageIndex = 0;
  miniNavigation = false;

  mounted() {
    this.moveOverview();
  }

  moveOverview() {
    this.moveTo(this.paths.mainConfigAdminOverview);
  }

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickOverview() {
    this.moveOverview();
  }

  onClickUsers() {
    this.moveTo(this.paths.mainConfigAdminUsers);
  }

  onClickGroups() {
    this.moveTo(this.paths.mainConfigAdminGroups);
  }

  onClickLambdas() {
    this.moveTo(this.paths.mainConfigAdminLambdas);
  }

  onClickFeatures() {
    this.moveTo(this.paths.mainConfigAdminFeatures);
  }

  onClickSettings() {
    this.moveTo(this.paths.mainConfigAdminSettings);
  }
}
</script>
