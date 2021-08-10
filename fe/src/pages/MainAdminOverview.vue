<i18n lang="yaml">
en:
  title: "Overview"
  subtitle: "Prints a summary of the system status."
  users: "Users"
  groups: "Groups"
  projects: "Projects"

ko:
  title: "개요"
  subtitle: "시스템의 상태를 요약하여 출력합니다."
  users: "사용자"
  groups: "그룹"
  projects: "프로젝트"
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-list flat>
      <v-list-item>
        <v-row>
          <v-col cols="4">
            <v-card flat outlined>
              <v-card-text class="text-h6 text-center">
                {{ $t('users') + `: ${users}` }}
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="4">
            <v-card flat outlined>
              <v-card-text class="text-h6 text-center">
                {{ $t('groups') + `: ${groups}` }}
              </v-card-text>
            </v-card>
          </v-col>

          <v-col cols="4">
            <v-card flat outlined>
              <v-card-text class="text-h6 text-center">
                {{ $t('projects') + `: ${projects}` }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-list-item>
    </v-list>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation
  }
})
export default class MainAdminOverview extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Overview',
      disabled: true,
    },
  ];

  users = 0;
  groups = 0;
  projects = 0;

  created() {
    this.$api2.getSystemOverview()
        .then(response => {
          this.users = response.users || 0;
          this.groups = response.groups || 0;
          this.projects = response.projects || 0;
        })
        .catch(error => {
          console.error(error);
        });
  }
}
</script>
