<i18n lang="yaml">
en:
  title: "Admin setting"
  overview: "Overview"
  users: "Users"
  groups: "Groups"
  projects: "Projects"
  permissions: "Permissions"
  containers: "Containers"
  lambdas: "Lambdas"
  configs: "Configs"
  ports: "Ports"
  daemons: "Daemons"
  external:
    airjoy:
      devices: "AIRJOY Devices"

ko:
  title: "관리자 설정"
  overview: "개요"
  users: "사용자"
  groups: "그룹"
  projects: "프로젝트"
  permissions: "권한"
  containers: "컨테이너"
  lambdas: "람다"
  configs: "구성"
  ports: "포트"
  daemons: "데몬"
  external:
    airjoy:
      devices: "AIRJOY 장치 관리"
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
          :value="index"
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

        <v-list-item link @click.stop="containers">
          <v-list-item-icon>
            <v-icon>fa-cubes</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('containers') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="lambdas">
          <v-list-item-icon>
            <v-icon>mdi-lambda</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('lambdas') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="configs">
          <v-list-item-icon>
            <v-icon>mdi-format-list-checks</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('configs') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item v-show="false" link @click.stop="ports">
          <v-list-item-icon>
            <v-icon>mdi-connection</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('ports') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="daemons">
          <v-list-item-icon>
            <v-icon>mdi-ghost</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('daemons') }}
          </v-list-item-title>
        </v-list-item>

        <v-divider v-show="false"></v-divider>
        <v-list-item v-show="false" link @click.stop="externalAirjoyDevices">
          <v-list-item-icon>
            <v-icon>mdi-weather-windy</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('external.airjoy.devices') }}
          </v-list-item-title>
        </v-list-item>

      </v-list-item-group>
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import {Component, Prop, Emit, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import adminNames from '@/router/names/admin';
import devNames from "@/router/names/dev";

@Component
export default class NaviAdmin extends VueBase {

  @Prop({type: Boolean, default: false})
  readonly noDefault!: boolean;

  index = 0;
  mini = false;

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  @Watch('$route')
  onChangeRoute() {
    const name = this.$route.name;
    if (name === adminNames.adminOverview) {
      this.index = 0;
    } else if (name === adminNames.adminUsers) {
      this.index = 1;
    } else if (name === adminNames.adminUsersEdit) {
      this.index = 1;
    } else if (name === adminNames.adminUsersNew) {
      this.index = 1;
    } else if (name === adminNames.adminGroups) {
      this.index = 2;
    } else if (name === adminNames.adminGroupsEdit) {
      this.index = 2;
    } else if (name === adminNames.adminGroupsNew) {
      this.index = 2;
    } else if (name === adminNames.adminProjects) {
      this.index = 3;
    } else if (name === adminNames.adminProjectsEdit) {
      this.index = 3;
    } else if (name === adminNames.adminProjectsNew) {
      this.index = 3;
    } else if (name === adminNames.adminPermissions) {
      this.index = 4;
    } else if (name === adminNames.adminPermissionsEdit) {
      this.index = 4;
    } else if (name === adminNames.adminPermissionsNew) {
      this.index = 4;
    } else if (name === adminNames.adminContainers) {
      this.index = 5;
    } else if (name === adminNames.adminTemplates) {
      this.index = 6;
    } else if (name === adminNames.adminConfigs) {
      this.index = 7;
    } else if (name === adminNames.adminPorts) {
      this.index = 8;
    } else if (name === adminNames.adminDaemons) {
      this.index = 9;
    } else if (name === adminNames.adminDaemonsEdit) {
      this.index = 9;
    } else if (name === adminNames.adminDaemonsNew) {
      this.index = 9;
    } else if (name === adminNames.adminAirjoyDevices) {
      this.index = 10;
    } else {
      this.index = -1;
    }
  }

  @Emit()
  input(index: number) {
    this.index = index;
    return index;
  }

  @Emit('click:overview')
  overview() {
    if (!this.noDefault) {
      this.moveToAdmin();
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

  @Emit('click:containers')
  containers() {
    if (!this.noDefault) {
      this.moveToAdminContainers();
    }
  }

  @Emit('click:lambdas')
  lambdas() {
    if (!this.noDefault) {
      this.moveToAdminTemplates();
    }
  }

  @Emit('click:configs')
  configs() {
    if (!this.noDefault) {
      this.moveToAdminConfigs();
    }
  }

  @Emit('click:ports')
  ports() {
    if (!this.noDefault) {
      this.moveToAdminPorts();
    }
  }

  @Emit('click:daemons')
  daemons() {
    if (!this.noDefault) {
      this.moveToAdminDaemons();
    }
  }

  @Emit('click:external-airjoy-devices')
  externalAirjoyDevices() {
    if (!this.noDefault) {
      this.moveToAdminAirjoyDevices();
    }
  }
}
</script>
