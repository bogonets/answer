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
  <div class="grid-view" ref="view">
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

    <div class="grid-view--table" ref="table">
      <div class="grid-view--header" ref="header">
        <div class="grid-view--header-row">
          <div class="grid-view--header-drag"></div>

          <div class="grid-view--header-index">
            {{ $t('header.id') }}
          </div>

          <template v-for="header in headers">
            <div
                class="grid-view--header-data" :key="`${header}-data`"
                @mousedown="onMouseDownHeader($event, header)"
            >
              {{ header }}
            </div>

            <div :key="`${header}-divider`">
            </div>
          </template>

          <div class="grid-view--header-add">
            <v-btn plain icon small @click="onClickAddHeader">
              <v-icon small>mdi-plus</v-icon>
            </v-btn>
          </div>
        </div>
      </div>

      <div class="grid-view--body" ref="body">
        <div
            class="grid-view--body-row"
            v-for="item in items"
            :key="item.id"
            @mouseenter="onEnterRowItem($event, item)"
            @mouseleave="onLeaveRowItem($event, item)"
        >
          <div class="grid-view--body-drag">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="8 0 8 24"
                role="img"
                aria-hidden="true"
            >
              <path :d="icons.dragVertical"></path>
            </svg>
          </div>

          <div class="grid-view--body-index">
            {{ item.id }}
          </div>

          <div
              class="grid-view--body-data"
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
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {mdiDragVertical} from '@mdi/js';

@Component
export default class GridView extends VueBase {
  readonly icons = {
    dragVertical: mdiDragVertical
  };

  @Ref('table')
  readonly tableElement!: HTMLDivElement;

  @Ref('view')
  readonly viewElement!: HTMLDivElement;

  @Ref('header')
  readonly headerElement!: HTMLDivElement;

  @Ref('body')
  readonly bodyElement!: HTMLDivElement;

  headers = ["name", "sport"];
  items = [
    { id: 1, name: "Abby", sport: "basket" },
    { id: 2, name: "Brooke", sport: "foot" },
    { id: 3, name: "Courtenay", sport: "volley" },
    { id: 4, name: "David", sport: "rugby" }
  ];

  draggingHeader = '';
  cursorElement?: HTMLDivElement;
  cursorId = -1;

  getHeaderRowElement() {
    return this.headerElement.getElementsByClassName('grid-view--header-row')[0];
  }

  getHeaderDataElement(header: string) {
    const index = this.headers.indexOf(header);
    const headerRow = this.getHeaderRowElement()
    return headerRow.getElementsByClassName('grid-view--header-data')[index];
  }

  getBodyRowElements() {
    return this.bodyElement.getElementsByClassName('grid-view--body-row');
  }

  getLastRowElement() {
    if (this.items.length == 0) {
      return this.getHeaderRowElement();
    }
    return this.getBodyRowElements()[this.items.length - 1];
  }

  getColumnRect(header: string) {
    const element = this.getHeaderDataElement(header);
    if (!element) {
      throw Error('Not found header element');
    }

    this.draggingHeader = header;
    document.addEventListener('mousemove', this.onMouseMove);
    document.addEventListener('mouseup', this.onMouseUp);

    const elementRect = element.getBoundingClientRect();
    const tableRect = this.tableElement.getBoundingClientRect();
    const viewRect = this.viewElement.getBoundingClientRect();
    const lastRect = this.getLastRowElement().getBoundingClientRect();

    const x = elementRect.x - viewRect.x;
    const y = elementRect.y - viewRect.y;
    const width = elementRect.width;
    const height = lastRect.bottom - tableRect.top;
    return {x, y, width, height};
  }

  onMouseDownHeader(event: MouseEvent, header: string) {
    this.draggingHeader = header;
    document.addEventListener('mousemove', this.onMouseMove);
    document.addEventListener('mouseup', this.onMouseUp);

    const rect = this.getColumnRect(header)
    this.cursorElement = document.createElement('div');
    this.cursorElement.style.position = 'absolute';
    this.cursorElement.style.left = `${rect.x}px`;
    this.cursorElement.style.top = `${rect.y}px`;
    this.cursorElement.style.width = `${rect.width}px`;
    this.cursorElement.style.height = `${rect.height}px`;
    this.cursorElement.style.background = `#55000022`;

    this.viewElement.insertBefore(this.cursorElement, this.tableElement);
  }

  onMouseDownBodyDrag(event: MouseEvent, item) {
  }

  onMouseMove() {
  }

  onMouseUp() {
    this.draggingHeader = '';
    document.removeEventListener('mousemove', this.onMouseMove);
    document.removeEventListener('mouseup', this.onMouseUp);
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
    // this.cursorId = item.id;
  }

  onLeaveRowItem(event, item) {
    // this.cursorId = -1;
  }

  onClickCell(item) {
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

$color-grey: map-get($colors, 'grey');
$color-grey-base: map-get($color-grey, 'base');
$color-grey-lighten-5: map-get($color-grey, 'lighten-5');
$color-grey-lighten-4: map-get($color-grey, 'lighten-4');
$color-grey-lighten-3: map-get($color-grey, 'lighten-3');
$color-grey-lighten-2: map-get($color-grey, 'lighten-2');
$color-grey-lighten-1: map-get($color-grey, 'lighten-1');
$color-grey-darken-1: map-get($color-grey, 'darken-1');
$color-grey-darken-2: map-get($color-grey, 'darken-2');
$color-grey-darken-3: map-get($color-grey, 'darken-3');
$color-grey-darken-4: map-get($color-grey, 'darken-4');

$light-background: map-get($material-light, 'background');
$light-color: map-deep-get($material-light, 'text', 'secondary');

$dark-background: map-get($material-dark, 'background');
$dark-color: map-deep-get($material-dark, 'text', 'secondary');

@mixin get-text-style($name) {
  font-size: map-deep-get($headings, $name, 'size') !important;
  font-weight: map-deep-get($headings, $name, 'weight');
  line-height: map-deep-get($headings, $name, 'line-height');
  letter-spacing: map-deep-get($headings, $name, 'letter-spacing') !important;
  font-family: map-deep-get($headings, $name, 'font-family') !important;
}

@mixin text-subtitle-2 {
  @include get-text-style('subtitle-2');
}

@mixin text-body-2 {
  @include get-text-style('body-2');
}

@mixin font-bold {
  font-weight: map-get($font-weights, 'bold');
}

.theme--light.v-application {
  .grid-view {
    background: $light-background;
    color: $light-color;

    .grid-view--header {
      background: $color-grey-lighten-4;
    }
  }

  .outline {
    border-color: $color-grey-lighten-2;
  }
}

.theme--dark.v-application {
  .grid-view {
    background: $dark-background;
    color: $dark-color;

    .grid-view--header {
      background: $color-grey-darken-4;
    }
  }

  .outline {
    border-color: $color-grey-darken-2;
  }
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

@mixin cell-drag-aligning {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-content: center;
  justify-content: center;
  align-items: center;
}

@mixin cell-index-aligning {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-content: center;
  justify-content: flex-end;
  align-items: center;
}

@mixin cell-data-aligning {
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
      @include text-subtitle-2;

      .grid-view--header-row {
        @include flex-row;

        .grid-view--header-drag {
          @include drag-vertical-sizing;
          @include cell-drag-aligning;
          @include cell-outline-drag;
        }

        .grid-view--header-index {
          @include cell-index-sizing;
          @include cell-index-aligning;
          @include cell-outline;
        }

        .grid-view--header-data {
          @include cell-data-sizing;
          @include cell-data-aligning;
          @include cell-outline;
        }

        .grid-view--header-add {
          @include cell-data-aligning;
        }
      }
    }

    .grid-view--body {
      @include flex-column;
      @include text-body-2;

      .grid-view--body-row {
        @include flex-row;

        .grid-view--body-drag {
          @include drag-vertical-sizing;
          @include drag-vertical-coloring;
          @include cell-drag-aligning;
          @include cell-outline-drag;

          //cursor: grab;
          //cursor: -webkit-grab;
          //cursor:-moz-grab;
        }

        .grid-view--body-index {
          @include cell-index-sizing;
          @include cell-index-aligning;
          @include cell-outline;
        }

        .grid-view--body-data {
          @include cell-data-sizing;
          @include cell-data-aligning;
          @include cell-outline;
        }

        .grid-view--body-add {
          @include cell-data-aligning;
        }
      }
    }
  }

  .grid-view--footer {
  }
}

.grid-view .grid-view--table .grid-view--body .grid-view--body-row {
  .grid-view--body-drag {
    svg {
      visibility: hidden;
    }
  }
}

.grid-view .grid-view--table .grid-view--body .grid-view--body-row:hover {
  .grid-view--body-drag {
    svg {
      visibility: visible;
    }
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
