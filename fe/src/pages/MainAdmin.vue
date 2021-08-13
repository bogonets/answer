<i18n lang="yaml">
en:
  title: "Admin Preference"
  overview: "Overview"
  users: "Users"
  groups: "Groups"
  projects: "Projects"
  tasks: "Tasks"
  lambdas: "Lambdas"
  features: "Features"
  envs: "System variables"

ko:
  title: "관리자 설정"
  overview: "개요"
  users: "사용자"
  groups: "그룹"
  projects: "프로젝트"
  tasks: "테스크"
  lambdas: "람다 관리"
  features: "기능 설정"
  envs: "시스템 변수"
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
            <v-icon>mdi-cog-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('title') }}
          </v-list-item-title>
          <v-btn icon @click.stop="onClickFoldNavigation">
            <v-icon>mdi-chevron-left</v-icon>
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
              <v-icon>mdi-developer-board</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('overview') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickUsers">
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('users') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickGroups">
            <v-list-item-icon>
              <v-icon>mdi-account-group</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('groups') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickProjects">
            <v-list-item-icon>
              <v-icon>mdi-clipboard-check-multiple</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('projects') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickTasks">
            <v-list-item-icon>
              <v-icon>mdi-monitor-multiple</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('tasks') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickLambdas">
            <v-list-item-icon>
              <v-icon>mdi-lambda</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('lambdas') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickFeatures">
            <v-list-item-icon>
              <v-icon>mdi-format-list-checks</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('features') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickEnvs">
            <v-list-item-icon>
              <v-icon>mdi-cogs</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('envs') }}
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
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class MainAdmin extends VueBase {

  currentSubpageIndex = 0;
  miniNavigation = false;

  moveOverview() {
    this.moveToMainAdminOverview();
  }

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickOverview() {
    this.moveOverview();
  }

  onClickUsers() {
    this.moveToMainAdminUsers();
  }

  onClickGroups() {
    this.moveToMainAdminGroups();
  }

  onClickProjects() {
    this.moveToMainAdminProjects();
  }

  onClickTasks() {
    this.moveToMainAdminTasks();
  }

  onClickLambdas() {
    this.moveToMainAdminLambdas();
  }

  onClickFeatures() {
    this.moveToMainAdminFeatures();
  }

  onClickEnvs() {
    this.moveToMainAdminEnvs();
  }
}
</script>
