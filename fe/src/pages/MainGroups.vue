<i18n lang="yaml">
en:
  search_label: "You can filter by name or description."
  new_item: "New Group"
  headers:
    slug: "Slug"
    name: "Name"
    description: "Description"
    created_at: "Created at"
    updated_at: "Updated at"
    actions: "Actions"
  loading: "Loading... Please wait"
  empty_items: "Empty Groups"

ko:
  search_label: "이름 또는 설명을 필터링할 수 있습니다."
  new_item: "새로운 그룹"
  headers:
    slug: "슬러그"
    name: "이름"
    description: "설명"
    created_at: "생성일"
    updated_at: "수정일"
    actions: "관리"
  loading: "불러오는중 입니다... 잠시만 기다려 주세요."
  empty_items: "그룹이 존재하지 않습니다."
</i18n>

<template>
  <v-container>
    <toolbar-navigation :items="navigationItems"></toolbar-navigation>
    <v-divider></v-divider>

    <v-data-table
        class="row-pointer"
        :headers="headers"
        :items="users"
        :search="filterText"
        :loading="showLoading"
        :loading-text="$t('loading')"
        @click:row="onClickRow"
    >

      <template v-slot:top>
        <v-toolbar flat>

          <v-text-field
              class="mr-4"
              v-model="filterText"
              append-icon="mdi-magnify"
              single-line
              hide-details
              :label="$t('search_label')"
          ></v-text-field>

          <v-btn color="primary" @click="onClickNewGroup">
            {{ $t('new_group') }}
          </v-btn>

        </v-toolbar>
      </template>

      <template v-slot:item.created_at="{ item }">
        {{ utcToDate(item.created_at) }}
      </template>

      <template v-slot:item.updated_at="{ item }">
        {{ utcToDate(item.updated_at) }}
      </template>

      <template v-slot:no-data>
        {{ $t('empty_group') }}
      </template>

    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ToolbarNavigation from '@/components/ToolbarNavigation.vue';

@Component({
  components: {
    ToolbarNavigation,
  }
})
export default class MainGroups extends VueBase {
  private readonly navigationItems = [
    {
      text: 'Groups',
      disabled: true,
    },
  ];

  private readonly headers = [
    {
      text: this.$t('headers.slug').toString(),
      align: 'left',
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
  users: object = [];
  showLoading = true;

  mounted() {
    this.$api2.getSelfGroups()
        .then(response => {
          console.info(response);
          this.users = response;
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

  onClickRow(item) {
  }

  onClickNewGroup() {
    // this.moveToMainGroupsNew();
  }
}
</script>

<style lang="scss" scoped>
.row-pointer::v-deep tr {
  cursor: pointer;
}
</style>
