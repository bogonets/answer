<i18n lang="yaml">
en:
  search_label: "You can filter by key or value."
  add_info: "Add info"
  headers:
    key: "Key"
    value: "Value"
    created_at: "Created at"
    updated_at: "Updated at"
    actions: "Actions"
  title:
    add: "Add info"
    edit: "Edit info"
  subtitle:
    add: "You can add new info."
    edit: "Edit"
  loading: "Loading... Please wait"
  empty_infos: "Empty Infos"
  delete_confirm: "Are you sure? Are you really removing this info?"
  cancel: "Cancel"
  delete: "Delete"

ko:
  search_label: "열쇠 또는 값을 필터링할 수 있습니다."
  add_info: "설정 추가"
  headers:
    key: "열쇠 (Key)"
    value: "값 (Value)"
    created_at: "생성일"
    updated_at: "수정일"
    actions: "관리"
  title:
    add: "설정 추가"
    edit: "설정 변경"
  subtitle:
    add: "새로운 설정을 추가할 수 있습니다."
    edit: "설정을 편집할 수 있습니다."
  loading: "불러오는중 입니다... 잠시만 기다려 주세요."
  empty_infos: "정보가 존재하지 않습니다."
  delete_confirm: "이 정보를 정말 제거합니까?"
  cancel: "취소"
  delete: "제거"
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-data-table
        :headers="headers"
        :items="infos"
        :search="filterText"
        :loading="showLoading"
        :loading-text="$t('loading')"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-text-field
              class="mr-4"
              v-model="filterText"
              append-icon="mdi-magnify"
              :label="$t('search_label')"
              single-line
              hide-details
          ></v-text-field>
          <v-btn color="primary" @click="onClickAddInfo">
            {{ $t('add_info') }}
          </v-btn>
        </v-toolbar>
      </template>

      <template v-slot:item.created_at="{ item }">
        {{ utcToDate(item.created_at) }}
      </template>

      <template v-slot:item.updated_at="{ item }">
        {{ utcToDate(item.updated_at) }}
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon
            v-if="validModifiable(item.key)"
            small
            class="mr-2"
            @click="onClickEditInfo(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
            color="red"
            v-if="validModifiable(item.key)"
            small
            @click="onClickDeleteInfo(item)"
        >
          mdi-delete
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_infos') }}
      </template>
    </v-data-table>

    <!-- Add Dialog -->
    <v-dialog
        v-model="showAddInfoDialog"
        persistent
        max-width="360px"
        no-click-animation
        @keydown.esc.stop="onClickAddInfoCancel"
    >
      <card-info-new
          :title="$t('title.add')"
          :subtitle="$t('subtitle.add')"
          @cancel="onClickAddInfoCancel"
          @ok="onClickAddInfoOk"
      ></card-info-new>
    </v-dialog>

    <!-- Edit Dialog -->
    <v-dialog
        v-model="showEditInfoDialog"
        persistent
        max-width="360px"
        no-click-animation
        @keydown.esc.stop="onClickEditInfoCancel"
    >
      <card-info-new
          disable-key
          disable-validate
          :title="$t('title.edit')"
          :subtitle="$t('subtitle.edit')"
          :init-key="editCandidateKey"
          :init-value="editCandidateValue"
          @cancel="onClickEditInfoCancel"
          @ok="onClickEditInfoOk"
      ></card-info-new>
    </v-dialog>

    <!-- Delete a user dialog. -->
    <v-dialog v-model="showDeleteInfoDialog" max-width="320">
      <v-card>
        <v-card-title class="text-h5 error--text">
          {{ $t('delete') }}
        </v-card-title>
        <v-card-text>
          {{ $t('delete_confirm') }}
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickDeleteInfoCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn
              :loading="showDeleteLoading"
              :disabled="showDeleteLoading"
              color="error"
              @click="onClickDeleteInfoOk"
          >
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
import CardInfoNew from '@/components/CardInfoNew.vue';
import {isReccKey} from '@/rules/recc-info';
import {CreateInfoQ, UpdateInfoQ} from "@/packet/info";

@Component({
  components: {
    ToolbarNavigation,
    CardInfoNew: CardInfoNew,
  }
})
export default class MainAdminInfos extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
    },
    {
      text: 'Infos',
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.key').toString(),
      align: 'start',
      filterable: true,
      value: 'key',
    },
    {
      text: this.$t('headers.value').toString(),
      filterable: true,
      value: 'value',
    },
    {
      text: this.$t('headers.created_at').toString(),
      align: 'center',
      filterable: false,
      value: 'created_at',
    },
    {
      text: this.$t('headers.updated_at').toString(),
      align: 'center',
      filterable: false,
      value: 'updated_at',
    },
    {
      text: this.$t('headers.actions').toString(),
      align: 'center',
      filterable: false,
      sortable: false,
      value: 'actions',
    },
  ];

  filterText = '';
  infos: object = [];
  showAddInfoDialog = false;
  showLoading = true;
  showEditInfoDialog = false;
  showDeleteInfoDialog = false;
  showDeleteLoading = false;
  editCandidateKey = '';
  editCandidateValue = '';
  deleteCandidateKey = '';

  mounted() {
    this.updateInfos();
  }

  updateInfos() {
    this.showLoading = true;
    this.$api2.getAdminInfos()
        .then((infos) => {
          this.infos = infos;
          this.showLoading = false;
        })
        .catch(error => {
          console.error(error);
          this.showLoading = false;
        });
  }

  utcToDate(utc: undefined | string): string {
    return utc?.split('T')[0] || '';
  }

  validModifiable(key: string): boolean {
    return !isReccKey(key);
  }

  validRemovable(key: string): boolean {
    return !isReccKey(key);
  }

  // --------
  // Add info
  // --------

  onClickAddInfo() {
    this.showAddInfoDialog = true;
  }

  onClickAddInfoCancel() {
    this.showAddInfoDialog = false;
  }

  onClickAddInfoOk(event) {
    this.showAddInfoDialog = false;
    const body = {key: event.key, value: event.value} as CreateInfoQ
    this.$api2.postAdminInfos(body)
        .then(() => {
          this.updateInfos();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  // ---------
  // Edit info
  // ---------

  onClickEditInfo(item) {
    this.editCandidateKey = item.key;
    this.editCandidateValue = item.value;
    this.showEditInfoDialog = true;
  }

  onClickEditInfoCancel() {
    this.showEditInfoDialog = false;
  }

  onClickEditInfoOk(event) {
    this.showEditInfoDialog = false;
    const body = {value: event.value} as UpdateInfoQ;
    this.$api2.patchAdminInfosPkey(event.key, body)
        .then(() => {
          this.updateInfos();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.toastRequestFailure(error);
        });
  }

  // -----------
  // Delete info
  // -----------

  onClickDeleteInfo(item) {
    this.deleteCandidateKey = item.key;
    this.showDeleteInfoDialog = true;
  }

  onClickDeleteInfoCancel() {
    this.showDeleteInfoDialog = false;
  }

  onClickDeleteInfoOk() {
    this.showDeleteLoading = true;
    this.$api2.deleteAdminInfo(this.deleteCandidateKey)
        .then(() => {
          this.showDeleteInfoDialog = false;
          this.showDeleteLoading = false;
          this.updateInfos();
          this.toastRequestSuccess();
        })
        .catch(error => {
          this.showDeleteInfoDialog = false;
          this.showDeleteLoading = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>
