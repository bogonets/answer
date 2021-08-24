<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <table-projects
        request-type="admin"
        @click:new="onClickNew"
        @click:edit="onClickEdit"
        @click:move="onClickMove"
    ></table-projects>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import TableProjects from '@/components/TableProjects.vue';
import {ProjectA} from '@/packet/project';

@Component({
  components: {
    ToolbarNavigation,
    TableProjects,
  }
})
export default class AdminProjects extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdminOverview(),
    },
    {
      text: 'Projects',
      disabled: true,
    },
  ];

  onClickNew() {
    this.moveToAdminProjectsNew();
  }

  onClickEdit(item: ProjectA) {
    this.moveToAdminProjectsEdit(item.group_slug, item.project_slug);
  }

  onClickMove(item: ProjectA) {
  }
}
</script>
