<i18n lang="yaml">
en:
  title: "Settings"
  subtitle: "Modify environment variables used in the system."
  search_label: "You can filter by key or value."
  add_info: "Add info"
  headers:
    key: "Key"
    value: "Value"
    created_at: "Created at"
    updated_at: "Updated at"
    actions: "Actions"
  empty_infos: ""

ko:
  title: "환경설정"
  subtitle: "시스템에서 사용되는 환경변수를 수정합니다."
  search_label: "열쇠 또는 값을 필터링할 수 있습니다."
  add_info: "설정 추가"
  headers:
    key: "열쇠 (Key)"
    value: "값 (Value)"
    created_at: "생성일"
    updated_at: "수정일"
    actions: "관리"
  empty_infos: ""
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
            small
            class="mr-2"
            :disabled="validModifiable(item.key)"
            @click="onClickEditInfo(item)"
        >
          mdi-pencil
        </v-icon>
        <v-icon
            small
            color="red"
            :disabled="validRemovable(item.key)"
            @click="onClickRemoveInfo(item)"
        >
          mdi-delete
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_infos') }}
      </template>

    </v-data-table>

  </v-container>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

const RECC_REGEX = /^recc\..*/;

@Component({
  components: {
    ToolbarNavigation,
  }
})
export default class SettingsPage extends VueBase {

  filterText = "";
  navigationItems: object = [];
  headers: object = [];
  infos: object = [];
  showLoading = true;

  created() {
    this.navigationItems = [
      {
        text: 'Admin',
        disabled: false,
        href: this.paths.mainConfigAdminOverview,
      },
      {
        text: 'Settings',
        disabled: true,
      },
    ];
    this.headers = [
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
    ]
  }

  mounted() {
    this.$api2.getInfos()
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
    return !!RECC_REGEX.exec(key);
  }

  validRemovable(key: string): boolean {
    return !!RECC_REGEX.exec(key);
  }

  onClickAddInfo() {
  }

  onClickEditInfo(item) {
  }

  onClickRemoveInfo(item) {
  }
}
</script>
