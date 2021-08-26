<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

<!--    <form-project-edit-->
<!--        :value="group"-->
<!--        :loading-submit="loadingSubmit"-->
<!--        :loading-delete="loadingDelete"-->
<!--        :show-delete-dialog="showDeleteDialog"-->
<!--        @ok="onClickOk"-->
<!--        @delete:show="onClickDelete"-->
<!--        @delete:cancel="onClickDeleteCancel"-->
<!--        @delete:ok="onClickDeleteOk"-->
<!--    ></form-project-edit>-->

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import {ProjectA, UpdateProjectQ} from '@/packet/project';

@Component({
  components: {
    ToolbarNavigation,
  }
})
export default class GroupSettings extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToRootGroups(),
    },
    {
      text: 'Settings',
      disabled: true,
    },
  ];
}
</script>
