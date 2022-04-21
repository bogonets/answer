<i18n lang="yaml">
en:
  labels:
    new: 'Add Event'
    delete: 'Delete a Event'
    search: 'You can filter by name'
  headers:
    enable: 'Enable'
    category: 'Category'
    name: 'Name'
    modified: 'Modified at'
    actions: 'Actions'
  category:
    color: 'Color'
    detection: 'Detection'
    matching: 'Matching'
    ocr: 'OCR'
    unknown: 'Unknown'
  msg:
    loading: 'Loading... Please wait'
    empty: 'Empty Events'
    delete_confirm: 'Are you really removing this event?'
  cancel: 'Cancel'
  submit: 'Submit'
  delete: 'Delete'

ko:
  labels:
    new: '이벤트 추가'
    delete: '이벤트 제거'
    search: '이름을 필터링할 수 있습니다'
  headers:
    enable: '활성화'
    category: '종류'
    name: '이름'
    modified: '수정일'
    actions: '관리'
  category:
    color: '색상 비교'
    detection: '객체 탐지'
    matching: '영상 비교'
    ocr: '문자 인식'
    unknown: '알 수 없음'
  msg:
    loading: '불러오는중 입니다... 잠시만 기다려 주세요.'
    empty: '이벤트가 존재하지 않습니다.'
    delete_confirm: '이 이벤트를 정말 제거합니까?'
  cancel: '취소'
  submit: '제출'
  delete: '제거'
</i18n>

<template>
  <v-data-table
    sort-desc
    sort-by="name"
    :class="dataTableClass"
    :items-per-page="itemsPerPage"
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
          :label="$t('labels.search')"
        ></v-text-field>
        <v-btn v-if="!hideNewItemButton" color="primary" @click="clickNew">
          {{ $t('labels.new') }}
        </v-btn>
      </v-toolbar>
    </template>

    <template v-slot:item.enable="{item}">
      <v-btn icon @click="clickActive(item)">
        <v-icon>{{ enableIcon(item) }}</v-icon>
      </v-btn>
    </template>

    <template v-slot:item.category="{item}">
      <v-chip>
        <v-icon left>{{ categoryIcon(item) }}</v-icon>
        {{ categoryText(item) }}
      </v-chip>
    </template>

    <template v-slot:item.modified="{item}">
      {{ modifiedDate(item) }}
    </template>

    <template v-if="!hideActions" v-slot:item.actions="{item}">
      <v-icon v-if="!hideActionEdit" small @click="clickEdit(item)">mdi-pencil</v-icon>
      <v-icon
        v-if="!hideActionDelete"
        class="ml-2"
        color="error"
        small
        @click="clickDelete(item)"
      >
        mdi-delete
      </v-icon>
    </template>

    <template v-slot:no-data>
      {{ $t('msg.empty') }}
    </template>
  </v-data-table>
</template>

<script lang="ts">
import {Component, Emit, Prop, Watch} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {updatedOrCreated} from '@/chrono/iso8601';
import type {DataTableHeader} from '@/hints/vuetify';
import type {VmsEventConfigA} from '@/packet/vms';
import {
  EVENT_CATEGORY_NAME_COLOR,
  EVENT_CATEGORY_NAME_DETECTION,
  EVENT_CATEGORY_NAME_MATCHING,
  EVENT_CATEGORY_NAME_OCR,
} from '@/packet/vms';

@Component
export default class TableVmsEventConfigs extends VueBase {
  readonly categories = [
    {
      icon: 'mdi-palette',
      text: this.$t('category.color'),
      value: EVENT_CATEGORY_NAME_COLOR,
    },
    {
      icon: 'mdi-image-search',
      text: this.$t('category.detection'),
      value: EVENT_CATEGORY_NAME_DETECTION,
    },
    {
      icon: 'mdi-compare',
      text: this.$t('category.matching'),
      value: EVENT_CATEGORY_NAME_MATCHING,
    },
    {
      icon: 'mdi-ocr',
      text: this.$t('category.ocr'),
      value: EVENT_CATEGORY_NAME_OCR,
    },
  ];

  @Prop({type: Number, default: 15})
  readonly itemsPerPage!: number;

  @Prop({type: Boolean, default: false})
  readonly hideFilterInput!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideNewItemButton!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionEdit!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionDelete!: boolean;

  @Prop({type: Boolean, default: false})
  readonly clickableRow!: boolean;

  @Prop({type: Boolean, default: false})
  readonly loading!: boolean;

  @Prop({type: Array, default: () => []})
  readonly items!: Array<VmsEventConfigA>;

  headers = [] as Array<DataTableHeader>;
  filter = '';

  created() {
    this.headers = this.createHeaders();
  }

  @Watch('items', {deep: true})
  watchItems() {
    // EMPTY.
  }

  createHeaders() {
    const headers = [
      {
        text: this.$t('headers.enable').toString(),
        align: 'center',
        filterable: false,
        sortable: false,
        width: '80px',
        value: 'enable',
      },
      {
        text: this.$t('headers.category').toString(),
        align: 'center',
        filterable: true,
        sortable: true,
        value: 'category',
      },
      {
        text: this.$t('headers.name').toString(),
        align: 'center',
        filterable: true,
        sortable: true,
        value: 'name',
      },
      {
        text: this.$t('headers.modified').toString(),
        align: 'center',
        filterable: false,
        sortable: true,
        value: 'modified',
      },
    ] as Array<DataTableHeader>;

    if (!this.hideActions) {
      headers.push({
        text: this.$t('headers.actions').toString(),
        align: 'center',
        filterable: false,
        sortable: false,
        width: '84px',
        value: 'actions',
      });
    }
    return headers;
  }

  get hideTopBar() {
    return this.hideFilterInput && this.hideNewItemButton;
  }

  get hideActions() {
    return this.hideActionEdit && this.hideActionDelete;
  }

  get dataTableClass() {
    if (this.items.length >= 1 && this.clickableRow) {
      return 'row-pointer';
    } else {
      return '';
    }
  }

  modifiedDate(item: VmsEventConfigA) {
    return updatedOrCreated(item.updated_at, item.created_at);
  }

  enableIcon(item: VmsEventConfigA) {
    if (item.enable) {
      return 'mdi-checkbox-marked';
    } else {
      return 'mdi-checkbox-blank-outline';
    }
  }

  categoryIcon(item: VmsEventConfigA) {
    const findCategory = this.categories.find(i => i.value == item.category);
    if (typeof findCategory === 'undefined') {
      return '';
    }
    return findCategory.icon;
  }

  categoryText(item: VmsEventConfigA) {
    const findCategory = this.categories.find(i => i.value == item.category);
    if (typeof findCategory === 'undefined') {
      return this.$t('category.unknown').toString();
    }
    return findCategory.text;
  }

  onClickRow(item: VmsEventConfigA) {
    if (this.clickableRow) {
      this.clickRow(item);
    }
  }

  @Emit('click:active')
  clickActive(item: VmsEventConfigA) {
    return item;
  }

  @Emit('click:new')
  clickNew() {
    // EMPTY.
  }

  @Emit('click:row')
  clickRow(item: VmsEventConfigA) {
    return item;
  }

  @Emit('click:edit')
  clickEdit(item: VmsEventConfigA) {
    return item;
  }

  @Emit('click:delete')
  clickDelete(item: VmsEventConfigA) {
    return item;
  }
}
</script>

<style lang="scss" scoped>
.row-pointer::v-deep tr {
  cursor: pointer;
}
</style>
