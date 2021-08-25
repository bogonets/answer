<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <table-groups
        :loading="loading"
        :items="items"
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
export default class AdminGroups extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
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
    this.$api2.getAdminGroups()
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
    this.moveToAdminGroupsNew();
  }

  onClickEdit(item: GroupA) {
    this.moveToAdminGroupsEdit(item.slug);
  }

  onClickMove(item: GroupA) {
  }
}
</script>
