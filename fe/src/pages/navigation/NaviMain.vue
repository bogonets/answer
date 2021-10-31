<i18n lang="yaml">
en:
  dashboard: "Dashboard"
  layouts: "Layouts"
  files: "Files"
  tables: "Tables"
  tasks: "Tasks"
  vp: "Visual Programming"
  vms:
    live: "Live"
    devices: "Devices"
    layouts: "Layouts"
    evnets_calendar: "Events Calendar"
    evnets_filter: "Events Filter"
    user_configs: "User Configs"
  members: "Members"
  settings: "Settings"

ko:
  dashboard: "대시보드"
  layouts: "레이아웃"
  files: "파일"
  tables: "테이블"
  tasks: "태스크"
  vp: "시각 프로그래밍"
  vms:
    live: "실시간"
    devices: "장치 목록"
    layouts: "레이아웃"
    evnets_calendar: "이벤트 달력"
    evnets_filter: "이벤트 필터"
    user_configs: "개인 설정"
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

        <div v-show="isVms">
          <v-divider></v-divider>

          <v-list-item v-show="hasManagerRead" link @click.stop="vmsLive">
            <v-list-item-icon>
              <v-icon>mdi-broadcast</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('vms.live') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-show="hasManagerRead" link @click.stop="vmsDevices">
            <v-list-item-icon>
              <v-icon>mdi-cctv</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('vms.devices') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-show="hasManagerRead" link @click.stop="vmsLayouts">
            <v-list-item-icon>
              <v-icon>mdi-view-dashboard</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('vms.layouts') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-show="hasManagerRead" link @click.stop="vmsEventsCalendar">
            <v-list-item-icon>
              <v-icon>mdi-calendar</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('vms.evnets_calendar') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-show="hasManagerRead" link @click.stop="vmsEventsFilter">
            <v-list-item-icon>
              <v-icon>mdi-filter</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('vms.evnets_filter') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-show="hasManagerRead" link @click.stop="vmsUserConfigs">
            <v-list-item-icon>
              <v-icon>mdi-camera-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('vms.user_configs') }}
            </v-list-item-title>
          </v-list-item>
        </div>

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
import type {RawPermission} from '@/packet/permission';
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
  permission = {} as RawPermission;

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

  get hasManagerRead() {
    return this.permission?.r_manager || false;
  }

  created() {
    (async () => {
      await this.requestSetup();
    })();
  }

  mounted() {
    this.legacyMounted();
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
    } else if (name === mainNames.mainVisualProgramming) {
      this.index = 5;

    } else if (name === mainNames.mainVmsLive) {
      this.index = 6;
    } else if (name === mainNames.mainVmsDevices) {
      this.index = 7;
    } else if (name === mainNames.mainVmsDevicesDiscovery) {
      this.index = 7;
    } else if (name === mainNames.mainVmsDevicesEdit) {
      this.index = 7;
    } else if (name === mainNames.mainVmsDevicesNew) {
      this.index = 7;
    } else if (name === mainNames.mainVmsLayouts) {
      this.index = 8;
    } else if (name === mainNames.mainVmsLayoutsEdit) {
      this.index = 8;
    } else if (name === mainNames.mainVmsLayoutsNew) {
      this.index = 8;
    } else if (name === mainNames.mainVmsEventsCalendar) {
      this.index = 9;
    } else if (name === mainNames.mainVmsEventsFilter) {
      this.index = 10;

    } else if (name === mainNames.mainMembers) {
      this.index = 11;
    } else if (name === mainNames.mainSettings) {
      this.index = 12;

    } else {
      this.index = -1;
    }
  }

  /**
   * @deprecated
   */
  private legacyMounted() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const projectName = `${group}@${project}`;
    this.$store.commit('drawer/setNaviShow', {bool: true});
    this.$store.commit('project/setSelectProject', {name: projectName});
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
      this.moveToMainTasks();
    }
  }

  @Emit('click:visual-programming')
  visualProgramming() {
    if (!this.noDefault) {
      this.moveToMainVisualProgramming();
    }
  }

  @Emit('click:vms-live')
  vmsLive() {
    if (!this.noDefault) {
      this.moveToMainVmsLive();
    }
  }

  @Emit('click:vms-devices')
  vmsDevices() {
    if (!this.noDefault) {
      this.moveToMainVmsDevices();
    }
  }

  @Emit('click:vms-layouts')
  vmsLayouts() {
    if (!this.noDefault) {
      this.moveToMainVmsLayouts();
    }
  }

  @Emit('click:vms-events-calendar')
  vmsEventsCalendar() {
    if (!this.noDefault) {
      this.moveToMainVmsEventsCalendar();
    }
  }

  @Emit('click:vms-events-filter')
  vmsEventsFilter() {
    if (!this.noDefault) {
      this.moveToMainVmsEventsFilter();
    }
  }

  @Emit('click:vms-user-configs')
  vmsUserConfigs() {
    if (!this.noDefault) {
      this.moveToMainVmsUserConfigs();
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
