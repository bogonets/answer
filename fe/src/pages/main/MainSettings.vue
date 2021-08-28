<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <form-project-edit
        :value="project"
        :loading-submit="loadingSubmit"
        :loading-delete="loadingDelete"
        :show-delete-dialog="showDeleteDialog"
        @ok="onClickOk"
        @delete:show="onClickDelete"
        @delete:cancel="onClickDeleteCancel"
        @delete:ok="onClickDeleteOk"
    ></form-project-edit>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import FormProjectEdit from '@/components/FormProjectEdit.vue';
import {ProjectA, UpdateProjectQ} from '@/packet/project';

@Component({
  components: {
    ToolbarBreadcrumbs,
    FormProjectEdit,
  }
})
export default class MainSettings extends VueBase {
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
      text: this.$route.params.project,
      disabled: false,
      href: () => this.moveToMain(),
    },
    {
      text: 'Settings',
      disabled: true,
    },
  ];

  project = {} as ProjectA;

  showDeleteDialog = false;
  loadingDelete = false;
  loadingSubmit = false;

  created() {
    this.requestProject();
  }

  requestProject() {
    this.$api2.getMainProjectsPgroupPproject(
        this.$route.params.group,
        this.$route.params.project,
    )
        .then(item => {
          this.project = item;
        })
        .catch(error => {
          this.toastRequestFailure(error);
          this.moveToBack();
        });
  }

  onClickOk(event: UpdateProjectQ) {
    this.loadingSubmit = true;
    this.$api2.patchMainProjectsPgroupPproject(
        this.$route.params.group,
        this.$route.params.project,
        event,
    )
        .then(() => {
          this.loadingSubmit = false;
          this.toastRequestSuccess();
          this.requestProject();
        })
        .catch(error => {
          this.loadingSubmit = false;
          this.toastRequestFailure(error);
        });
  }

  onClickDelete() {
    this.showDeleteDialog = true;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk() {
    this.loadingDelete = true;
    this.$api2.deleteMainProjectsPgroupProject(
        this.$route.params.group,
        this.$route.params.project,
    )
        .then(() => {
          this.loadingDelete = false;
          this.showDeleteDialog = false;
          this.toastRequestSuccess();
          this.moveToGroup();
        })
        .catch(error => {
          this.loadingDelete = false;
          this.showDeleteDialog = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
