<i18n lang="yaml">
en:
  search_label: "You can filter by key or value."
  headers:
    key: "Key"
    type: "Type"
    value: "Value"
    actions: "Actions"
  loading: "Loading... Please wait"
  empty_configs: "Empty Configs"

ko:
  search_label: "열쇠 또는 값을 필터링할 수 있습니다."
  headers:
    key: "열쇠 (Key)"
    type: "자료형 (Type)"
    value: "값 (Value)"
    actions: "관리"
  loading: "불러오는중 입니다... 잠시만 기다려 주세요."
  empty_configs: "설정이 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-data-table
        :headers="headers"
        :items="configs"
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
        </v-toolbar>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon
            v-if="false"
            small
            class="mr-2"
            @click="onClickEditConfig(item)"
        >
          mdi-pencil
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_configs') }}
      </template>
    </v-data-table>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation
  }
})
export default class AdminConfigs extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToMainAdminOverview(),
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
  configs: object = [];
  showLoading = true;

  editCandidateKey = '';
  editCandidateValue = '';
  showEditConfigDialog = false;

  mounted() {
    this.updateConfigs();
  }

  updateConfigs() {
    this.showLoading = true;
    this.$api2.getAdminConfigs()
        .then((infos) => {
          this.configs = infos;
          this.showLoading = false;
        })
        .catch(error => {
          console.error(error);
          this.showLoading = false;
        });
  }

  onClickEditConfig(item) {
    this.editCandidateKey = item.key;
    this.editCandidateValue = item.value;
    this.showEditConfigDialog = true;
  }

}
</script>
