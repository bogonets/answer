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
          <v-avatar color="info" size="24">{{ projectAvatar }}</v-avatar>
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
          :value="index"
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

        <v-divider v-show="isVms"></v-divider>
        <v-list-item v-show="isVms" link @click.stop="vms">
          <v-list-item-icon>
            <v-icon>mdi-cctv</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('vms') }}
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
import {Component, Emit, Prop, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import type {ProjectA} from '@/packet/project';
import type {PermissionA} from '@/packet/permission';
import {FEATURE_VMS} from '@/packet/features';
import mainNames from '@/router/names/main';

@Component
export default class NaviMain extends VueBase {

  @Prop({type: Boolean, default: false})
  readonly noDefault!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideMembers!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideSettings!: boolean;

  index = 0;
  mini = false;
  project = {} as ProjectA;
  permission = {} as PermissionA;

  get projectSlug(): string {
    const project = this.$route.params.project;
    if (project) {
      return project;
    }
    return this.$t('project.unknown').toString();
  }

  get projectAvatar(): string {
    const project = this.$route.params.project;
    if (project) {
      return project[0].toUpperCase();
    }
    return '?';
  }

  get features() {
    return this.project?.features || [] as Array<string>;
  }

  get isVms() {
    return this.features.findIndex(i => i == FEATURE_VMS) != -1;
  }

  created() {
    (async () => {
      await this.requestSetup();
    })();
  }

  async requestSetup() {
    try {
      const group = this.$route.params.group;
      const project = this.$route.params.project;
      this.project = await this.$api2.getMainProjectsPgroupPproject(group, project);
      this.permission = await this.requestProjectPermission();
    } catch (error) {
      this.toastRequestFailure(error);
      this.moveToBack();
    }
  }

  @Watch('$route')
  onChangeRoute() {
    const name = this.$route.name;
    if (name === mainNames.mainDashboard) {
      this.index = 0;
    } else if (name === mainNames.mainLayouts) {
      this.index = 1;
    } else if (name === mainNames.mainFiles) {
      this.index = 2;
    } else if (name === mainNames.mainTables) {
      this.index = 3;
    } else if (name === mainNames.mainTasks) {
      this.index = 4;
    } else if (name === mainNames.mainVp) {
      this.index = 5;
    } else if (name === mainNames.mainVms) {
      this.index = 6;
    } else if (name === mainNames.mainMembers) {
      this.index = 7;
    } else if (name === mainNames.mainSettings) {
      this.index = 8;
    } else {
      this.index = -1;
    }
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
    this.index = index;
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
      this.moveToMainLayouts();
    }
  }

  @Emit('click:files')
  files() {
    if (!this.noDefault) {
      this.moveToMainFiles();
    }
  }

  @Emit('click:tables')
  tables() {
    if (!this.noDefault) {
      this.moveToMainTables();
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
      this.moveToMainMembers();
    }
  }

  @Emit('click:settings')
  settings() {
    if (!this.noDefault) {
      this.moveToMainSettings();
    }
  }
}
</script>
