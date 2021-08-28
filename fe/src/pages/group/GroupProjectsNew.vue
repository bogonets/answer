<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-project-new
        disable-group
        :init-group="$route.params.group"
        :loading-groups="loadingGroups"
        :loading-submit="loadingSubmit"
        :group-items="groupItems"
        @ok="onClickOk"
    ></form-project-new>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import FormProjectNew from "@/components/FormProjectNew.vue";
import {CreateProjectQ} from "@/packet/project";

@Component({
  components: {
    ToolbarBreadcrumbs,
    FormProjectNew,
  }
})
export default class GroupProjectsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToRootGroups(),
    },
    {
      text: this.$route.params.group,
      disabled: false,
      href: () => this.moveToGroup(),
    },
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToGroupProjects(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];

  loadingGroups = false;
  loadingSubmit = false;
  groupItems = [] as Array<string>;

  created() {
    this.requestGroups();
  }

  requestGroups() {
    this.loadingGroups = true;
    this.$api2.getMainGroups()
        .then(items => {
          this.loadingGroups = false;
          this.groupItems = items.map(x => x.slug);
        })
        .catch(error => {
          this.loadingGroups = false;
          this.moveToBack();
          this.toastRequestFailure(error);
        });
  }

  onClickOk(event: CreateProjectQ) {
    this.loadingSubmit = true;
    this.$api2.postMainProjects(event)
        .then(() => {
          this.loadingSubmit = false;
          this.toastRequestSuccess();
          this.moveToBack();
        })
        .catch(error => {
          this.loadingSubmit = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
