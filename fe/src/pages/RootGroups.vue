<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

      <table-groups
          hide-action-edit
          hide-action-move
          clickable-row
          :loading="loading"
          :items="items"
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
  }
})
export default class RootGroups extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: true,
    },
  ];

  loading = false;
  items = [] as Array<GroupA>;

  created() {
    this.requestGroups()
  }

  requestGroups() {
    this.loading = true;
    this.$api2.getMainGroups()
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
    this.moveToRootGroupsNew();
  }

  onClickRow(item: GroupA) {
    console.info(`onClickRow(${item.slug})`);
    this.moveToGroup(item.slug);
  }
}
</script>
