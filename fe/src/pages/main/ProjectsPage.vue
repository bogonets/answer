<i18n lang="yaml">
en:
  title: "Project Management"
  subtitle: "You can add, edit and remove projects."
  search_label: "You can filter by project name or description"
  new_project: "New Project"
  headers:
    name: "Project"
    description: "Description"
    features: "Features"
    created_at: "Created at"
    updated_at: "Updated at"
  loading: "Loading... Please wait"
  empty_project: "Empty Project"

ko:
  title: "프로젝트 관리"
  subtitle: "프로젝트를 추가하거나 편집 및 제거할 수 있습니다."
  search_label: "프로젝트명 또는 상세정보를 필터링할 수 있습니다."
  new_project: "새로운 프로젝트"
  headers:
    name: "프로젝트명"
    description: "상세"
    features: "기능"
    created_at: "생성일"
    updated_at: "갱신일"
  loading: "불러오는중 입니다... 잠시만 기다려 주세요."
  empty_project: "프로젝트가 존재하지 않습니다."
</i18n>

<template>
  <a-project-table v-if="enableLegacy"></a-project-table>
  <v-container v-else>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-data-table
        :headers="headers"
        :items="users"
        :search="filterText"
        :loading="showLoading"
        :loading-text="$t('loading')"
        @click:row="onClickRow"
    >

      <template v-slot:top>
        <v-toolbar flat>

          <v-text-field
              class="mr-4"
              v-model="filterText"
              append-icon="mdi-magnify"
              single-line
              hide-details
              :label="$t('search_label')"
          ></v-text-field>

          <v-btn color="primary" @click="onClickNewProject">
            {{ $t('new_project') }}
          </v-btn>

        </v-toolbar>
      </template>

      <template v-slot:item.created_at="{ item }">
        {{ utcToDate(item.created_at) }}
      </template>

      <template v-slot:item.updated_at="{ item }">
        {{ utcToDate(item.updated_at) }}
      </template>

      <template v-slot:no-data>
        {{ $t('empty_project') }}
      </template>

    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import aProjectTable from '@/components/Table/aProjectTable.vue';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

const ANONYMOUS_GROUP = '-';

@Component({
  components: {
    ToolbarNavigation,
    aProjectTable,
  }
})
export default class ProjectsPage extends VueBase {

  readonly enableLegacy = false;

  navigationItems: object = [];
  filterText = "";
  headers: object = [];
  users: object = [];
  showLoading = true;

  created() {
    this.navigationItems = [
      {
        text: 'Projects',
        disabled: true,
      },
    ];
    this.headers = [
      {
        text: this.$t('headers.name').toString(),
        align: 'start',
        filterable: true,
        value: 'name',
      },
      {
        text: this.$t('headers.description').toString(),
        align: 'center',
        filterable: true,
        value: 'description',
      },
      {
        text: this.$t('headers.features').toString(),
        align: 'end',
        filterable: false,
        value: 'features',
      },
      {
        text: this.$t('headers.created_at').toString(),
        align: 'end',
        filterable: false,
        value: 'created_at',
      },
      {
        text: this.$t('headers.updated_at').toString(),
        align: 'end',
        filterable: false,
        value: 'updated_at',
      },
    ]
  }

  mounted() {
    this.$api2.getProjects()
        .then(response => {
          console.info(response);
          this.users = response;
          this.showLoading = false;
        })
        .catch(error => {
          console.error(error);
          this.showLoading = false;
        });
  }

  utcToDate(utc: undefined | string): string {
    // Note: Parsing of strings with `Date.parse` is strongly discouraged due to browser
    // differences and inconsistencies.
    if (utc === undefined) {
      return '';
    }

    // Example: 2021-07-24T08:24:29.315870
    return utc.split('T')[0];
  }

  onClickRow(item) {
    // Legacy code:
    this.$store.commit("project/setSelectProject", { name: item.name });
    this.moveToMainProject(ANONYMOUS_GROUP, item.name);
  }

  onClickNewProject() {
    this.moveToMainProjectsNew();
  }
}
</script>
