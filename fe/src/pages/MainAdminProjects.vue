<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <table-projects
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
import {ProjectA} from '@/packet/project';
import TableProjects from '@/components/TableProjects.vue';

@Component({
  components: {
    ToolbarNavigation,
    TableProjects,
  }
})
export default class MainAdminProjects extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Projects',
      disabled: true,
    },
  ];

  onClickNew() {
    this.moveToMainAdminProjectsNew();
  }

  onClickEdit(item: ProjectA) {
    this.moveToMainAdminProjectsEdit(item.group_slug, item.project_slug);
  }

  onClickMove(item: ProjectA) {
  }
}
</script>
