<i18n lang="yaml">
en:
  tools:
    tables: "Tables"
    views: "Views"
    filter: "Filter"
    sort: "Sort"
    hide: "Hide Fields"
  header:
    id: "#"

ko:
  tools:
    tables: "테이블"
    views: "뷰"
    filter: "필터"
    sort: "정렬"
    hide: "숨김"
  header:
    id: "#"
</i18n>

<template>
  <div class="grid-view">
    <div class="grid-view--toolbar">
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
    </div>

    <div class="grid-view--table">
      <div class="grid-view--table-header" :class="gridViewTableHeaderClass">
        <div class="grid-view--table-header-row">
          <div
              class="grid-view--table-header-row-drag"
              :class="gridViewTableDragClass"
          ></div>

          <div
              class="grid-view--table-header-row-index"
              :class="gridViewTableHeaderRowDataClass"
          >
            {{ $t('header.id') }}
          </div>

          <template v-for="header in headers">
            <div
                class="grid-view--table-header-row-data"
                :class="gridViewTableHeaderRowDataClass"
                :key="`${header}-data`"
            >
              {{ header }}
            </div>

            <div :key="`${header}-divider`">
              <v-divider vertical></v-divider>
            </div>
          </template>

          <div class="grid-view--table-header-row-add">
            <v-btn plain icon small @click="onClickAddHeader">
              <v-icon small>mdi-plus</v-icon>
            </v-btn>
          </div>
        </div>
      </div>

      <div class="grid-view--table-body" :class="gridViewTableBodyClass">
        <div
            class="grid-view--table-body-row"
            v-for="item in items"
            :key="item.id"
            @mouseenter="onEnterRowItem($event, item)"
            @mouseleave="onLeaveRowItem($event, item)"
        >
          <div
              class="grid-view--table-body-row-drag"
              :class="gridViewTableDragClass"
          >
            <svg
                v-show="isShowDragIcon(item)"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="8 0 8 24"
                role="img"
                aria-hidden="true"
            >
              <path :d="icons.dragVertical"></path>
            </svg>
          </div>

          <div
              class="grid-view--table-body-row-index"
              :class="gridViewTableBodyRowDataClass"
          >
            {{ item.id }}
          </div>

          <div
              class="grid-view--table-body-row-data"
              :class="gridViewTableBodyRowDataClass"
              v-for="header in headers"
              :key="header"
              @click="onClickCell(item)"
          >
            {{ item[header] }}
          </div>
        </div>

        <div class="grid-view--table-body-row">
          <div class="grid-view--table-body-row-add">
            <v-btn plain icon small @click="onClickAddItem">
              <v-icon small>mdi-plus</v-icon>
            </v-btn>
          </div>
        </div>
      </div>
    </div>

    <div class="grid-view--footer">
    </div>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {mdiDragVertical} from '@mdi/js';

@Component
export default class GridView extends VueBase {
  readonly icons = {
    dragVertical: mdiDragVertical
  };

  headers = ["name", "sport"];
  items = [
    { id: 1, name: "Abby", sport: "basket" },
    { id: 2, name: "Brooke", sport: "foot" },
    { id: 3, name: "Courtenay", sport: "volley" },
    { id: 4, name: "David", sport: "rugby" }
  ];
  dragging = false;

  cursorId = -1;

  get brightness() {
    if (this.$vuetify.theme.dark) {
      return 'darken';
    } else {
      return 'lighten';
    }
  }

  get backgroundHeaderClass() {
    return ['grey', `${this.brightness}-4`].join(' ');
  }

  get outlineClass() {
    return `outline-grey-${this.brightness}`;
  }

  get outlineDragClass() {
    return `outline-drag-grey-${this.brightness}`;
  }

  get gridViewTableHeaderClass() {
    return [
      this.backgroundHeaderClass,
      'text-subtitle-2',
      'text--secondary',
    ].join(' ');
  }

  get gridViewTableBodyClass() {
    return [
      'text-body-2',
      'text--secondary',
    ].join(' ');
  }

  get gridViewTableDragClass() {
    return [
      this.outlineDragClass
    ].join(' ');
  }

  get gridViewTableHeaderRowDataClass() {
    return [
        this.outlineClass
    ].join(' ');
  }

  get gridViewTableBodyRowDataClass() {
    return [
      this.outlineClass
    ].join(' ');
  }

  isShowDragIcon(item) {
    return item.id == this.cursorId;
  }

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

  onClickAddHeader() {
  }

  onClickAddItem() {
  }

  onEnterRowItem(event, item) {
    this.cursorId = item.id;
  }

  onLeaveRowItem(event, item) {
    this.cursorId = -1;
  }

  onClickCell(item) {
  }
}
</script>

<style lang="scss" scoped>
$color-grey-lighten-4: '#F5F5F5';
$color-grey-lighten-3: '#EEEEEE';
$color-grey-lighten-2: '#E0E0E0';
$color-grey-lighten-1: '#BDBDBD';
$color-grey-darken-1: '#757575';
$color-grey-darken-2: '#616161';
$color-grey-darken-3: '#424242';
$color-grey-darken-4: '#212121';

@mixin cell-outline-drag {
  border-top-width: 0;
  border-bottom-width: 1px;
  border-bottom-style: solid;
}

@mixin cell-outline {
  border-left-width: 0;
  border-top-width: 0;

  border-right-width: 1px;
  border-bottom-width: 1px;

  border-right-style: solid;
  border-bottom-style: solid;
}

.outline-drag-grey-darken {
  @include cell-outline-drag;
  border-color: $color-grey-darken-3;
}

.outline-drag-grey-lighten {
  @include cell-outline-drag;
  border-color: $color-grey-lighten-3;
}

.outline-grey-darken {
  @include cell-outline;
  border-color: $color-grey-darken-3;
}

.outline-grey-lighten {
  @include cell-outline;
  border-color: $color-grey-lighten-3;
}

@mixin flex-column {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
}

@mixin flex-row {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

@mixin field-drag-centering {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-content: center;
  justify-content: center;
  align-items: center;
}

@mixin field-index-centering {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-content: center;
  justify-content: center;
  align-items: center;
}

@mixin field-data-centering {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
}

@mixin field-index-sizing {
  padding: 0 8px;
  min-width: 32px;
  min-height: 32px;
}

@mixin field-data-sizing {
  padding: 0 10px;
  min-width: 100px;
  min-height: 32px;
}

@mixin drag-vertical-sizing {
  width: 10px;
  height: 32px;
}

@mixin drag-vertical-coloring {
  fill: currentColor;
}

.grid-view {
  @include flex-column;

  .grid-view--toolbar {
  }

  .grid-view--table {
    @include flex-column;

    .grid-view--table-header {
      @include flex-column;

      .grid-view--table-header-row {
        @include flex-row;

        .grid-view--table-header-row-drag {
          @include drag-vertical-sizing;
        }

        .grid-view--table-header-row-index {
          @include field-index-sizing;
          @include field-index-centering;
        }

        .grid-view--table-header-row-data {
          @include field-data-sizing;
          @include field-data-centering;
        }

        .grid-view--table-header-row-add {
        }
      }
    }

    .grid-view--table-body {
      @include flex-column;

      .grid-view--table-body-row {
        @include flex-row;

        .grid-view--table-body-row-drag {
          @include drag-vertical-sizing;
          @include drag-vertical-coloring;
          @include field-drag-centering;

          cursor: grab;
        }

        .grid-view--table-body-row-index {
          @include field-index-sizing;
          @include field-index-centering;
        }

        .grid-view--table-body-row-data {
          @include field-data-sizing;
          @include field-data-centering;
        }

        .grid-view--table-body-row-add {
        }
      }
    }
  }

  .grid-view--footer {
  }
}

//.flip-list-move {
//  transition: transform 0.5s;
//}
//
//.no-move {
//  transition: transform 0s;
//}
//
//.ghost {
//  opacity: 0.5;
//  background: #c8ebfb;
//}
//
//.list-group {
//  min-height: 20px;
//}
//
//.list-group-item {
//  cursor: move;
//}
//
//.list-group-item i {
//  cursor: pointer;
//}
</style>
