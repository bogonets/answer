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
      <div :class="gridViewHeaderClass">
        <div class="grid-view--header-row">
          <div :class="gridViewHeaderDragClass"></div>

          <div :class="gridViewHeaderIndexClass">
            {{ $t('header.id') }}
          </div>

          <template v-for="header in headers">
            <div :class="gridViewHeaderDataClass" :key="`${header}-data`">
              {{ header }}
            </div>

            <div :key="`${header}-divider`">
            </div>
          </template>

          <div :class="gridViewHeaderAddClass">
            <v-btn plain icon small @click="onClickAddHeader">
              <v-icon small>mdi-plus</v-icon>
            </v-btn>
          </div>
        </div>
      </div>

      <div :class="gridViewBodyClass">
        <div
            class="grid-view--body-row"
            v-for="item in items"
            :key="item.id"
            @mouseenter="onEnterRowItem($event, item)"
            @mouseleave="onLeaveRowItem($event, item)"
        >
          <div :class="gridViewBodyDragClass">
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

          <div :class="gridViewBodyIndexClass">
            {{ item.id }}
          </div>

          <div
              :class="gridViewBodyDataClass"
              v-for="header in headers"
              :key="header"
              @click="onClickCell(item)"
          >
            {{ item[header] }}
          </div>
        </div>

        <div class="grid-view--body-row">
          <div class="grid-view--body-add">
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

  // ------------
  // Header class
  // ------------

  get gridViewHeaderClass() {
    return [
      'grey',
      `${this.brightness}-4`,
      'grid-view--header',
      'text-subtitle-2',
      'text--secondary',
    ].join(' ');
  }

  get gridViewHeaderDragClass() {
    return [
      `outline-grey-${this.brightness}`,
      'grid-view--header-drag',
    ].join(' ');
  }

  get gridViewHeaderIndexClass() {
    return [
      `outline-grey-${this.brightness}`,
      'grid-view--header-index',
    ].join(' ');
  }

  get gridViewHeaderDataClass() {
    return [
      `outline-grey-${this.brightness}`,
      'grid-view--header-data',
    ].join(' ');
  }

  get gridViewHeaderAddClass() {
    return [
      `outline-grey-${this.brightness}`,
      'grid-view--header-add',
    ].join(' ');
  }

  // ----------
  // Body class
  // ----------

  get gridViewBodyClass() {
    return [
      'grid-view--body',
      'text-body-2',
      'text--secondary',
    ].join(' ');
  }

  get gridViewBodyDragClass() {
    return [
      `outline-grey-${this.brightness}`,
      'grid-view--body-drag',
    ].join(' ');
  }

  get gridViewBodyIndexClass() {
    return [
      `outline-grey-${this.brightness}`,
      'grid-view--body-index',
    ].join(' ');
  }

  get gridViewBodyDataClass() {
    return [
      `outline-grey-${this.brightness}`,
      'grid-view--body-data',
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

.outline-grey-darken {
  border-color: $color-grey-darken-2;
}

.outline-grey-lighten {
  border-color: $color-grey-lighten-2;
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

@mixin cell-drag-centering {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-content: center;
  justify-content: center;
  align-items: center;
}

@mixin cell-index-centering {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-content: center;
  justify-content: flex-end;
  align-items: center;
}

@mixin cell-data-centering {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
}

@mixin cell-index-sizing {
  padding: 0 8px;
  min-width: 40px;
  min-height: 32px;
}

@mixin cell-data-sizing {
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

    .grid-view--header {
      @include flex-column;

      .grid-view--header-row {
        @include flex-row;

        .grid-view--header-drag {
          @include drag-vertical-sizing;
          @include cell-drag-centering;
          @include cell-outline-drag;
        }

        .grid-view--header-index {
          @include cell-index-sizing;
          @include cell-index-centering;
          @include cell-outline;
        }

        .grid-view--header-data {
          @include cell-data-sizing;
          @include cell-data-centering;
          @include cell-outline;
        }

        .grid-view--header-add {
          @include cell-data-centering;
        }
      }
    }

    .grid-view--body {
      @include flex-column;

      .grid-view--body-row {
        @include flex-row;

        .grid-view--body-drag {
          @include drag-vertical-sizing;
          @include drag-vertical-coloring;
          @include cell-drag-centering;
          @include cell-outline-drag;

          cursor: grab;
        }

        .grid-view--body-index {
          @include cell-index-sizing;
          @include cell-index-centering;
          @include cell-outline;
        }

        .grid-view--body-data {
          @include cell-data-sizing;
          @include cell-data-centering;
          @include cell-outline;
        }

        .grid-view--body-add {
          @include cell-data-centering;
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
