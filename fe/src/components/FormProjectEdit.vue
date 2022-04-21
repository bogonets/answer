<i18n lang="yaml">
en:
  header:
    basic: 'Edit project'
    detail: 'Detail'
  subheader:
    basic: "You can edit the project's basic properties."
    detail: 'Detailed information about this project.'
  label:
    created_at: 'Created At'
    updated_at: 'Updated At'
    delete: 'Delete a project'
  hint:
    delete: 'Please be careful! It cannot be recovered.'
  delete_confirm: 'Are you sure? Are you really removing this project?'
  cancel: 'Cancel'
  delete: 'Delete'

ko:
  header:
    basic: '프로젝트 편집'
    detail: '상세 정보'
  subheader:
    basic: '프로젝트의 기본 속성을 편집할 수 있습니다.'
    detail: '이 프로젝트에 대한 자세한 정보입니다.'
  label:
    created_at: '프로젝트 생성일'
    updated_at: '프로젝트 갱신일'
    delete: '프로젝트 제거'
  hint:
    delete: '주의하세요! 이 명령은 되돌릴 수 없습니다!'
  delete_confirm: '이 프로젝트를 정말 제거합니까?'
  cancel: '취소'
  delete: '제거'
</i18n>

<template>
  <div>
    <left-title :header="$t('header.basic')" :subheader="$t('subheader.basic')">
      <form-project
        disable-group
        disable-slug
        hide-cancel-button
        :hide-features="hideFeatures"
        :hide-visibility="hideVisibility"
        :disable-submit-button="!modified"
        :group-items="[this.groupSlug]"
        :value="current"
        @input="onUpdateCurrent"
        :loading-submit="loadingSubmit"
        @ok="onClickOk"
      ></form-project>
    </left-title>

    <left-title :header="$t('header.detail')" :subheader="$t('subheader.detail')">
      <v-card outlined>
        <v-simple-table class="elevation-1">
          <template v-slot:default>
            <tbody>
              <tr>
                <td>{{ $t('label.created_at') }}</td>
                <td>{{ createdAt }}</td>
              </tr>
              <tr>
                <td>{{ $t('label.updated_at') }}</td>
                <td>{{ updatedAt }}</td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </v-card>
    </left-title>

    <v-alert outlined prominent type="error" class="ma-4">
      <v-row align="center" class="pl-4">
        <v-col>
          <v-row>
            <h6 class="text-h6">{{ $t('label.delete') }}</h6>
          </v-row>
          <v-row>
            <span class="text-body-2">{{ $t('hint.delete') }}</span>
          </v-row>
        </v-col>
        <v-col class="shrink">
          <v-btn color="error" @click.stop="onClickDelete">
            {{ $t('delete') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <!-- Delete dialog. -->
    <v-dialog v-model="showDeleteDialog" max-width="320">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('label.delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('delete_confirm') }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickDeleteCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn :loading="loadingDelete" color="error" @click="onClickDeleteOk">
            {{ $t('delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Emit, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import LeftTitle from '@/components/LeftTitle.vue';
import type {ProjectA, UpdateProjectQ} from '@/packet/project';
import FormProject, {ProjectItem} from '@/components/FormProject.vue';
import {iso8601ToLocal} from '@/chrono/iso8601';
import * as _ from 'lodash';

export function createEmptyProjectA() {
  return {
    group_slug: '',
    project_slug: '',
  } as ProjectA;
}

@Component({
  components: {
    LeftTitle,
    FormProject,
  },
})
export default class FormProjectEdit extends VueBase {
  @Prop({type: Boolean})
  readonly hideFeatures!: boolean;

  @Prop({type: Boolean})
  readonly hideVisibility!: boolean;

  @Prop({type: Object, default: createEmptyProjectA})
  readonly value!: ProjectA;

  @Prop({type: Boolean, default: false})
  readonly showDeleteDialog!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loadingDelete!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loadingSubmit!: boolean;

  current = new ProjectItem();
  original = new ProjectItem();
  modified = false;

  get groupSlug() {
    return this.value?.group_slug || '';
  }

  get createdAt() {
    return iso8601ToLocal(this.value?.created_at || '');
  }

  get updatedAt() {
    return iso8601ToLocal(this.value?.updated_at || '');
  }

  @Watch('value')
  onChangeValue(newVal: ProjectA) {
    this.updateProject(newVal);
  }

  updateProject(items: ProjectA) {
    const group_slug = items.group_slug || '';
    const project_slug = items.project_slug || '';
    const name = items.name || '';
    const description = items.description || '';
    const features = items.features || [];
    const visibility = items.visibility || 0;

    this.current.group = group_slug;
    this.current.slug = project_slug;
    this.current.name = name;
    this.current.description = description;
    this.current.features = features;
    this.current.visibility = visibility;
    this.original.fromObject(this.current);
    this.modified = !_.isEqual(this.original, this.current);
  }

  onUpdateCurrent(value: ProjectItem) {
    this.current = value;
    this.modified = !_.isEqual(this.original, this.current);
  }

  @Emit('ok')
  onClickOk(event: ProjectItem) {
    return {
      name: event.name,
      description: event.description,
      features: event.features,
      visibility: event.visibility,
    } as UpdateProjectQ;
  }

  @Emit('delete:show')
  onClickDelete() {
    // EMPTY
  }

  @Emit('delete:cancel')
  onClickDeleteCancel() {
    // EMPTY
  }

  @Emit('delete:ok')
  onClickDeleteOk() {
    // EMPTY
  }
}
</script>
