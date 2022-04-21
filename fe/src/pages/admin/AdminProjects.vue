<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <table-projects
      :loading="loading"
      :items="items"
      @click:new="onClickNew"
      @click:edit="onClickEdit"
      @click:move="onClickMove"
    ></table-projects>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import TableProjects from '@/components/TableProjects.vue';
import {ProjectA} from '@/packet/project';

@Component({
  components: {
    ToolbarBreadcrumbs,
    TableProjects,
  },
})
export default class AdminProjects extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
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
    this.loading = true;
    this.$api2
      .getAdminProjects()
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
    this.moveToAdminProjectsNew();
  }

  onClickEdit(item: ProjectA) {
    this.moveToAdminProjectsEdit(item.group_slug, item.project_slug);
  }

  onClickMove(item: ProjectA) {
    this.moveToMain(item.group_slug, item.project_slug);
  }
}
</script>
