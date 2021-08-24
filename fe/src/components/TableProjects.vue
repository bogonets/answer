<i18n lang="yaml">
en:
  label:
    search: "You can filter by name or description."
    new: "New Project"
  headers:
    group_slug: "Group slug"
    project_slug: "Project slug"
    name: "Name"
    description: "Description"
    created_at: "Created at"
    updated_at: "Updated at"
    actions: "Actions"
  msg:
    loading: "Loading... Please wait"
    empty: "Empty Projects"

ko:
  label:
    search: "이름 또는 설명을 필터링할 수 있습니다."
    new: "새로운 프로젝트"
  headers:
    group_slug: "그룹 슬러그"
    project_slug: "프로젝트 슬러그"
    name: "이름"
    description: "설명"
    created_at: "생성일"
    updated_at: "수정일"
    actions: "관리"
  msg:
    loading: "불러오는중 입니다... 잠시만 기다려 주세요."
    empty: "프로젝트가 존재하지 않습니다."
</i18n>

<template>
  <v-data-table
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

    <template v-slot:item.created_at="{ item }">
      {{ utcToDate(item.created_at) }}
    </template>

    <template v-slot:item.updated_at="{ item }">
      {{ utcToDate(item.updated_at) }}
    </template>

    <template v-if="!hideActions" v-slot:item.actions="{ item }">
      <v-icon v-if="!hideActionEdit" small class="mr-2" @click="clickEdit(item)">
        mdi-pencil
      </v-icon>
      <v-icon v-if="!hideActionMove" small class="mr-2" @click="clickMove(item)">
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
import {ProjectA} from '@/packet/project';

const REQUEST_TYPE_SELF = 'self';
const REQUEST_TYPE_ADMIN = 'admin';

@Component
export default class TableProjects extends VueBase {
  @Prop({type: String, default: REQUEST_TYPE_SELF})
  readonly requestType!: string;

  @Prop({type: Boolean, default: false})
  readonly hideToast!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideFilterInput!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideNewItemButton!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionEdit!: boolean;

  @Prop({type: Boolean, default: false})
  readonly hideActionMove!: boolean;

  @Prop({type: Boolean, default: false})
  readonly clickableRow!: boolean;

  headers = [] as Array<object>;
  loading = false;
  filter = '';
  items = [] as Array<ProjectA>;

  created() {
    this.requestItems();

    if (this.hideActions) {
      this.headers = this.createHeaders(false);
    } else {
      this.headers = this.createHeaders(true);
    }
  }

  get hideTopBar(): boolean {
    return this.hideFilterInput && this.hideNewItemButton;
  }

  get hideActions(): boolean {
    return this.hideActionEdit && this.hideActionMove;
  }

  createHeaders(includeActions = true) {
    const headers = [
      {
        text: this.$t('headers.group_slug').toString(),
        align: 'left',
        filterable: true,
        sortable: true,
        value: 'group_slug',
      },
      {
        text: this.$t('headers.project_slug').toString(),
        align: 'left',
        filterable: true,
        sortable: true,
        value: 'project_slug',
      },
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
        text: this.$t('headers.created_at').toString(),
        align: 'center',
        filterable: false,
        sortable: true,
        value: 'created_at',
      },
      {
        text: this.$t('headers.updated_at').toString(),
        align: 'center',
        filterable: false,
        sortable: true,
        value: 'updated_at',
      },
    ];
    if (includeActions) {
      headers.push({
        text: this.$t('headers.actions').toString(),
        align: 'center',
        filterable: false,
        sortable: false,
        value: 'actions',
      })
    }
    return headers;
  }

  requestItems() {
    if (this.requestType === REQUEST_TYPE_SELF) {
      this.requestSelfProjects();
    } else if (this.requestType === REQUEST_TYPE_ADMIN) {
      this.requestAdminProjects();
    } else {
      throw Error(`Unknown request type: ${this.requestType}`);
    }
  }

  requestSelfProjects() {
    this.$api2.getMainProjects()
        .then(items => {
          this.onRequestSuccess(items);
        })
        .catch(error => {
          this.onRequestFailure(error);
        });
  }

  requestAdminProjects() {
    this.loading = true;
    this.$api2.getAdminProjects()
        .then(items => {
          this.onRequestSuccess(items);
        })
        .catch(error => {
          this.onRequestFailure(error);
        });
  }

  onRequestSuccess(items: Array<ProjectA>) {
    this.loading = false;
    this.items = items;
  }

  onRequestFailure(error) {
    this.loading = false;
    if (this.hideToast) {
      this.toastRequestFailure(error);
    }
  }

  get dataTableClass(): string {
    if (this.clickableRow) {
      return 'row-pointer';
    } else {
      return '';
    }
  }

  utcToDate(utc: undefined | string): string {
    return utc?.split('T')[0] || '';
  }

  @Emit('click:new')
  clickNew() {
    // EMPTY.
  }

  @Emit('click:row')
  clickRow(item: ProjectA) {
    return item;
  }

  @Emit('click:edit')
  clickEdit(item: ProjectA) {
    return item;
  }

  @Emit('click:move')
  clickMove(item: ProjectA) {
    return item;
  }

  onClickRow(item: ProjectA) {
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