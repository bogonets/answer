<i18n lang="yaml">
en:
  dashboard: 'Dashboard'
  layouts: 'Layout: {0}'
  tables: 'Tables: {0}'
  tasks: 'Tasks: {0}'
  members: 'Members: {0}'

ko:
  dashboard: '대시보드'
  layouts: '레이아웃: {0}'
  tables: '테이블: {0}'
  tasks: '태스크: {0}'
  members: '회원: {0}'
</i18n>

<template>
  <v-container>
    <breadcrumb-main name="Dashboard"></breadcrumb-main>
    <v-divider></v-divider>

    <v-toolbar flat>
      <span class="text--secondary text-h6 font-weight-bold">
        {{ $t('dashboard') }}
      </span>
      <v-spacer></v-spacer>
      <v-chip class="ml-2" small outlined color="primary">
        <v-icon left>mdi-identifier</v-icon>
        {{ groupSlug }}
        <v-icon>mdi-slash-forward</v-icon>
        {{ projectSlug }}
      </v-chip>
    </v-toolbar>
    <v-divider></v-divider>

    <v-row class="mt-2">
      <v-col v-if="false" v-show="hasPermissionLayoutView()" cols="6" sm="3">
        <card-button @click="onClickLayouts">
          <v-icon large>mdi-view-dashboard</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap">
            {{ $t('layouts', [item.layouts || 0]) }}
          </span>
        </card-button>
      </v-col>

      <v-col v-if="false" v-show="hasPermissionTableView()" cols="6" sm="3">
        <card-button @click="onClickTables">
          <v-icon large>mdi-table-multiple</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap">
            {{ $t('tables', [item.tables || 0]) }}
          </span>
        </card-button>
      </v-col>

      <v-col v-if="false" v-show="hasPermissionTaskView()" cols="6" sm="3">
        <card-button @click="onClickTasks">
          <v-icon large>mdi-format-list-checks</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap">
            {{ $t('tasks', [item.tasks || 0]) }}
          </span>
        </card-button>
      </v-col>

      <v-col v-if="false" v-show="hasPermissionMemberView()" cols="6" sm="3">
        <card-button @click="onClickMembers">
          <v-icon large>mdi-account-group</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap">
            {{ $t('members', [item.members || 0]) }}
          </span>
        </card-button>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import CardButton from '@/components/CardButton.vue';
import type {ProjectOverviewA} from '@/packet/project';

@Component({
  components: {
    BreadcrumbMain,
    CardButton,
  },
})
export default class MainDashboard extends VueBase {
  loading = false;
  item = {} as ProjectOverviewA;

  get groupSlug() {
    return this.$route.params.group;
  }

  get projectSlug() {
    return this.$route.params.project;
  }

  created() {
    this.updateOverview();
  }

  updateOverview() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    this.loading = true;
    this.$api2
      .getMainProjectsPgroupPprojectOverview(group, project)
      .then(item => {
        this.loading = false;
        this.item = item;
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  onClickLayouts() {
    this.moveToMainLayouts();
  }

  onClickTables() {
    this.moveToMainTables();
  }

  onClickTasks() {}

  onClickMembers() {
    this.moveToMainMembers();
  }
}
</script>
