<i18n lang="yaml">
en:
  dashboard: 'Dashboard'
  kanban: 'Kanban'
  layouts: 'Layouts'
  files: 'Files'
  tables: 'Tables'
  tasks: 'Tasks'
  vp: 'Visual Programming'
  vms:
    live: 'Live'
    devices: 'Devices'
    layouts: 'Layouts'
    events_calendar: 'Events Calendar'
    events_list: 'Events List'
    user_configs: 'User Configs'
  members: 'Members'
  settings: 'Settings'

ko:
  dashboard: '대시보드'
  kanban: '간반보드'
  layouts: '레이아웃'
  files: '파일'
  tables: '테이블'
  tasks: '태스크'
  vp: '시각 프로그래밍'
  vms:
    live: '실시간'
    devices: '장치 목록'
    layouts: '레이아웃'
    events_calendar: '이벤트 달력'
    events_list: '이벤트 목록'
    user_configs: '개인 설정'
  members: '회원 관리'
  settings: '프로젝트 설정'
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

      <v-list-item-group mandatory color="primary" :value="index" @change="input">
        <div>
          <v-divider></v-divider>

          <v-list-item link @click.stop="dashboard">
            <v-list-item-icon>
              <v-icon>mdi-gauge</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('dashboard') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="kanban">
            <v-list-item-icon>
              <v-icon>mdi-view-week-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('kanban') }}
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

          <v-list-item v-show="false" link @click.stop="tasks">
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
        </div>

        <div v-for="plugin in plugins" :key="plugin.name">
          <v-divider></v-divider>

          <v-list-item
            v-for="menu in plugin.menus.project"
            :key="`${plugin.name}-${menu.name}`"
            link
            @click.stop="pluginMenu(plugin.name, menu)"
          >
            <v-list-item-icon v-if="menu.icon">
              <v-icon>{{ menu.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ pluginMenuTitle(menu) }}
            </v-list-item-title>
          </v-list-item>
        </div>

        <v-divider
          v-if="hasPermissionMemberView() || hasPermissionSettingView()"
        ></v-divider>

        <v-list-item v-show="hasPermissionMemberView()" link @click.stop="members">
          <v-list-item-icon>
            <v-icon>mdi-account-group</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('members') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item v-show="hasPermissionSettingView()" link @click.stop="settings">
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

<script lang="ts">
import {Component, Emit, Prop, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import type {ProjectA} from '@recc/api/dist/packet/project';
import type {PluginA, PluginMenuA, PluginMenusA} from '@recc/api/dist/packet/plugin';
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
  permission = {} as Array<string>;
  plugins = [] as Array<PluginA>;

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

  anyPluginMenu(plugin: PluginA): boolean {
    if (plugin.menus.project.length == 0) {
      return false;
    }
    for (const menu of plugin.menus.project) {
      if (!menu.permission) {
        continue;
      }
      if (!this.hasPermission(menu.permission)) {
        return false;
      }
    }
    return true;
  }

  visiblePluginMenus(plugin: PluginA): Array<PluginMenuA> {
    const result = [] as Array<PluginMenuA>;
    for (const menu of plugin.menus.project) {
      if (!menu.permission || this.hasPermission(menu.permission)) {
        result.push(menu);
      }
    }
    return result;
  }

  created() {
    const result = [] as Array<PluginA>;
    for (const plugin of this.$localStore.preference.plugins) {
      if (this.anyPluginMenu(plugin)) {
        result.push({
          name: plugin.name,
          menus: {
            admin: [],
            group: [],
            project: this.visiblePluginMenus(plugin),
            user: [],
          } as PluginMenusA,
        } as PluginA);
      }
    }
    this.plugins = result;

    (async () => {
      await this.requestSetup();
    })();
  }

  get pluginsMenusLength() {
    return this.plugins.map(x => x.menus.project.length).reduce((x, y) => x + y);
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

  findMenuIndex() {
    const currentPluginName = this.$router.currentRoute.params.plugin;
    const currentMenuName = this.$router.currentRoute.params.menu;

    let pluginIndex = 0;
    for (const plugin of this.plugins) {
      if (currentPluginName !== plugin.name) {
        pluginIndex += plugin.menus.project.length;
        continue;
      }

      for (const menu of plugin.menus.project) {
        if (currentMenuName !== menu.name) {
          pluginIndex++;
          continue;
        }

        return pluginIndex;
      }
    }

    return -1;
  }

  @Watch('$route')
  onChangeRoute() {
    const name = this.$route.name;
    if (name === mainNames.mainDashboard) {
      this.index = 0;
    } else if (name === mainNames.mainKanban) {
      this.index = 1;
    } else if (name === mainNames.mainLayouts) {
      this.index = 2;
    } else if (name === mainNames.mainFiles) {
      this.index = 3;
    } else if (name === mainNames.mainTables) {
      this.index = 4;
    } else if (name === mainNames.mainTasks) {
      this.index = 5;
    } else if (name === mainNames.mainVisualProgramming) {
      this.index = 6;
    } else if (name === mainNames.mainPlugin) {
      this.index = 6 + this.findMenuIndex() + 1;
    } else if (name === mainNames.mainMembers) {
      this.index = 6 + this.pluginsMenusLength + 1;
    } else if (name === mainNames.mainSettings) {
      this.index = 6 + this.pluginsMenusLength + 2;
    } else {
      this.index = -1;
    }
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

  @Emit('click:kanban')
  kanban() {
    if (!this.noDefault) {
      this.moveToMainKanban();
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

  @Emit('click:plugin')
  pluginMenu(plugin: string, menu: PluginMenuA) {
    if (!this.noDefault) {
      this.moveToMainPlugin(plugin, menu.name);
    }
    return menu;
  }

  pluginMenuTitle(menu: PluginMenuA): string {
    const localeName = menu.translations[this.$localStore.lang];
    if (localeName) {
      return localeName;
    } else {
      return menu.name;
    }
  }
}
</script>
