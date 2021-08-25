<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <table-projects
        hide-action-edit
        hide-action-move
        clickable-row
        request-type="self"
        @click:new="onClickNew"
        @click:row="onClickRow"
    ></table-projects>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import TableProjects from "@/components/TableProjects.vue";
import {ProjectA} from '@/packet/project';

@Component({
  components: {
    ToolbarNavigation,
    TableProjects,
  }
})
export default class MainProjects extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: true,
      href: () => this.moveToMainGroups(),
    },
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
