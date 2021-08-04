<i18n lang="yaml">
en:
  dashboard: "Dashboard"
  layouts: "Layouts"
  files: "Files"
  tables: "Tables"
  vms: "VMS"
  tasks: "Tasks"
  vp: "Visual Programming"
  airjoy:
    tables: "Airjoy Tables"
    statistics: "Airjoy Statistics"
    monitoring: "Airjoy Monitoring"
    users: "Airjoy Users"
  graph: "Graph"
  settings: "Settings"

ko:
  dashboard: "대시보드"
  layouts: "레이아웃"
  files: "파일"
  tables: "테이블"
  vms: "VMS"
  tasks: "테스크"
  vp: "시각 프로그래밍"
  airjoy:
    tables: "에어조이 테이블"
    statistics: "에어조이 통계"
    monitoring: "에어조이 모니터링"
    users: "에어조이 사용자 관리"
  graph: "그래프"
  settings: "설정"
</i18n>

<template>
  <!-- Avoid using <v-container> to get rid of `max-width` limit on subpages. -->
  <div class="pa-0">
    <adr-navigation v-if="enableLegacyNavigation">
    </adr-navigation>
    <v-navigation-drawer
        v-else
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
            <v-avatar color="accent" size="24">{{ projectAvatar }}</v-avatar>
          </v-list-item-avatar>
          <v-list-item-title>
            {{ project }}
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

          <v-list-item link @click.stop="onClickDashboard">
            <v-list-item-icon>
              <v-icon>mdi-gauge</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('dashboard') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickLayouts">
            <v-list-item-icon>
              <v-icon>mdi-view-dashboard</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('layouts') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickFiles">
            <v-list-item-icon>
              <v-icon>mdi-folder</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('files') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickTables">
            <v-list-item-icon>
              <v-icon>mdi-table-multiple</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('tables') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickTasks">
            <v-list-item-icon>
              <v-icon>mdi-format-list-checks</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('tasks') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickVisualProgramming">
            <v-list-item-icon>
              <v-icon>mdi-lambda</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('vp') }}
            </v-list-item-title>
          </v-list-item>

          <v-divider></v-divider>

          <v-list-item v-if="enableVms" link @click.stop="onClickVms">
            <v-list-item-icon>
              <v-icon>mdi-cctv</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('vms') }}
            </v-list-item-title>
          </v-list-item>

          <v-divider v-if="enableVms"></v-divider>

          <v-list-item v-if="enableAirjoy" link @click.stop="onClickAirjoyTables">
            <v-list-item-icon>
              <v-icon dense>fa-wind</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('airjoy.tables') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-if="enableAirjoy" link @click.stop="onClickAirjoyStatistics">
            <v-list-item-icon>
              <v-icon dense>fa-chart-bar</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('airjoy.statistics') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-if="enableAirjoy" link @click.stop="onClickAirjoyMonitoring">
            <v-list-item-icon>
              <v-icon dense>fa-border-all</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('airjoy.monitoring') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-if="enableAirjoy" link @click.stop="onClickAirjoyUsers">
            <v-list-item-icon>
              <v-icon dense>fa-users-cog</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('airjoy.users') }}
            </v-list-item-title>
          </v-list-item>

          <v-divider v-if="enableAirjoy"></v-divider>

          <v-list-item v-if="enableLegacyGraph" link @click.stop="onClickGraph">
            <v-list-item-icon>
              <v-icon dense>fa-project-diagram</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('graph') }}
            </v-list-item-title>
          </v-list-item>

          <v-divider v-if="enableLegacyGraph"></v-divider>

          <v-list-item link @click.stop="onClickSettings">
            <v-list-item-icon>
              <v-icon>mdi-cogs</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('settings') }}
            </v-list-item-title>
          </v-list-item>

        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <adr-components>
    </adr-components>

    <adlg-add-layout>
    </adlg-add-layout>

    <router-view>
    </router-view>
  </div>
</template>

<script lang='ts'>
import adrNavigation from '@/components/Drawer/adrNavigation.vue';
import adrComponents from '@/components/Drawer/adrComponents.vue';
import adlgAddLayout from '@/components/Dialog/adlgAddLayout.vue';
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component({
  components: {
    adrNavigation,
    adrComponents,
    adlgAddLayout,
  }
})
export default class ProjectPage extends VueBase {

  enableLegacyNavigation = false;
  enableVms = true;
  enableAirjoy = true;
  enableLegacyGraph = true;

  currentSubpageIndex = 0;
  miniNavigation = false;

  get group(): string {
    return this.$route.params.group;
  }

  get project(): string {
    return this.$route.params.project;
  }

  get projectAvatar(): string {
    return this.project[0].toUpperCase();
  }

  mounted() {
    // Legacy code:
    this.$store.commit('drawer/setNaviShow', {bool: true});
    this.$store.commit('project/setSelectProject', {name: this.project});
    this.$store.commit('project/setViewNaviList', {menus: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]});
    this.$store.commit('signal/setLayoutMainSignal', {bool: true});
  }

  beforeDestroy() {
    // Legacy code:
    this.$store.commit('drawer/setNaviShow', {bool: false});
    this.$store.commit('project/setViewNaviList', {menus: null});
  }

  onClickFoldNavigation() {
    this.miniNavigation = !this.miniNavigation;
  }

  onClickGraph() {
    this.moveToMainProjectGraph();
  }

  onClickDashboard() {
    this.moveToMainProjectDashboard();
  }

  onClickLayouts() {
    this.moveToMainProjectLayouts();
  }

  onClickFiles() {
    this.moveToMainProjectFiles();
  }

  onClickTables() {
    this.moveToMainProjectTables();
  }

  onClickVms() {
    this.moveToMainProjectVms();
  }

  onClickTasks() {
    this.moveToMainProjectTasks();
  }

  onClickVisualProgramming() {
    this.moveToMainProjectVp();
  }

  onClickSettings() {
    this.moveToMainProjectSettings();
  }

  onClickAirjoyTables() {
    this.moveToMainProjectAirjoyManage();
  }

  onClickAirjoyStatistics() {
    this.moveToMainProjectAirjoyGraph();
  }

  onClickAirjoyMonitoring() {
    this.moveToMainProjectAirjoyMonitor();
  }

  onClickAirjoyUsers() {
    this.moveToMainProjectAuth();
  }
}
</script>
