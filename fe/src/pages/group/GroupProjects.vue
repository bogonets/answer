<template>
  <v-container>
    <toolbar-breadcrumbs :items="breadcrumbs"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <table-projects
      hide-action-edit
      hide-action-move
      clickable-row
      :loading="loading"
      :items="items"
      @click:new="onClickNew"
      @click:row="onClickRow"
    ></table-projects>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import TableProjects from '@/components/TableProjects.vue';
import {ProjectA} from '@recc/api/dist/packet/project';

@Component({
  components: {
    ToolbarBreadcrumbs,
    TableProjects,
  },
})
export default class GroupProjects extends VueBase {
  readonly breadcrumbs = [
    {
      text: this.$route.params.group,
      disabled: false,
      href: () => this.moveToGroup(),
    },
    {
      text: 'Projects',
      disabled: true,
    },
  ];

  loading = false;
  items = [] as Array<ProjectA>;

  created() {
    this.requestProjects();
  }

  requestProjects() {
    const group = this.$route.params.group;
    this.loading = true;
    this.$api2
      .getMainGroupsPgroupProjects(group)
      .then(items => {
        this.loading = false;
        this.items = items;
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  onClickNew() {
    this.moveToGroupProjectsNew();
  }

  onClickRow(item: ProjectA) {
    this.moveToMain(item.group_slug, item.project_slug);
  }
}
</script>
