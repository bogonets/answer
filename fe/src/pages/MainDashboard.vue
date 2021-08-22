<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <table-groups
        request-type="self"
        hide-action-edit
        hide-action-move
        clickable-row
        @click:new="onClickNew"
        @click:row="onClickRow"
    ></table-groups>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import TableGroups from '@/components/TableGroups.vue';
import {GroupA} from '@/packet/group';

@Component({
  components: {
    ToolbarNavigation,
    TableGroups,
  },
})
export default class MainDashboard extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Dashboard',
      disabled: true,
    },
  ];

  onClickNew() {
    this.moveToMainGroupsNew();
  }

  onClickRow(item: GroupA) {
    const group_slug = item.slug;
  }
}
</script>
