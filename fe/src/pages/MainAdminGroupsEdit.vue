<i18n lang="yaml">
en:
  header:
    basic: "Edit group"
    detail: "Detail"
  subheader:
    basic: "You can edit the group's basic properties."
    detail: "Detailed information about this group."
  label:
    created_at: "Created At"
    updated_at: "Updated At"
    delete: "Delete a group"
  hint:
    delete: "Please be careful! It cannot be recovered."
  delete_confirm: "Are you sure? Are you really removing this group?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  header:
    basic: "그룹 편집"
    detail: "상세 정보"
  subheader:
    basic: "그룹의 기본 속성을 편집할 수 있습니다."
    detail: "이 그룹에 대한 자세한 정보입니다."
  label:
    created_at: "계정 생성일"
    updated_at: "계정 갱신일"
    delete: "그룹 제거"
  hint:
    delete: "주의하세요! 이 명령은 되돌릴 수 없습니다!"
  delete_confirm: "이 그룹을 정말 제거합니까?"
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
      <form-group
          disable-slug
          hide-cancel-button
          v-model="current"
          :loading="showSubmitLoading"
          @ok="onClickOk"
      ></form-group>
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
import FormGroup, {GroupItem} from '@/components/FormGroup.vue';
import {GroupA, UpdateGroupQ} from '@/packet/group';

@Component({
  components: {
    ToolbarNavigation,
    LeftTitle,
    FormGroup,
  }
})
export default class MainAdminGroupsEdit extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Groups',
      disabled: false,
      href: () => this.moveToMainAdminGroups(),
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
  current = new GroupItem();

  showSubmitLoading = false;
  showDeleteDialog = false;
  showDeleteLoading = false;

  get group(): string {
    return this.$route.params.group;
  }

  created() {
    this.requestGroup();
  }

  requestGroup() {
    this.$api2.getGroupsPgroup(this.group)
        .then(body => {
          this.updateGroup(body);
        })
        .catch(error => {
          this.toastRequestFailure(error);
          this.moveToBack();
        });
  }

  updateGroup(group: GroupA) {
    const name = group.name || '';
    const description = group.description || '';
    const features = group.features || [];
    const createdAt = group.created_at || '';
    const updatedAt = group.updated_at || '';

    this.current.slug = this.group;
    this.current.name = name;
    this.current.description = description;
    this.current.features = features;

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

  onClickOk(event: GroupItem) {
    const body = {
      name: event.name,
      description: event.description,
      features: event.features,
    } as UpdateGroupQ;

    this.showSubmitLoading = true;
    this.$api2.patchGroupsPgroup(this.group, body)
        .then(() => {
          this.showSubmitLoading = false;
          this.toastRequestSuccess();
          this.requestGroup();
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
    this.$api2.deleteGroupsGroup(this.group)
        .then(() => {
          this.showDeleteLoading = false;
          this.showDeleteDialog = false;
          this.toastRequestSuccess();
          this.moveToMainAdminGroups();
        })
        .catch(error => {
          this.showDeleteLoading = false;
          this.showDeleteDialog = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
