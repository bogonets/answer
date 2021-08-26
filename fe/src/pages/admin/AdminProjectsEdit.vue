<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
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
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import {ProjectA, UpdateProjectQ} from '@/packet/project';
import FormProjectEdit from "@/components/FormProjectEdit.vue";

@Component({
  components: {
    ToolbarNavigation,
    FormProjectEdit,
  }
})
export default class AdminProjectsEdit extends VueBase {
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
      text: 'Edit',
      disabled: true,
    },
  ];

  project = {} as ProjectA;

  loadingSubmit = false;
  loadingDelete = false;
  showDeleteDialog = false;

  created() {
    this.requestProject();
  }

  requestProject() {
    this.$api2.getAdminProjectsPgroupPproject(
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
    this.$api2.patchAdminProjectsPgroupPproject(
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
    this.$api2.deleteAdminProjectsPgroupProject(
        this.$route.params.group,
        this.$route.params.project,
    )
        .then(() => {
          this.loadingDelete = false;
          this.showDeleteDialog = false;
          this.toastRequestSuccess();
          this.moveToAdminProjects();
        })
        .catch(error => {
          this.loadingDelete = false;
          this.showDeleteDialog = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
