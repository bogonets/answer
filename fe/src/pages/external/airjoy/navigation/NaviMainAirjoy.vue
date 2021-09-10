<i18n lang="yaml">
en:
  summary: "Summary"
  table: "Table"
  live: "Live"
  chart: "Chart"
  members: "Members"
  settings: "Settings"

ko:
  summary: "요약"
  table: "테이블"
  live: "실시간"
  chart: "차트"
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
          :value="value"
          @change="input"
      >

        <v-list-item link @click.stop="airjoySummary">
          <v-list-item-icon>
            <v-icon>mdi-weather-windy</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('summary') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="airjoyLive">
          <v-list-item-icon>
            <v-icon>mdi-monitor-dashboard</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('live') }}
          </v-list-item-title>
        </v-list-item>

        <v-list-item link @click.stop="airjoyTable">
          <v-list-item-icon>
            <v-icon>mdi-table</v-icon>
          </v-list-item-icon>
          <v-list-item-title>
            {{ $t('table') }}
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
import {UserA} from '@/packet/user';
import {ProjectA} from '@/packet/project';

@Component
export default class NaviMainAirjoy extends VueBase {

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
  project = {} as ProjectA;
  user = {} as UserA;

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
      this.user = await this.$api2.getSelf();
      this.project = await this.$api2.getMainProjectsPgroupPproject(
          this.$route.params.group,
          this.$route.params.project,
      );
    } catch (error) {
      this.toastRequestFailure(error);
      this.moveToBack();
    }
  }

  onClickFoldNavigation() {
    this.mini = !this.mini;
  }

  @Emit()
  input(index: number) {
    return index;
  }

  @Emit('click:airjoy-summary')
  airjoySummary() {
    if (!this.noDefault) {
      this.moveToMainAirjoySummary();
    }
  }

  @Emit('click:airjoy-live')
  airjoyLive() {
    if (!this.noDefault) {
      this.moveToMainAirjoyLive();
    }
  }

  @Emit('click:airjoy-table')
  airjoyTable() {
    if (!this.noDefault) {
      this.moveToMainAirjoyTable();
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
