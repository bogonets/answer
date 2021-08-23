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
  <left-title
      :header="$t('header')"
      :subheader="$t('subheader')"
  >
    <form-project
        hide-origin-prefix
        :request-type="requestType"
        :loading="submitLoading"
        @cancel="cancel"
        @ok="onClickOk"
    ></form-project>
  </left-title>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import LeftTitle from "@/components/LeftTitle.vue";
import FormProject, {ProjectItem} from '@/components/FormProject.vue';
import {CreateProjectQ} from '@/packet/project';

const REQUEST_TYPE_SELF = 'self';
const REQUEST_TYPE_ADMIN = 'admin';

@Component({
  components: {
    ToolbarNavigation,
    LeftTitle,
    FormProject,
  }
})
export default class FormProjectNew extends VueBase {
  @Prop({type: String, default: REQUEST_TYPE_SELF})
  readonly requestType!: string;

  @Prop({type: Boolean, default: false})
  readonly hideToast!: boolean;

  submitLoading = false;

  @Emit()
  cancel() {
    // EMPTY.
  }

  @Emit('request:success')
  requestSuccess() {
    this.submitLoading = false;
    if (this.hideToast) {
      this.toastRequestSuccess();
    }
  }

  @Emit('request:failure')
  requestFailure(error) {
    this.submitLoading = false;
    if (this.hideToast) {
      this.toastRequestFailure(error);
    }
    return error;
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
    if (this.requestType === REQUEST_TYPE_SELF) {
      this.requestPostSelfProjects(body);
    } else if (this.requestType === REQUEST_TYPE_ADMIN) {
      this.requestPostProjects(body);
    } else {
      throw Error(`Unknown request type: ${this.requestType}`);
    }
  }

  requestPostProjects(body: CreateProjectQ) {
    this.$api2.postAdminProjects(body)
        .then(() => {
          this.requestSuccess();
        })
        .catch(error => {
          this.requestFailure(error);
        });
  }

  requestPostSelfProjects(body: CreateProjectQ) {
    this.$api2.postMainProjects(body)
        .then(() => {
          this.requestSuccess();
        })
        .catch(error => {
          this.requestFailure(error);
        });
  }
}
</script>
