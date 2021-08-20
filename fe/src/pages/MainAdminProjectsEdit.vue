<i18n lang="yaml">
en:
  header:
    basic: "Edit project"
    detail: "Detail"
  subheader:
    basic: "You can edit the project's basic properties."
    detail: "Detailed information about this project."
  label:
    created_at: "Created At"
    updated_at: "Updated At"
    delete: "Delete a project"
  hint:
    delete: "Please be careful! It cannot be recovered."
  delete_confirm: "Are you sure? Are you really removing this project?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  header:
    basic: "프로젝트 편집"
    detail: "상세 정보"
  subheader:
    basic: "프로젝트의 기본 속성을 편집할 수 있습니다."
    detail: "이 프로젝트에 대한 자세한 정보입니다."
  label:
    created_at: "프로젝트 생성일"
    updated_at: "프로젝트 갱신일"
    delete: "프로젝트 제거"
  hint:
    delete: "주의하세요! 이 명령은 되돌릴 수 없습니다!"
  delete_confirm: "이 프로젝트를 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <left-title
        :header="$t('header.basic')"
        :subheader="$t('subheader.basic')"
    >
      <form-project
          disable-group
          disable-slug
          hide-cancel-button
          :disable-submit-button="!modified"
          :value="current"
          @input="inputCurrent"
          :loading="showSubmitLoading"
          @ok="onClickOk"
      ></form-project>
    </left-title>

    <left-title
        :header="$t('header.detail')"
        :subheader="$t('subheader.detail')"
    >
      <v-card outlined>
        <v-data-table
            hide-default-header
            hide-default-footer
            :headers="detailHeaders"
            :items="detailItems"
            item-key="name"
            class="elevation-1"
        ></v-data-table>
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
          <v-btn :loading="showDeleteLoading" color="error" @click="onClickDeleteOk">
            {{ $t('delete') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import FormProject, {ProjectItem} from '@/components/FormProject.vue';
import {ProjectA, UpdateProjectQ} from '@/packet/project';
import * as _ from 'lodash';

@Component({
  components: {
    ToolbarNavigation,
    LeftTitle,
    FormProject,
  }
})
export default class MainAdminProjectsEdit extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Projects',
      disabled: false,
      href: () => this.moveToMainAdminProjects(),
    },
    {
      text: 'Edit',
      disabled: true,
    },
  ];

  private readonly detailHeaders = [
    {
      text: 'name',
      value: 'name',
      align: 'right',
    },
    {
      text: 'value',
      value: 'value',
    },
  ];

  detailItems = [] as Array<object>;
  current = new ProjectItem();
  original = new ProjectItem();

  modified = false;
  showSubmitLoading = false;
  showDeleteDialog = false;
  showDeleteLoading = false;

  get group(): string {
    return this.$route.params.group;
  }

  get project(): string {
    return this.$route.params.project;
  }

  created() {
    this.requestProject();
  }

  requestProject() {
    this.$api2.getProjectsPgroupPproject(this.group, this.project)
        .then(body => {
          this.updateProject(body);
        })
        .catch(error => {
          this.toastRequestFailure(error);
          this.moveToBack();
        });
  }

  updateProject(group: ProjectA) {
    const name = group.name || '';
    const description = group.description || '';
    const features = group.features || [];
    const visibility = group.visibility || 0;
    const createdAt = group.created_at || '';
    const updatedAt = group.updated_at || '';

    this.current.group = this.group;
    this.current.slug = this.project;
    this.current.name = name;
    this.current.description = description;
    this.current.features = features;
    this.current.visibility = visibility;
    this.original.fromObject(this.current);
    this.modified = !_.isEqual(this.original, this.current);

    this.detailItems = [
      {
        name: this.$t('label.created_at'),
        value: createdAt,
      },
      {
        name: this.$t('label.updated_at'),
        value: updatedAt,
      },
    ];
  }

  inputCurrent(value: ProjectItem) {
    this.current = value;
    this.modified = !_.isEqual(this.original, this.current);
  }

  onClickOk(event: ProjectItem) {
    const body = {
      name: event.name,
      description: event.description,
      features: event.features,
      visibility: event.visibility,
    } as UpdateProjectQ;

    this.showSubmitLoading = true;
    this.$api2.patchProjectsPgroupPproject(this.group, this.project, body)
        .then(() => {
          this.showSubmitLoading = false;
          this.toastRequestSuccess();
          this.requestProject();
        })
        .catch(error => {
          this.showSubmitLoading = false;
          this.toastRequestFailure(error);
        });
  }

  // ------
  // Delete
  // ------

  onClickDelete() {
    this.showDeleteDialog = true;
  }

  onClickDeleteCancel() {
    this.showDeleteDialog = false;
  }

  onClickDeleteOk() {
    this.showDeleteLoading = true;
    this.$api2.deleteProjectsPgroupProject(this.group, this.project)
        .then(() => {
          this.showDeleteLoading = false;
          this.showDeleteDialog = false;
          this.toastRequestSuccess();
          this.moveToMainAdminProjects();
        })
        .catch(error => {
          this.showDeleteLoading = false;
          this.showDeleteDialog = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
