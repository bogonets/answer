<i18n lang="yaml">
en:
  tools:
    tables: "Tables"
    views: "Views"
    filter: "Filter"
    sort: "Sort"
    hide: "Hide Fields"

ko:
  tools:
    tables: "테이블"
    views: "뷰"
    filter: "필터"
    sort: "정렬"
    hide: "숨김"
</i18n>

<template>
  <div class="main-table">
    <v-toolbar dense flat>
      <v-btn plain small @click="onClickView">
        <v-icon left>
          mdi-table
        </v-icon>
        {{ $t('tools.tables') }}
      </v-btn>

      <v-btn plain small @click="onClickView">
        <v-icon left>
          mdi-view-grid
        </v-icon>
        {{ $t('tools.views') }}
      </v-btn>

      <v-btn plain small @click="onClickFilter">
        <v-icon left>
          mdi-filter
        </v-icon>
        {{ $t('tools.filter') }}
      </v-btn>

      <v-btn plain small @click="onClickSort">
        <v-icon left>
          mdi-sort
        </v-icon>
        {{ $t('tools.sort') }}
      </v-btn>

      <v-btn plain small @click="onClickHide">
        <v-icon left>
          mdi-eye-off
        </v-icon>
        {{ $t('tools.hide') }}
      </v-btn>

      <v-btn icon plain small @click="onClickMore">
        <v-icon>
          mdi-dots-horizontal
        </v-icon>
      </v-btn>
    </v-toolbar>
    <v-divider></v-divider>

    <grid-view>
    </grid-view>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import GridView from '@/components/DynamicTable/GridView.vue';

const NAVIGATION_DENSE_HEIGHT = 48;
const DIVIDER_HEIGHT = 1;
const VIEW_PORT_MARGIN_TOP = (NAVIGATION_DENSE_HEIGHT * 2) + DIVIDER_HEIGHT;

@Component({
  components: {
    GridView,
  }
})
export default class MainTables extends VueBase {
  private readonly viewPortMarginTop = VIEW_PORT_MARGIN_TOP;

  onClickView() {
  }

  onClickFilter() {
  }

  onClickSort() {
  }

  onClickHide() {
  }

  onClickMore() {
  }
}
</script>

<style lang="scss" scoped>
.main-table {
}
</style>
