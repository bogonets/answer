<i18n lang="yaml">
en:
  header:
    basic: "Edit permission"
    detail: "Detail"
  subheader:
    basic: "You can edit the permission's basic properties."
    detail: "Detailed information about this permission."
  label:
    created_at: "Created At"
    updated_at: "Updated At"
    delete: "Delete a permission"
  hint:
    delete: "Please be careful! It cannot be recovered."
  delete_confirm: "Are you sure? Are you really removing this permission?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  header:
    basic: "권한 편집"
    detail: "상세 정보"
  subheader:
    basic: "권한의 기본 속성을 편집할 수 있습니다."
    detail: "이 권한에 대한 자세한 정보입니다."
  label:
    created_at: "권한 생성일"
    updated_at: "권한 갱신일"
    delete: "권한 제거"
  hint:
    delete: "주의하세요! 이 명령은 되돌릴 수 없습니다!"
  delete_confirm: "이 권한를 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <left-title
        :header="$t('header.basic')"
        :subheader="$t('subheader.basic')"
    >
      <form-permission
          disable-slug
          hide-cancel-button
          :disable-all-ignore-lock="original.lock"
          :disable-submit-button="!modified"
          :value="current"
          @input="inputCurrent"
          :loading="showSubmitLoading"
          @ok="onClickOk"
      ></form-permission>
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

    <v-alert v-if="!original.lock" outlined prominent type="error" class="ma-4">
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
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import FormPermission, {PermissionItem} from '@/components/FormPermission.vue';
import {PermissionA, UpdatePermissionQ} from '@/packet/permission';
import {iso8601ToLocal} from '@/chrono/iso8601';
import * as _ from 'lodash';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
    FormPermission,
  }
})
export default class AdminPermissionsEdit extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Permissions',
      disabled: false,
      href: () => this.moveToAdminPermissions(),
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
  current = new PermissionItem();
  original = new PermissionItem();

  modified = false;
  showSubmitLoading = false;
  showDeleteDialog = false;
  showDeleteLoading = false;

  get perm(): string {
    return this.$route.params.perm;
  }

  created() {
    this.requestPermission();
  }

  requestPermission() {
    this.$api2.getAdminPermissionsPperm(this.perm)
        .then(body => {
          this.updatePermission(body);
        })
        .catch(error => {
          this.toastRequestFailure(error);
          this.moveToBack();
        });
  }

  updatePermission(permission: PermissionA) {
    const slug = permission.slug || '';
    const name = permission.name || '';
    const description = permission.description || '';
    const features = permission.features || [];
    const r_layout = permission.r_layout || false;
    const w_layout = permission.w_layout || false;
    const r_storage = permission.r_storage || false;
    const w_storage = permission.w_storage || false;
    const r_manager = permission.r_manager || false;
    const w_manager = permission.w_manager || false;
    const r_graph = permission.r_graph || false;
    const w_graph = permission.w_graph || false;
    const r_member = permission.r_member || false;
    const w_member = permission.w_member || false;
    const r_setting = permission.r_setting || false;
    const w_setting = permission.w_setting || false;
    const hidden = permission.hidden || false;
    const lock = permission.lock || false;
    const createdAt = permission.created_at || '';
    const updatedAt = permission.updated_at || '';

    this.current.slug = slug;
    this.current.name = name;
    this.current.description = description;
    this.current.features = features;
    this.current.r_layout = r_layout;
    this.current.w_layout = w_layout;
    this.current.r_storage = r_storage;
    this.current.w_storage = w_storage;
    this.current.r_manager = r_manager;
    this.current.w_manager = w_manager;
    this.current.r_graph = r_graph;
    this.current.w_graph = w_graph;
    this.current.r_member = r_member;
    this.current.w_member = w_member;
    this.current.r_setting = r_setting;
    this.current.w_setting = w_setting;
    this.current.hidden = hidden;
    this.current.lock = lock;
    this.original.fromObject(this.current);
    this.modified = !_.isEqual(this.original, this.current);

    this.detailItems = [
      {
        name: this.$t('label.created_at'),
        value: iso8601ToLocal(createdAt),
      },
      {
        name: this.$t('label.updated_at'),
        value: iso8601ToLocal(updatedAt),
      },
    ];
  }

  inputCurrent(value: PermissionItem) {
    this.current = value;
    this.modified = !_.isEqual(this.original, this.current);
  }

  onClickOk(event: PermissionItem) {
    const body = {
      slug: event.slug,
      name: event.name,
      description: event.description,
      features: event.features,
      r_layout: event.r_layout,
      w_layout: event.w_layout,
      r_storage: event.r_storage,
      w_storage: event.w_storage,
      r_manager: event.r_manager,
      w_manager: event.w_manager,
      r_graph: event.r_graph,
      w_graph: event.w_graph,
      r_member: event.r_member,
      w_member: event.w_member,
      r_setting: event.r_setting,
      w_setting: event.w_setting,
      hidden: event.hidden,
      lock: event.lock,
    } as UpdatePermissionQ;

    this.showSubmitLoading = true;
    this.$api2.patchAdminPermissionsPperm(this.perm, body)
        .then(() => {
          this.showSubmitLoading = false;
          this.toastRequestSuccess();
          this.requestPermission();
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
    this.$api2.deleteAdminPermissionsPperm(this.perm)
        .then(() => {
          this.showDeleteLoading = false;
          this.showDeleteDialog = false;
          this.toastRequestSuccess();
          this.moveToAdminPermissions();
        })
        .catch(error => {
          this.showDeleteLoading = false;
          this.showDeleteDialog = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
