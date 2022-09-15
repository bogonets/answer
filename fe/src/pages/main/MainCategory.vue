<i18n lang="yaml">
en:
  search_label: 'You can filter by id or name.'

ko:
  search_label: '아이디(ID) 또는 이름을 필터링할 수 있습니다.'
</i18n>

<template>
  <v-container>
    <v-data-table
      item-key="key"
      :items-per-page="itemsPerPage"
      :headers="headers"
      :items="items"
      :search="filter"
      :loading="loading"
    >
      <template v-slot:top>
        <div>
          <v-toolbar flat>
            <v-text-field
              class="mr-4"
              v-model="filter"
              append-icon="mdi-magnify"
              :label="$t('search_label')"
              single-line
              hide-details
            ></v-text-field>
          </v-toolbar>
        </div>
        <div class="d-flex flex-row align-center">
          <v-text-field
            label="새로운 카테고리"
            type="text"
            filled
            rounded
            dense
            append-outer-icon="mdi-plus-circle"
            placeholder="새로운 카테고리 이름을 입력해 주세요."
          ></v-text-field>
        </div>
      </template>

      <template v-slot:item.color="{item}">
        <v-chip small :color="item.color">
          {{ item.color }}
        </v-chip>
      </template>

      <template v-slot:item.actions="{item}">
        <v-icon small disabled class="mr-2" @click="onClickContainerEdit(item)">
          mdi-pencil
        </v-icon>
        <v-icon small disabled class="mr-2" @click="onClickContainerEdit(item)">
          mdi-delete
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

const ITEMS_PER_PAGE = 15;

@Component
export default class MainCategory extends VueBase {
  readonly itemsPerPage = ITEMS_PER_PAGE;
  readonly headers = [
    {
      text: 'ID',
      align: 'center',
      filterable: true,
      sortable: true,
      width: '80px',
      value: 'id',
    },
    {
      text: '분류',
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'name',
    },
    {
      text: '상위 분류',
      align: 'center',
      filterable: true,
      sortable: true,
      value: 'super',
    },
    {
      text: '색상',
      align: 'center',
      filterable: false,
      sortable: true,
      width: '100px',
      value: 'color',
    },
    {
      text: '관리',
      align: 'center',
      filterable: false,
      sortable: false,
      width: '80px',
      value: 'actions',
    },
  ];

  loading = false;
  filter = '';
  items = [
    {
      id: '0',
      name: 'Fire',
      super: 'Fire',
      color: '#FF0000',
    },
    {
      id: '1',
      name: 'Smoke',
      super: 'Fire',
      color: '#808080',
    },
    {
      id: '2',
      name: 'Car',
      super: undefined,
      color: '#E1E1E1',
    },
    {
      id: '3',
      name: 'Bus',
      super: 'Car',
      color: '#8888FF',
    },
    {
      id: '4',
      name: 'Truck',
      super: 'Car',
      color: '#FFBB11',
    },
  ];

  shortKey(item) {
    return item.key.substring(0, 12);
  }

  statusColor(item) {
    return item.color;
  }

  onClickContainerEdit(item) {}
}
</script>
