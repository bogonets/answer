<template>
  <v-container>
    <breadcrumb-main name="Settings"></breadcrumb-main>
    <v-divider></v-divider>

    <form-project-edit
        hide-features
        hide-visibility
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
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';
import FormProjectEdit from '@/components/FormProjectEdit.vue';
import {ProjectA, UpdateProjectQ} from '@/packet/project';

@Component({
  components: {
    BreadcrumbMain,
    FormProjectEdit,
  }
})
export default class MainSettings extends VueBase {
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
