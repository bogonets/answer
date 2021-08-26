<i18n lang="yaml">
en:
  dashboard: "Dashboard"
  layouts: "Layouts"
  files: "Files"
  tables: "Tables"
  tasks: "Tasks"
  vp: "Visual Programming"
  vms: "VMS"
  members: "Members"
  settings: "Settings"
  airjoy:
    tables: "Airjoy Tables"
    statistics: "Airjoy Statistics"
    monitoring: "Airjoy Monitoring"
    users: "Airjoy Users"

ko:
  dashboard: "대시보드"
  layouts: "레이아웃"
  files: "파일"
  tables: "테이블"
  tasks: "태스크"
  vp: "시각 프로그래밍"
  vms: "VMS"
  members: "회원 관리"
  settings: "프로젝트 설정"
  airjoy:
    tables: "에어조이 테이블"
    statistics: "에어조이 통계"
    monitoring: "에어조이 모니터링"
    users: "에어조이 사용자 관리"
</i18n>

<template>
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
          <v-avatar color="accent" size="24">{{ projectAvatar }}</v-avatar>
        </v-list-item-icon>
        <v-list-item-title>
          {{ projectSlug }}
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

        <v-list-item link @click.stop="dashboard">
          <v-list-item-icon>
            <v-icon>mdi-gauge</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('dashboard') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="layouts">
          <v-list-item-icon>
            <v-icon>mdi-view-dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('layouts') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="files">
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('files') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="tables">
          <v-list-item-icon>
            <v-icon>mdi-table-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('tables') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="tasks">
          <v-list-item-icon>
            <v-icon>mdi-format-list-checks</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('tasks') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="visualProgramming">
          <v-list-item-icon>
            <v-icon>mdi-lambda</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('vp') }}
          </v-list-item-title>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item link @click.stop="vms">
          <v-list-item-icon>
            <v-icon>mdi-cctv</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('vms') }}
          </v-list-item-title>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item link @click.stop="airjoyTables">
          <v-list-item-icon>
            <v-icon dense>fa-wind</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('airjoy.tables') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="airjoyStatistics">
          <v-list-item-icon>
            <v-icon dense>fa-chart-bar</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('airjoy.statistics') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="airjoyMonitoring">
          <v-list-item-icon>
            <v-icon dense>fa-border-all</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('airjoy.monitoring') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="airjoyUsers">
          <v-list-item-icon>
            <v-icon dense>fa-users-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('airjoy.users') }}
          </v-list-item-title>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item link @click.stop="members">
          <v-list-item-icon>
            <v-icon>mdi-account-group</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('members') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="settings">
          <v-list-item-icon>
            <v-icon>mdi-cog-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('settings') }}
          </v-list-item-title>
        </v-list-item>

      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang='ts'>
import {Component, Emit, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class NaviMain extends VueBase {

  @Prop({type: Boolean, default: false})
  readonly noDefault!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideMembers!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideSettings!: boolean;

  @Prop({type: Number, default: 0})
  readonly value!: number;

  index = 0;
  mini = false;

  get projectSlug(): string {
    const name = this.$route.params.project;
    if (name) {
      return name;
    }
    return this.$t('project.unknown').toString();
  }

  get projectAvatar(): string {
    const name = this.$route.params.project;
    if (name) {
      return name[0].toUpperCase();
    }
    return '?';
  }

  /**
   * @deprecated
   */
  private legacyMounted() {
    this.$store.commit('drawer/setNaviShow', {bool: true});
    this.$store.commit('project/setSelectProject', {name: this.$route.params.project});
    this.$store.commit('project/setViewNaviList', {menus: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]});
    this.$store.commit('signal/setLayoutMainSignal', {bool: true});
  }

  /**
   * @deprecated
   */
  private legacyBeforeDestroy() {
    this.$store.commit('drawer/setNaviShow', {bool: false});
    this.$store.commit('project/setViewNaviList', {menus: null});
  }

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  @Emit()
  input(index: number) {
    return index;
  }

  @Emit('click:dashboard')
  dashboard() {
    if (!this.noDefault) {
      this.moveToMainDashboard();
    }
  }

  @Emit('click:layouts')
  layouts() {
    if (!this.noDefault) {
      // this.moveToMainProjectLayouts();
    }
  }

  @Emit('click:files')
  files() {
    if (!this.noDefault) {
      // this.moveToMainProjectFiles();
    }
  }

  @Emit('click:tables')
  tables() {
    if (!this.noDefault) {
      // this.moveToMainProjectTables();
    }
  }

  @Emit('click:tasks')
  tasks() {
    if (!this.noDefault) {
      // this.moveToMainProjectTasks();
    }
  }

  @Emit('click:visual-programming')
  visualProgramming() {
    if (!this.noDefault) {
      // this.moveToMainProjectVisualProgramming();
    }
  }

  @Emit('click:vms')
  vms() {
    if (!this.noDefault) {
      this.moveToMainVms();
    }
  }

  @Emit('click:members')
  members() {
    if (!this.noDefault) {
    }
  }

  @Emit('click:settings')
  settings() {
    if (!this.noDefault) {
      // this.moveToMainProjectConfigs();
    }
  }

  // -----------------
  // Extension: AirJoy
  // -----------------

  @Emit('click:airjoy-tables')
  airjoyTables() {
    if (!this.noDefault) {
      // this.moveToMainProjectAirjoyTables();
    }
  }

  @Emit('click:airjoy-statistics')
  airjoyStatistics() {
    if (!this.noDefault) {
      // this.moveToMainProjectAirjoyStatistics();
    }
  }

  @Emit('click:airjoy-monitoring')
  airjoyMonitoring() {
    if (!this.noDefault) {
      // this.moveToMainProjectAirjoyMonitoring();
    }
  }

  @Emit('click:airjoy-users')
  airjoyUsers() {
    if (!this.noDefault) {
      // this.moveToMainProjectMembers();
    }
  }
}
</script>
