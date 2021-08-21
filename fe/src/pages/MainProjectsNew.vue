<i18n lang="yaml">
en:
  header: "New project"
  subheader: >
    A project is where you house your files, manage tasks, and do graph-based programming.

ko:
  header: "새로운 프로젝트"
  subheader: >
    프로젝트는 파일을 보관하고, 작업을 관리하고, 그래프 기반 프로그래밍을 수행하는 곳입니다.
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <left-title
        :header="$t('header')"
        :subheader="$t('subheader')"
    >
      <form-project
          :loading="submitLoading"
          @cancel="onClickCancel"
          @ok="onClickOk"
      ></form-project>
    </left-title>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import LeftTitle from "@/components/LeftTitle.vue";
import FormProject, {ProjectItem} from '@/components/FormProject.vue';
import {CreateProjectQ} from '@/packet/project';

@Component({
  components: {
    ToolbarNavigation,
    LeftTitle,
    FormProject,
  }
})
export default class MainProjectsNew extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToMainProjects(),
    },
    {
      text: 'New',
      disabled: true,
    },
  ];

  submitLoading = false;

  onClickCancel() {
    this.moveToBack();
  }

  onClickOk(event: ProjectItem) {
    const body = {
      group_slug: event.group,
      project_slug: event.slug,
      name: event.name,
      description: event.description,
      features: event.features,
      visibility: event.visibility,
    } as CreateProjectQ;

    this.submitLoading = true;
    this.$api2.postSelfProjects(body)
        .then(() => {
          this.submitLoading = false;
          this.moveToMainAdminProjects();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.submitLoading = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
