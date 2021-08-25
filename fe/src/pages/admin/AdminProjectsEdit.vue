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
  msg:
    no_group: "Not exists group slug."
    no_project: "Not exists project slug."
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
  msg:
    no_group: "그룹 슬러그가 없습니다."
    no_project: "프로젝트 슬러그가 없습니다."
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
          :group-items="[this.group]"
          :value="current"
          @input="inputCurrent"
          :loading-submit="loadingSubmit"
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
          <v-btn :loading="loadingDelete" color="error" @click="onClickDeleteOk">
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
  loadingSubmit = false;
  loadingDelete = false;
  showDeleteDialog = false;

  group = '';
  project = '';

  created() {
    this.group = this.$route.params.group || '';
    this.project = this.$route.params.project || '';

    if (!this.group) {
      this.toastError(this.$t('msg.no_group'));
      this.moveToBack();
      return;
    }

    if (!this.project) {
      this.toastError(this.$t('msg.no_project'));
      this.moveToBack();
      return;
    }

    this.requestProject();
  }

  requestProject() {
    this.$api2.getAdminProjectsPgroupPproject(this.group, this.project)
        .then(items => {
          this.updateProject(items)
        })
        .catch(error => {
          this.toastRequestFailure(error);
          this.moveToBack();
        });
  }

  updateProject(items: ProjectA) {
    const name = items.name || '';
    const description = items.description || '';
    const features = items.features || [];
    const visibility = items.visibility || 0;
    const createdAt = items.created_at || '';
    const updatedAt = items.updated_at || '';

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

    this.loadingSubmit = true;
    this.$api2.patchAdminProjectsPgroupPproject(this.group, this.project, body)
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
    this.loadingDelete = true;
    this.$api2.deleteAdminProjectsPgroupProject(this.group, this.project)
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
