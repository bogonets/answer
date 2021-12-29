<i18n lang="yaml">
en:
  devices: "Devices"
  summary: "Summary"
  live: "Live"
  chart: "Chart"
  service: "Service"
  airjoy_settings: "Airjoy Settings"
  members: "Members"
  settings: "Settings"

ko:
  devices: "장치 관리"
  summary: "요약"
  live: "실시간"
  chart: "차트"
  service: "서비스"
  airjoy_settings: "에어조이 설정"
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

        <v-list-item v-if="!hideSummary" link @click.stop="airjoySummary">
          <v-list-item-icon>
            <v-icon>mdi-weather-windy</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('summary') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item v-if="showDevices" link @click.stop="airjoyDevices">
          <v-list-item-icon>
            <v-icon>mdi-tablet</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('devices') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item v-if="showLive" link @click.stop="airjoyLive">
          <v-list-item-icon>
            <v-icon>mdi-monitor-dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('live') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item v-if="showChart" link @click.stop="airjoyChart">
          <v-list-item-icon>
            <v-icon>mdi-chart-bar</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('chart') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item v-if="showService" link @click.stop="airjoyService">
          <v-list-item-icon>
            <v-icon>mdi-wrench</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('service') }}
          </v-list-item-title>
        </v-list-item>

        <v-divider v-if="!hideAirjoySettings"></v-divider>
        <v-list-item v-if="!hideAirjoySettings" link @click.stop="airjoySettings">
          <v-list-item-icon>
            <v-icon>mdi-application-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('airjoy_settings') }}
          </v-list-item-title>
        </v-list-item>

        <v-divider v-if="showMember || showSetting"></v-divider>

        <v-list-item v-if="showMember" link @click.stop="members">
          <v-list-item-icon>
            <v-icon>mdi-account-group</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('members') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item v-if="showSetting" link @click.stop="settings">
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
import mainAirjoyNames from '@/router/names/external/airjoy/main';
import mainNames from '@/router/names/main';

@Component
export default class NaviMainAirjoy extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly noDefault!: boolean;

  @Prop({type: Boolean, default: true})
  readonly hideSummary!: boolean;

  @Prop({type: Boolean, default: true})
  readonly hideAirjoySettings!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideMembers!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideSettings!: boolean;

  index = 0;
  mini = false;
  project = {} as ProjectA;
  permission = {} as Array<string>;

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

  get showDevices() {
    return this.hasPermissionManagerView();
  }

  get showLive() {
    return this.hasPermissionManagerView();
  }

  get showChart() {
    return this.hasPermissionManagerView();
  }

  get showService() {
    return this.hasPermissionManagerView();
  }

  get showMember() {
    return this.hasPermissionMemberView();
  }

  get showSetting() {
    return this.hasPermissionSettingView();
  }

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  @Watch('$route')
  onChangeRoute() {
    const name = this.$route.name;
    if (name === mainAirjoyNames.mainAirjoyDevices) {
      this.index = 0;
    } else if (name === mainAirjoyNames.mainAirjoyDetails) {
      this.index = 0;
    } else if (name === mainAirjoyNames.mainAirjoyLive) {
      this.index = 1;
    } else if (name === mainAirjoyNames.mainAirjoyChart) {
      this.index = 2;
    } else if (name === mainAirjoyNames.mainAirjoyService) {
      this.index = 3;
    } else if (name === mainNames.mainMembers) {
      this.index = 4;
    } else if (name === mainNames.mainSettings) {
      this.index = 5;
    } else if (name === mainAirjoyNames.mainAirjoySettings) {
      this.index = -1;
    } else if (name === mainAirjoyNames.mainAirjoySummary) {
      this.index = -1;
    } else {
      this.index = -1;
    }
  }

  @Emit()
  input(index: number) {
    this.index = index;
    return index;
  }

  @Emit('click:airjoy-summary')
  airjoySummary() {
    if (!this.noDefault) {
      this.moveToMainAirjoySummary();
    }
  }

  @Emit('click:airjoy-devices')
  airjoyDevices() {
    if (!this.noDefault) {
      this.moveToMainAirjoyDevices();
    }
  }

  @Emit('click:airjoy-live')
  airjoyLive() {
    if (!this.noDefault) {
      this.moveToMainAirjoyLive();
    }
  }

  @Emit('click:airjoy-chart')
  airjoyChart() {
    if (!this.noDefault) {
      this.moveToMainAirjoyChart();
    }
  }

  @Emit('click:airjoy-service')
  airjoyService() {
    if (!this.noDefault) {
      this.moveToMainAirjoyService();
    }
  }

  @Emit('click:airjoy-settings')
  airjoySettings() {
    if (!this.noDefault) {
      this.moveToMainAirjoySettings();
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
