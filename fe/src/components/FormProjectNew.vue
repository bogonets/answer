<i18n lang="yaml">
en:
  header: 'New project'
  subheader: >
    A project is where you house your files, manage tasks, and do graph-based programming.

ko:
  header: '새로운 프로젝트'
  subheader: >
    프로젝트는 파일을 보관하고, 작업을 관리하고, 그래프 기반 프로그래밍을 수행하는 곳입니다.
</i18n>

<template>
  <left-title :header="$t('header')" :subheader="$t('subheader')">
    <form-project
      hide-origin-prefix
      hide-cancel-button
      :hide-features="hideFeatures"
      :hide-visibility="hideVisibility"
      :loading-groups="loadingGroups"
      :loading-submit="loadingSubmit"
      :disable-group="disableGroup"
      :group-items="groupItems"
      :feature-items="featureItems"
      :init-group="initGroup"
      @ok="ok"
    ></form-project>
  </left-title>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import LeftTitle from '@/components/LeftTitle.vue';
import FormProject, {ProjectItem} from '@/components/FormProject.vue';
import {CreateProjectQ} from '@recc/api/dist/packet/project';

@Component({
  components: {
    LeftTitle,
    FormProject,
  },
})
export default class FormProjectNew extends VueBase {
  @Prop({type: Boolean})
  readonly hideFeatures!: boolean;

  @Prop({type: Boolean})
  readonly hideVisibility!: boolean;

  @Prop({type: Boolean})
  readonly loadingGroups!: boolean;

  @Prop({type: Boolean})
  readonly loadingSubmit!: boolean;

  @Prop({type: Boolean})
  readonly disableGroup!: boolean;

  @Prop({type: Array})
  readonly groupItems!: Array<string>;

  @Prop({type: Array})
  readonly featureItems!: Array<string>;

  @Prop({type: String})
  readonly initGroup!: string;

  @Emit()
  ok(event: ProjectItem) {
    return {
      group_slug: event.group,
      project_slug: event.slug,
      name: event.name,
      description: event.description,
      features: event.features,
      visibility: event.visibility,
    } as CreateProjectQ;
  }
}
</script>
