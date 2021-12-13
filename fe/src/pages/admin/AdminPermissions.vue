<i18n lang="yaml">
en:
  search_label: "You can filter by name or description."
  new_item: "New Permission"
  headers:
    group: "Group"
    slug: "Slug"
    name: "Name"
    description: "Description"
    hidden: "Hidden"
    lock: "Lock"
    created_at: "Created at"
    updated_at: "Updated at"
    actions: "Actions"
  loading: "Loading... Please wait"
  empty_items: "Empty Permissions"

ko:
  search_label: "이름 또는 설명을 필터링할 수 있습니다."
  new_item: "새로운 권한"
  headers:
    group: "그룹"
    slug: "슬러그"
    name: "이름"
    description: "설명"
    hidden: "숨김"
    lock: "잠금"
    created_at: "생성일"
    updated_at: "수정일"
    actions: "관리"
  loading: "불러오는중 입니다... 잠시만 기다려 주세요."
  empty_items: "프로젝트가 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <toolbar-breadcrumbs :items="navigationItems"></toolbar-breadcrumbs>
    <v-divider></v-divider>

    <v-data-table
        :headers="headers"
        :items="tableItems"
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
          <v-btn color="primary" @click="onClickNew">
            {{ $t('new_item') }}
          </v-btn>
        </v-toolbar>
      </template>

      <template v-slot:item.hidden="{ item }">
        <v-icon dense v-if="item.hidden">{{ hiddenIcon(item) }}</v-icon>
      </template>

      <template v-slot:item.lock="{ item }">
        <v-icon dense v-if="item.lock">{{ lockIcon(item) }}</v-icon>
      </template>

      <template v-slot:item.created_at="{ item }">
        {{ datetimeToDate(item.created_at) }}
      </template>

      <template v-slot:item.updated_at="{ item }">
        {{ datetimeToDate(item.updated_at) }}
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="onClickEdit(item)">
          mdi-pencil
        </v-icon>
      </template>

      <template v-slot:no-data>
        {{ $t('empty_items') }}
      </template>
    </v-data-table>

  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarBreadcrumbs from '@/components/ToolbarBreadcrumbs.vue';
import {RuleA} from '@/packet/rule';
import {iso8601ToLocalDate} from '@/chrono/iso8601';

@Component({
  components: {
    ToolbarBreadcrumbs,
  }
})
export default class AdminPermissions extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Admin',
      disabled: false,
      href: () => this.moveToAdmin(),
    },
    {
      text: 'Permissions',
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.slug').toString(),
      align: 'center',
      filterable: true,
      value: 'slug',
    },
    {
      text: this.$t('headers.name').toString(),
      align: 'center',
      filterable: true,
      value: 'name',
    },
    {
      text: this.$t('headers.description').toString(),
      align: 'center',
      filterable: true,
      value: 'description',
    },
    {
      text: this.$t('headers.hidden').toString(),
      align: 'center',
      sortable: false,
      filterable: false,
      value: 'hidden',
    },
    {
      text: this.$t('headers.lock').toString(),
      align: 'center',
      sortable: false,
      filterable: false,
      value: 'lock',
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
  tableItems = [] as Array<RuleA>;
  showLoading = true;

  mounted() {
    this.updateItems();
  }

  updateItems() {
    this.showLoading = true;
    this.$api2.getAdminRules()
        .then(items => {
          this.tableItems = items;
          this.showLoading = false;
        })
        .catch(error => {
          this.showLoading = false;
          this.toastRequestFailure(error);
        });
  }

  datetimeToDate(text) {
    return iso8601ToLocalDate(text);
  }

  onClickNew() {
    this.moveToAdminPermissionsNew();
  }

  onClickEdit(item: RuleA) {
    this.moveToAdminPermissionsEdit(item.slug);
  }

  hiddenIcon(item: RuleA) {
    if (item.hidden) {
      return 'mdi-eye-off';
    } else {
      return 'mdi-eye';
    }
  }

  lockIcon(item: RuleA) {
    if (item.lock) {
      return 'mdi-lock';
    } else {
      return 'mdi-lock-open-variant';
    }
  }
}
</script>
