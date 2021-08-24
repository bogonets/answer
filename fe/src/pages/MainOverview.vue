<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

      <table-groups
          request-type="self"
          hide-new-item-button
          hide-action-edit
          hide-action-move
          clickable-row
          @click:new="onClickNew"
          @click:row="onClickRow"
          @click:edit="onClickEdit"
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
  }
})
export default class MainOverview extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Overview',
      disabled: true,
    },
  ];

  onClickNew() {
  }

  onClickRow(item: GroupA) {
  }

  onClickEdit(item: GroupA) {
  }
}
</script>
