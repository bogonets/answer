<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-project-new
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
export default class AdminProjectsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToAdminProjects(),
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
    this.$api2.getAdminGroups()
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
    this.$api2.postAdminProjects(event)
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
