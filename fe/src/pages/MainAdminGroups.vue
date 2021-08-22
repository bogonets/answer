<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <table-groups
        request-type="admin"
        @click:new="onClickNew"
        @click:edit="onClickEdit"
        @click:move="onClickMove"
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
export default class MainAdminGroups extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Groups',
      disabled: true,
    },
  ];

  onClickNew() {
    this.moveToMainAdminGroupsNew();
  }

  onClickEdit(item: GroupA) {
    this.moveToMainAdminGroupsEdit(item.slug);
  }

  onClickMove(item: GroupA) {
  }
}
</script>
