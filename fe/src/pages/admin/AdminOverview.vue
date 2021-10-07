<i18n lang="yaml">
en:
  title: "Overview"
  subtitle: "Prints a summary of the system status."
  users: "Users: {0}"
  groups: "Groups: {0}"
  projects: "Projects: {0}"

ko:
  title: "개요"
  subtitle: "시스템의 상태를 요약하여 출력합니다."
  users: "사용자: {0}"
  groups: "그룹: {0}"
  projects: "프로젝트: {0}"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-row class="mt-2">
      <v-col cols="12">
        <card-button height="60px" @click="onClickClock">
          <div>
            <v-icon left>mdi-clock</v-icon>
            <span class="text--secondary text-subtitle-2 text-no-wrap">
              {{ item.time }}
            </span>
          </div>
        </card-button>
      </v-col>

      <v-col cols="4">
        <card-button @click="onClickUsers">
          <v-icon large>mdi-table-multiple</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap">
            {{ $t('users', [item.users || 0]) }}
          </span>
        </card-button>
      </v-col>

      <v-col cols="4">
        <card-button @click="onClickGroups">
          <v-icon large>mdi-format-list-checks</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap">
            {{ $t('groups', [item.groups || 0]) }}
          </span>
        </card-button>
      </v-col>

      <v-col cols="4">
        <card-button @click="onClickProjects">
          <v-icon large>mdi-account-group</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap">
            {{ $t('projects', [item.projects || 0]) }}
          </span>
        </card-button>
      </v-col>
    </v-row>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import CardButton from '@/components/CardButton.vue';
import type {SystemOverviewA} from "@/packet/system";

@Component({
  components: {
    ToolbarBreadcrumbs,
    CardButton,
  }
})
export default class AdminOverview extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Overview',
      disabled: true,
    },
  ];

  loading = false;
  item = {} as SystemOverviewA;

  created() {
    this.updateOverview();
  }

  updateOverview() {
    this.loading = true;
    this.$api2.getAdminSystemOverview()
        .then(item => {
          this.loading = false;
          this.item = item;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  onClickClock() {
    this.updateOverview();
  }

  onClickUsers() {
    this.moveToAdminUsers();
  }

  onClickGroups() {
    this.moveToAdminGroups();
  }

  onClickProjects() {
    this.moveToAdminProjects();
  }
}
</script>
