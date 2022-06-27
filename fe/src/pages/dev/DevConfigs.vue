<i18n lang="yaml">
en:
  search_label: 'You can filter by key or value.'
  headers:
    key: 'Key'
    type: 'Type'
    value: 'Value'
    actions: 'Actions'
  loading: 'Loading... Please wait'
  empty_configs: 'Empty Configs'

ko:
  search_label: '열쇠 또는 값을 필터링할 수 있습니다.'
  headers:
    key: '열쇠 (Key)'
    type: '자료형 (Type)'
    value: '값 (Value)'
    actions: '관리'
  loading: '불러오는중 입니다... 잠시만 기다려 주세요.'
  empty_configs: '설정이 존재하지 않습니다.'
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-data-table
      :headers="headers"
      :items="items"
      :search="filterText"
      :loading="loading"
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
        </v-toolbar>
      </template>

      <template v-slot:item.actions="{item}">
        <v-icon small class="mr-2" @click="onClickEditConfig(item)">mdi-pencil</v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_configs') }}
      </template>
    </v-data-table>

    <!-- Add Dialog -->
    <v-dialog
      v-model="showEditConfigDialog"
      persistent
      max-width="360"
      no-click-animation
      @keydown.esc.stop="onClickEditConfigCancel"
    >
      <config-card
        mode="edit"
        :config-key="editCandidateKey"
        :config-type="editCandidateType"
        :config-value="editCandidateValue"
        :loading-submit="loadingEditConfigSubmit"
        @cancel="onClickEditConfigCancel"
        @ok="onClickEditConfigOk"
      ></config-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import ConfigCard from '@/config/ConfigCard.vue';
import {ConfigA, UpdateConfigValueQ} from '@recc/api/dist/packet/config';

@Component({
  components: {
    ToolbarBreadcrumbs,
    ConfigCard,
  },
})
export default class DevConfigs extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Dev',
      disabled: false,
      href: () => this.moveToDev(),
    },
    {
      text: 'Configs',
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
      text: this.$t('headers.type').toString(),
      align: 'center',
      filterable: true,
      value: 'type',
    },
    {
      text: this.$t('headers.value').toString(),
      align: 'center',
      filterable: true,
      value: 'value',
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
  items = [] as Array<ConfigA>;
  loading = true;

  showEditConfigDialog = false;
  loadingEditConfigSubmit = false;
  editCandidateKey = '';
  editCandidateType = '';
  editCandidateValue = '';

  mounted() {
    this.updateConfigs();
  }

  updateConfigs() {
    this.loading = true;
    this.$api2
      .getDevConfigs()
      .then(items => {
        this.items = items;
        this.loading = false;
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  onClickEditConfig(item: ConfigA) {
    this.editCandidateKey = item.key;
    this.editCandidateType = item.type;
    this.editCandidateValue = item.value;
    this.showEditConfigDialog = true;
  }

  onClickEditConfigCancel() {
    this.showEditConfigDialog = false;
  }

  onClickEditConfigOk(item: ConfigA) {
    this.loadingEditConfigSubmit = true;
    const body = {
      value: item.value,
    } as UpdateConfigValueQ;
    this.$api2
      .patchDevConfigsPkey(item.key, body)
      .then(() => {
        this.showEditConfigDialog = false;
        this.loadingEditConfigSubmit = false;
        this.toastRequestSuccess();
        this.updateConfigs();
      })
      .catch(error => {
        this.loadingEditConfigSubmit = false;
        this.toastRequestFailure(error);
      });
  }
}
</script>
