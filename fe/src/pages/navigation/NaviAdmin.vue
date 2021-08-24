<i18n lang="yaml">
en:
  title: "Admin Preference"
  overview: "Overview"
  users: "Users"
  groups: "Groups"
  projects: "Projects"
  permissions: "Permissions"
  tasks: "Tasks"
  templates: "Templates"
  features: "Features"
  envs: "System variables"

ko:
  title: "관리자 설정"
  overview: "개요"
  users: "사용자"
  groups: "그룹"
  projects: "프로젝트"
  permissions: "권한"
  tasks: "태스크"
  templates: "템플릿"
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
        :mini-variant.sync="mini"
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
            :value="value"
            @change="input"
        >

          <v-list-item link @click.stop="overview">
            <v-list-item-icon>
              <v-icon>mdi-developer-board</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('overview') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="users">
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('users') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="groups">
            <v-list-item-icon>
              <v-icon>mdi-account-group</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('groups') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="projects">
            <v-list-item-icon>
              <v-icon>mdi-clipboard-check-multiple</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('projects') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="permissions">
            <v-list-item-icon>
              <v-icon>mdi-key-change</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('permissions') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="tasks">
            <v-list-item-icon>
              <v-icon>mdi-monitor-multiple</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('tasks') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="templates">
            <v-list-item-icon>
              <v-icon>mdi-lambda</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('templates') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="features">
            <v-list-item-icon>
              <v-icon>mdi-format-list-checks</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('features') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="envs">
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
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class NaviAdmin extends VueBase {

  @Prop({type: Boolean, default: false})
  readonly noDefault!: boolean;

  @Prop({type: Number, default: 0})
  readonly value!: number;

  mini = false;

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  @Emit()
  input(index: number) {
    return index;
  }

  @Emit('click:overview')
  overview() {
    if (!this.noDefault) {
      this.moveToAdminOverview();
    }
  }

  @Emit('click:users')
  users() {
    if (!this.noDefault) {
      this.moveToAdminUsers();
    }
  }

  @Emit('click:groups')
  groups() {
    if (!this.noDefault) {
      this.moveToAdminGroups();
    }
  }

  @Emit('click:projects')
  projects() {
    if (!this.noDefault) {
      this.moveToAdminProjects();
    }
  }

  @Emit('click:permissions')
  permissions() {
    if (!this.noDefault) {
      this.moveToAdminPermissions();
    }
  }

  @Emit('click:tasks')
  tasks() {
    if (!this.noDefault) {
      this.moveToAdminTasks();
    }
  }

  @Emit('click:templates')
  templates() {
    if (!this.noDefault) {
      this.moveToAdminTemplates();
    }
  }

  @Emit('click:features')
  features() {
    if (!this.noDefault) {
      this.moveToAdminConfigs();
    }
  }

  @Emit('click:envs')
  envs() {
    if (!this.noDefault) {
      this.moveToAdminInfos();
    }
  }
}
</script>
