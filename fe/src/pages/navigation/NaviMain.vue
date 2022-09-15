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

      <v-list-item-group
        mandatory
        color="primary"
        :value="index"
        @change="onChangeMenuIndex"
      >
        <div>
          <v-divider></v-divider>

          <v-list-item link @click.stop="onClickDashboard">
            <v-list-item-icon>
              <v-icon>mdi-gauge</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('dashboard') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item :v-show="showKanban" link @click.stop="onClickKanban">
            <v-list-item-icon>
              <v-icon>mdi-view-week-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('kanban') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item :v-show="showLayouts" link @click.stop="onClickLayouts">
            <v-list-item-icon>
              <v-icon>mdi-view-dashboard</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('layouts') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item :v-show="showFiles" link @click.stop="onClickFiles">
            <v-list-item-icon>
              <v-icon>mdi-folder</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('files') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item :v-show="showTables" link @click.stop="onClickTables">
            <v-list-item-icon>
              <v-icon>mdi-table-multiple</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('tables') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-show="showTasks" link @click.stop="onClickTasks">
            <v-list-item-icon>
              <v-icon>mdi-format-list-checks</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('tasks') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-show="showVp" link @click.stop="onClickVisualProgramming">
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
            @click.stop="onClickPluginMenu(plugin.name, menu)"
          >
            <v-list-item-icon v-if="menu.icon">
              <v-icon>{{ menu.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ pluginMenuTitle(menu) }}
            </v-list-item-title>
          </v-list-item>
        </div>

        <div v-show="true">
          <v-divider></v-divider>

          <v-list-item link @click.stop="onClickDatasets">
            <v-list-item-icon>
              <v-icon>mdi-inbox-multiple</v-icon>
            </v-list-item-icon>
            <v-list-item-title>데이터셋</v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickLabel">
            <v-list-item-icon>
              <v-icon>mdi-vector-polyline</v-icon>
            </v-list-item-icon>
            <v-list-item-title>라벨링</v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickCategory">
            <v-list-item-icon>
              <v-icon>mdi-label-multiple</v-icon>
            </v-list-item-icon>
            <v-list-item-title>범주</v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickInstructions">
            <v-list-item-icon>
              <v-icon>mdi-alert-circle</v-icon>
            </v-list-item-icon>
            <v-list-item-title>지침서</v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickMachineLearning">
            <v-list-item-icon>
              <v-icon>mdi-brain</v-icon>
            </v-list-item-icon>
            <v-list-item-title>머신러닝</v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickStorage">
            <v-list-item-icon>
              <v-icon>mdi-database</v-icon>
            </v-list-item-icon>
            <v-list-item-title>저장소</v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickHooks">
            <v-list-item-icon>
              <v-icon>mdi-hook</v-icon>
            </v-list-item-icon>
            <v-list-item-title>웹훅</v-list-item-title>
          </v-list-item>

          <v-list-item link @click.stop="onClickToolSettings">
            <v-list-item-icon>
              <v-icon>mdi-toolbox</v-icon>
            </v-list-item-icon>
            <v-list-item-title>도구설정</v-list-item-title>
          </v-list-item>
        </div>

        <div v-if="showMembers || showSettings">
          <v-divider></v-divider>

          <v-list-item v-if="showMembers" link @click.stop="onClickMembers">
            <v-list-item-icon>
              <v-icon>mdi-account-group</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('members') }}
            </v-list-item-title>
          </v-list-item>

          <v-list-item v-if="showSettings" link @click.stop="onClickSettings">
            <v-list-item-icon>
              <v-icon>mdi-cog-outline</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('settings') }}
            </v-list-item-title>
          </v-list-item>
        </div>
      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import {Component, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import type {PluginA, PluginMenuA, PluginMenusA} from '@recc/api/dist/packet/plugin';
import {
  PERM_SLUG_RECC_DOMAIN_FILE_VIEW,
  PERM_SLUG_RECC_DOMAIN_LAYOUT_VIEW,
  PERM_SLUG_RECC_DOMAIN_TABLE_VIEW,
  PERM_SLUG_RECC_DOMAIN_TASK_VIEW,
  PERM_SLUG_RECC_DOMAIN_VP_VIEW,
  PERM_SLUG_RECC_DOMAIN_MEMBER_VIEW,
  PERM_SLUG_RECC_DOMAIN_SETTING_VIEW,
} from '@recc/api/dist/packet/permission';
import mainNames from '@/router/names/main';

function visiblePluginMenus(plugin: PluginA, permissions: Array<string>) {
  const result = [] as Array<PluginMenuA>;
  for (const menu of plugin.menus.project) {
    if (!menu.permission || permissions.includes(menu.permission)) {
      result.push(menu);
    }
  }
  return result;
}

function anyPluginMenu(plugin: PluginA, permissions: Array<string>): boolean {
  if (plugin.menus.project.length == 0) {
    return false;
  }
  for (const menu of plugin.menus.project) {
    if (!menu.permission) {
      continue;
    }
    if (!permissions.includes(menu.permission)) {
      return false;
    }
  }
  return true;
}

function findAvailablePlugins(plugins: Array<PluginA>, permissions: Array<string>) {
  const result = [] as Array<PluginA>;
  for (const plugin of plugins) {
    if (anyPluginMenu(plugin, permissions)) {
      result.push({
        name: plugin.name,
        menus: {
          admin: [],
          group: [],
          project: visiblePluginMenus(plugin, permissions),
          user: [],
        } as PluginMenusA,
      } as PluginA);
    }
  }
  return result;
}

function findMenuIndex(pluginName: string, menuName: string, plugins: Array<PluginA>) {
  let result = 0;
  for (const plugin of plugins) {
    if (pluginName !== plugin.name) {
      result += plugin.menus.project.length;
      continue;
    }

    for (const menu of plugin.menus.project) {
      if (menuName !== menu.name) {
        result++;
        continue;
      }

      return result;
    }
  }

  return -1;
}

@Component
export default class NaviMain extends VueBase {
  index = 0;
  mini = false;
  permissions = [] as Array<string>;
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

  private hasPermission(perm: string) {
    return this.permissions.includes(perm);
  }

  get showKanban() {
    return true;
  }

  get showLayouts() {
    return this.hasPermission(PERM_SLUG_RECC_DOMAIN_LAYOUT_VIEW);
  }

  get showFiles() {
    return this.hasPermission(PERM_SLUG_RECC_DOMAIN_FILE_VIEW);
  }

  get showTables() {
    return this.hasPermission(PERM_SLUG_RECC_DOMAIN_TABLE_VIEW);
  }

  get showTasks() {
    return this.hasPermission(PERM_SLUG_RECC_DOMAIN_TASK_VIEW);
  }

  get showVp() {
    return this.hasPermission(PERM_SLUG_RECC_DOMAIN_VP_VIEW);
  }

  get showMembers() {
    return this.hasPermission(PERM_SLUG_RECC_DOMAIN_MEMBER_VIEW);
  }

  get showSettings() {
    return this.hasPermission(PERM_SLUG_RECC_DOMAIN_SETTING_VIEW);
  }

  get pluginsMenusLength() {
    return this.plugins.map(x => x.menus.project.length).reduce((x, y) => x + y);
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
      this.permissions = await this.$api2.getSelfPermissionsPgroupPproject(
        group,
        project,
      );
      const plugins = this.$localStore.preference.plugins;
      this.plugins = findAvailablePlugins(plugins, this.permissions);
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
    } else if (name === mainNames.mainDatasets) {
      this.index = 7;
    } else if (name === mainNames.mainLabel) {
      this.index = 8;
    } else if (name === mainNames.mainCategory) {
      this.index = 9;
    } else if (name === mainNames.mainInstructions) {
      this.index = 10;
    } else if (name === mainNames.mainMachineLearning) {
      this.index = 11;
    } else if (name === mainNames.mainStorage) {
      this.index = 12;
    } else if (name === mainNames.mainHooks) {
      this.index = 13;
    } else if (name === mainNames.mainToolSettings) {
      this.index = 14;
    } else if (name === mainNames.mainPlugin) {
      const plugin = this.$router.currentRoute.params.plugin;
      const menu = this.$router.currentRoute.params.menu;
      this.index = 14 + findMenuIndex(plugin, menu, this.plugins) + 1;
    } else if (name === mainNames.mainMembers) {
      this.index = 14 + this.pluginsMenusLength + 10;
    } else if (name === mainNames.mainSettings) {
      this.index = 14 + this.pluginsMenusLength + 11;
    } else {
      this.index = -1;
    }
  }

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  onChangeMenuIndex(index: number) {
    this.index = index;
  }

  onClickDashboard() {
    this.moveToMainDashboard();
  }

  onClickKanban() {
    this.moveToMainKanban();
  }

  onClickLayouts() {
    this.moveToMainLayouts();
  }

  onClickFiles() {
    this.moveToMainFiles();
  }

  onClickTables() {
    this.moveToMainTables();
  }

  onClickTasks() {
    this.moveToMainTasks();
  }

  onClickVisualProgramming() {
    this.moveToMainVisualProgramming();
  }

  onClickMembers() {
    this.moveToMainMembers();
  }

  onClickSettings() {
    this.moveToMainSettings();
  }

  onClickPluginMenu(plugin: string, menu: PluginMenuA) {
    this.moveToMainPlugin(undefined, undefined, plugin, menu.name, menu.path);
  }

  pluginMenuTitle(menu: PluginMenuA): string {
    const localeName = menu.translations[this.$localStore.lang];
    if (localeName) {
      return localeName;
    } else {
      return menu.name;
    }
  }

  // REMOVE

  onClickDatasets() {
    this.moveToMainDatasets();
  }

  onClickLabel() {
    this.moveToMainLabel();
  }

  onClickCategory() {
    this.moveToMainCategory();
  }

  onClickInstructions() {
    this.moveToMainInstructions();
  }

  onClickMachineLearning() {
    this.moveToMainMachineLearning();
  }

  onClickStorage() {
    this.moveToMainStorage();
  }

  onClickHooks() {
    this.moveToMainHooks();
  }

  onClickToolSettings() {
    this.moveToMainToolSettings();
  }
}
</script>
