<i18n lang="yaml">
en:
  header:
    basic: "Basic"
    detail: "Detail"
  subheader:
    basic: "This is essential information."
    detail: "Detailed information about this group."
  label:
    name: "Name"
    description: "Description"
    features: "Features"
    created_at: "Created At"
    updated_at: "Updated At"
    delete: "Delete a group"
  hint:
    name: "A human-readable group name."

ko:
  header:
    basic: "기본 정보"
    detail: "상세 정보"
  subheader:
    basic: "반드시 필요한 정보 입니다."
    detail: "이 그룹에 대한 자세한 정보입니다."
  label:
    name: "이름"
    description: "설명"
    features: "기능"
    created_at: "계정 생성일"
    updated_at: "계정 갱신일"
    delete: "그룹 제거"
  hint:
    name: "사람이 읽기 쉬운 그룹 이름 입니다."
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <left-title
        :header="$t('header.basic')"
        :subheader="$t('subheader.basic')"
    >
      <text-field-three-line
          :label="$t('label.name')"
          :hint="$t('hint.name')"
          :value="originalGroup.name"
      ></text-field-three-line>
    </left-title>

    <v-divider></v-divider>

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

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';
import TextFieldThreeLine from '@/components/TextFieldThreeLine.vue';
import LeftTitle from '@/components/LeftTitle.vue';
import RightControl from '@/components/RightControl.vue';
import {Group} from '@/apis/api-v2';

@Component({
  components: {
    RightControl,
    ToolbarNavigation,
    TextFieldThreeLine,
    LeftTitle,
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

  detailItems: Array<object> = [];
  originalGroup: Group = {};

  name = '';
  description = '';
  features: Array<string> = [];

  disableSubmit = true;
  showIsAdminLoading = false;
  showSignupLoading = false;
  showDeleteUserDialog = false;
  showDeleteLoading = false;

  created() {
    const group = this.$route.params.group as Group;
    // const name = group?.name || '';
    // if (!name) {
    //   console.error('Group name is not exists.');
    //   this.moveToMainAdminGroups();
    // }

    this.name = group.name || '';
    this.description = group.description || '';
    this.features = group.features || [];
    const created_at = group.created_at || '';
    const updated_at = group.updated_at || '';

    this.originalGroup = {
      name: this.name,
      description: this.description,
      features: this.features,
      created_at: created_at,
      updated_at: updated_at,
    } as Group;

    this.detailItems = [
      {
        name: this.$t('label.created_at'),
        value: created_at,
      },
      {
        name: this.$t('label.updated_at'),
        value: updated_at,
      },
    ];
  }

  get groupName(): string {
    return this.originalGroup.name || '';
  }

  onClickDelete() {
    this.showDeleteUserDialog = true;
  }

  onClickClear() {
    this.name = this.originalGroup.name || '';
    this.description = this.originalGroup.description || '';
    this.features = this.originalGroup.features || [];
  }

  onClickSubmit() {
    const patchGroup = {
      description: this.description,
      features: this.features,
    } as Group;

    this.showSignupLoading = true;
    this.$api2.patchGroupsGroup(this.name, patchGroup)
        .then(() => {
          this.showSignupLoading = false;
          this.toastRequestSuccess();

          this.originalGroup.name = patchGroup.name;
          this.originalGroup.description = patchGroup.description;
          this.originalGroup.features = patchGroup.features;
        })
        .catch(error => {
          this.showSignupLoading = false;
          this.toastRequestFailure(error);
        });
  }

  onClickDeleteUserCancel() {
    this.showDeleteUserDialog = false;
  }

  onClickDeleteUserOk() {
    this.showDeleteLoading = true;
    this.$api2.deleteGroupsGroup(this.name)
        .then(() => {
          this.showDeleteLoading = false;
          this.showDeleteUserDialog = false;
          this.toastRequestSuccess();
          this.moveToMainAdminGroups();
        })
        .catch(error => {
          this.showDeleteLoading = false;
          this.showDeleteUserDialog = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
