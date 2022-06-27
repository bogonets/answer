<i18n lang="yaml">
en:
  header:
    basic: 'Edit permission'
    detail: 'Detail'
  subheader:
    basic: "You can edit the permission's basic properties."
    detail: 'Detailed information about this permission.'
  label:
    created_at: 'Created At'
    updated_at: 'Updated At'
    delete: 'Delete a permission'
  hint:
    delete: 'Please be careful! It cannot be recovered.'
    cannot_owner_delete: 'The owner role cannot be deleted.'
  delete_confirm: 'Are you sure? Are you really removing this permission?'
  cancel: 'Cancel'
  delete: 'Delete'

ko:
  header:
    basic: '권한 편집'
    detail: '상세 정보'
  subheader:
    basic: '권한의 기본 속성을 편집할 수 있습니다.'
    detail: '이 권한에 대한 자세한 정보입니다.'
  label:
    created_at: '권한 생성일'
    updated_at: '권한 갱신일'
    delete: '권한 제거'
  hint:
    delete: '주의하세요! 이 명령은 되돌릴 수 없습니다!'
    cannot_owner_delete: '소유자(owner) 권한은 제거할 수 없습니다.'
  delete_confirm: '이 권한를 정말 제거합니까?'
  cancel: '취소'
  delete: '제거'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <left-title :header="$t('header.basic')" :subheader="$t('subheader.basic')">
      <form-role
        disable-slug
        hide-cancel-button
        :disable-all-ignore-lock="original.lock"
        :disable-submit-button="!modified"
        :loading="showSubmitLoading"
        :permissions="permissions"
        :value="current"
        @input="inputCurrent"
        @submit="onClickSubmit"
      ></form-role>
    </left-title>

    <left-title :header="$t('header.detail')" :subheader="$t('subheader.detail')">
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

    <v-alert
      v-if="original.slug === owner"
      outlined
      prominent
      border="left"
      type="warning"
    >
      {{ $t('hint.cannot_owner_delete') }}
    </v-alert>
    <v-alert v-else-if="!original.lock" outlined prominent type="error" class="ma-4">
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
import FormRole from '@/components/FormRole.vue';
import type {RoleA, UpdateRoleQ} from '@recc/api/dist/packet/role';
import {ROLE_SLUG_OWNER} from '@recc/api/dist/packet/role';
import {iso8601ToLocal} from '@/chrono/iso8601';
import * as _ from 'lodash';

@Component({
  components: {
    ToolbarBreadcrumbs,
    LeftTitle,
    FormRole,
  },
})
export default class AdminPermissionsEdit extends VueBase {
  readonly owner = ROLE_SLUG_OWNER;

  readonly navigationItems = [
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

  readonly detailHeaders = [
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

  permissions = [] as Array<string>;
  detailItems = [] as Array<object>;
  current = {} as RoleA;
  original = {} as RoleA;

  modified = false;
  showSubmitLoading = false;
  showDeleteDialog = false;
  showDeleteLoading = false;

  get perm(): string {
    return this.$route.params.perm;
  }

  created() {
    (async () => {
      await this.setup();
    })();
  }

  async setup() {
    try {
      this.permissions = await this.$api2.getMainPermissions();
      const role = await this.$api2.getAdminRolesProle(this.perm);
      this.updatePermission(role);
    } catch (error) {
      this.toastRequestFailure(error);
      this.moveToBack();
    }
  }

  requestRole() {
    this.$api2
      .getAdminRolesProle(this.perm)
      .then(role => {
        this.updatePermission(role);
      })
      .catch(error => {
        this.toastRequestFailure(error);
        this.moveToBack();
      });
  }

  updatePermission(permission: RoleA) {
    this.current = permission;
    this.original = _.cloneDeep(permission);
    this.modified = !_.isEqual(this.original, this.current);

    this.detailItems = [
      {
        name: this.$t('label.created_at'),
        value: iso8601ToLocal(this.original.created_at),
      },
      {
        name: this.$t('label.updated_at'),
        value: iso8601ToLocal(this.original.updated_at),
      },
    ];
  }

  inputCurrent(value: RoleA) {
    this.current = value;
    this.modified = !_.isEqual(this.original, this.current);
  }

  onClickSubmit(event: RoleA) {
    const body = {
      slug: event.slug,
      name: event.name,
      description: event.description,
      hidden: event.hidden,
      lock: event.lock,
      permissions: event.permissions || [],
    } as UpdateRoleQ;

    this.showSubmitLoading = true;
    this.$api2
      .patchAdminRolesProle(this.perm, body)
      .then(() => {
        this.showSubmitLoading = false;
        this.toastRequestSuccess();
        this.requestRole();
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
    this.$api2
      .deleteAdminRolesProle(this.perm)
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
