<i18n lang="yaml">
en:
  label:
    search: 'You can filter by name or description.'
    new: 'New Group'
  headers:
    slug: 'Slug'
    name: 'Name'
    description: 'Description'
    created_at: 'Created at'
    updated_at: 'Updated at'
    actions: 'Actions'
  msg:
    loading: 'Loading... Please wait'
    empty: 'Empty Groups'

ko:
  label:
    search: '이름 또는 설명을 필터링할 수 있습니다.'
    new: '새로운 그룹'
  headers:
    slug: '슬러그'
    name: '이름'
    description: '설명'
    created_at: '생성일'
    updated_at: '수정일'
    actions: '관리'
  msg:
    loading: '불러오는중 입니다... 잠시만 기다려 주세요.'
    empty: '그룹이 존재하지 않습니다.'
</i18n>

<template>
  <v-data-table
    sort-desc
    sort-by="name"
    :class="dataTableClass"
    :headers="headers"
    :items="items"
    :search="filter"
    :loading="loading"
    :loading-text="$t('msg.loading')"
    @click:row="onClickRow"
  >
    <template v-if="!hideTopBar" v-slot:top>
      <v-toolbar flat>
        <v-text-field
          v-if="!hideFilterInput"
          class="mr-4"
          v-model="filter"
          append-icon="mdi-magnify"
          single-line
          hide-details
          :label="$t('label.search')"
        ></v-text-field>
        <v-btn v-if="!hideNewItemButton" color="primary" @click="clickNew">
          {{ $t('label.new') }}
        </v-btn>
      </v-toolbar>
    </template>

    <template v-slot:item.name="{item}">
      {{ item.name }}
      <v-chip class="ml-2" x-small outlined color="primary">
        <v-icon left>mdi-identifier</v-icon>
        {{ item.slug }}
      </v-chip>
    </template>

    <template v-slot:item.updated_at="{item}">
      {{ datetimeToDate(item.created_at, item.updated_at) }}
    </template>

    <template v-if="!hideActions" v-slot:item.actions="{item}">
      <v-icon v-if="!hideActionEdit" small @click="clickEdit(item)">mdi-pencil</v-icon>
      <v-icon v-if="!hideActionMove" small class="ml-2" @click="clickMove(item)">
        mdi-exit-to-app
      </v-icon>
    </template>

    <template v-slot:no-data>
      {{ $t('msg.empty') }}
    </template>
  </v-data-table>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import type {GroupA} from '@recc/api/dist/packet/group';
import {iso8601ToLocalDate} from '@/chrono/iso8601';

@Component
export default class TableGroups extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly hideFilterInput!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideNewItemButton!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionEdit!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionMove!: boolean;

  @Prop({type: Boolean, default: false})
  readonly showGroupSlug!: boolean;

  @Prop({type: Boolean, default: false})
  readonly clickableRow!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: Array, default: () => new Array<GroupA>()})
  readonly items!: Array<GroupA>;

  headers = [] as Array<object>;
  filter = '';

  created() {
    this.headers = this.createHeaders();
  }

  get hideTopBar(): boolean {
    return this.hideFilterInput && this.hideNewItemButton;
  }

  get hideActions(): boolean {
    return this.hideActionEdit && this.hideActionMove;
  }

  createHeaders() {
    const headers = [] as Array<any>;
    if (this.showGroupSlug) {
      headers.push({
        text: this.$t('headers.slug').toString(),
        align: 'left',
        filterable: true,
        sortable: true,
        value: 'slug',
      });
    }

    headers.push(
      {
        text: this.$t('headers.name').toString(),
        align: 'center',
        filterable: true,
        sortable: true,
        value: 'name',
      },
      {
        text: this.$t('headers.description').toString(),
        align: 'center',
        filterable: true,
        sortable: true,
        value: 'description',
      },
      {
        text: this.$t('headers.updated_at').toString(),
        align: 'center',
        filterable: false,
        sortable: true,
        value: 'updated_at',
      },
    );

    if (!this.hideActions) {
      headers.push({
        text: this.$t('headers.actions').toString(),
        align: 'center',
        filterable: false,
        sortable: false,
        value: 'actions',
        width: '84px',
      });
    }
    return headers;
  }

  get dataTableClass() {
    if (this.items.length >= 1 && this.clickableRow) {
      return 'row-pointer';
    } else {
      return '';
    }
  }

  datetimeToDate(createdAt?: string, updatedAt?: string) {
    if (updatedAt) {
      return iso8601ToLocalDate(updatedAt);
    }
    if (createdAt) {
      return iso8601ToLocalDate(createdAt);
    }
    return '';
  }

  @Emit('click:new')
  clickNew() {
    // EMPTY.
  }

  @Emit('click:row')
  clickRow(item: GroupA) {
    return item;
  }

  @Emit('click:edit')
  clickEdit(item: GroupA) {
    return item;
  }

  @Emit('click:move')
  clickMove(item: GroupA) {
    return item;
  }

  onClickRow(item: GroupA) {
    if (this.clickableRow) {
      this.clickRow(item);
    }
  }
}
</script>

<style lang="scss" scoped>
.row-pointer::v-deep tr {
  cursor: pointer;
}
</style>
