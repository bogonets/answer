<template>
  <a-project-table v-if="enableLegacy"></a-project-table>
  <v-container v-else>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <table-projects
        hide-action-edit
        hide-action-move
        clickable-row
        @click:new="onClickNew"
        @click:row="onClickRow"
    ></table-projects>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import aProjectTable from '@/components/Table/aProjectTable.vue';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import TableProjects from "@/components/TableProjects.vue";
import {ProjectA} from '@/packet/project';

@Component({
  components: {
    aProjectTable,
    ToolbarNavigation,
    TableProjects,
  }
})
export default class MainProjects extends VueBase {
  /**
   * @deprecated
   */
  private readonly enableLegacy = false;

  private readonly navigationItems = [
    {
      text: 'Projects',
      disabled: true,
    },
  ];

  /**
   * @deprecated
   */
  private legacySelectProject(name) {
    this.$store.commit('project/setSelectProject', {name});
  }

  onClickNew() {
    this.moveToMainProjectsNew();
  }

  onClickRow(item: ProjectA) {
    this.legacySelectProject(item.project_slug);
    this.moveToMainProject(item.group_slug, item.project_slug);
  }
}
</script>
