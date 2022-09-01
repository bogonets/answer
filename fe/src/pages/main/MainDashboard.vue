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

    <v-row class="mt-4">
      <v-col class="d-flex flex-row justify-center" cols="4">
        <v-progress-circular
          :rotate="360"
          :size="240"
          :width="40"
          :value="80"
          color="teal"
        >
          <div class="d-flex flex-column align-center">
            <span class="text--secondary text-h6">CPU Usage</span>
            <span class="text-h6 font-weight-bold">80%</span>
          </div>
        </v-progress-circular>
      </v-col>

      <v-col class="d-flex flex-row justify-center" cols="4">
        <v-progress-circular
          :rotate="360"
          :size="240"
          :width="40"
          :value="35"
          color="primary"
        >
          <div class="d-flex flex-column align-center">
            <span class="text--secondary text-h6">Memory Usage</span>
            <span class="text-h6 font-weight-bold">35%</span>
          </div>
        </v-progress-circular>
      </v-col>

      <v-col class="d-flex flex-row justify-center" cols="4">
        <v-progress-circular
          :rotate="360"
          :size="240"
          :width="40"
          :value="90"
          color="pink"
        >
          <div class="d-flex flex-column align-center">
            <span class="text--secondary text-h6">Disk Usage</span>
            <span class="text-h6 font-weight-bold">90%</span>
          </div>
        </v-progress-circular>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import CardButton from '@/components/CardButton.vue';
import type {ProjectOverviewA} from '@recc/api/dist/packet/project';

@Component({
  components: {
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
