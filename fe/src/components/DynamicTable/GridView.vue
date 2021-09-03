<i18n lang="yaml">
en:
  header:
    id: "#"

ko:
  header:
    id: "#"
</i18n>

<template>
  <div class="grid-view" ref="table">
    <div class="grid-view--header" ref="header">
      <div class="grid-view--header-row" ref="headerRow">
        <div class="grid-view--header-drag">
        </div>

        <div class="grid-view--header-index" ref="headerIndex">
          {{ $t('header.id') }}
        </div>

        <template v-for="[index, header] in headers.entries()">
          <div class="grid-view--header-data" :key="`${header}-data`">
            <div
                class="grid-view--header-data-content"
                @mousedown="onMouseDownColumn($event, index)"
            >
              {{ header }}
            </div>

            <div
                class="grid-view--header-data-resize"
                :key="`${header}-divider`"
                @mousedown="onMouseDownColumnResize($event, index)"
            >
            </div>
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
          v-for="[index, item] in items.entries()"
          :key="item.id"
      >
        <div
            class="grid-view--body-drag"
            @mousedown="onMouseDownRow($event, index)"
        >
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
        >
          {{ item[header] }}
        </div>
      </div>

      <div class="grid-view--body-add">
        <v-btn plain icon small @click="onClickAddItem">
          <v-icon small>mdi-plus</v-icon>
        </v-btn>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {mdiDragVertical} from '@mdi/js';

export const NO_INDEX = -1;
export const DEFAULT_MIN_WIDTH = 100;

export interface Rect {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Range {
  begin: number;
  end: number;
}

@Component
export default class GridView extends VueBase {
  readonly icons = {
    dragVertical: mdiDragVertical
  };

  @Ref('table')
  readonly tableElement!: HTMLDivElement;

  @Ref('header')
  readonly headerElement!: HTMLDivElement;

  @Ref('headerIndex')
  readonly headerIndexElement!: HTMLDivElement;

  @Ref('headerRow')
  readonly headerRowElement!: HTMLDivElement;

  @Ref('body')
  readonly bodyElement!: HTMLDivElement;

  headers = ['name', 'sport', 'rank'];

  sizes = {
    name: {
      width: 0,
      height: 0,
    },
    sport: {
      width: 200,
      height: 0,
    },
    rank: {
      width: 300,
      height: 0,
    },
  };

  items = [
    { id: 1, name: 'Abby', sport: 'basket', rank: 10 },
    { id: 2, name: 'Brooke', sport: 'foot', rank: 20 },
    { id: 3, name: 'Courtenay', sport: 'volley', rank: 30 },
    { id: 4, name: 'David', sport: 'rugby', rank: 40 }
  ];

  draggingCandidateIndex = NO_INDEX;
  draggingIndex = NO_INDEX;

  visibleRanges = [] as Array<Range>;

  ghostElement?: HTMLDivElement;
  lineElement?: HTMLDivElement;

  cursorX = 0;
  cursorY = 0;

  originalWidthOfResizeCandidate = 0;  // Used only for resize feature.

  mounted() {
    this.refreshTable();
  }

  refreshTable() {
    for (let i = 0; i < this.headers.length; ++i) {
      const header = this.headers[i];
      const size = this.sizes[header] ?? {width: 0, height: 0};
      this.resizeColumn(size.width, i);
    }
  }

  get headerDataElements() {
    return this.headerRowElement.getElementsByClassName('grid-view--header-data');
  }

  get bodyRowElements() {
    return this.bodyElement.getElementsByClassName('grid-view--body-row');
  }

  getHeaderDataElement(index: number) {
    return this.headerDataElements[index] as HTMLDivElement;
  }

  getBodyRowElement(index: number) {
    return this.bodyRowElements[index] as HTMLDivElement;
  }

  getBodyDataElement(rowIndex: number, columnIndex: number) {
    const row = this.getBodyRowElement(rowIndex);
    const data = row.getElementsByClassName('grid-view--body-data');
    return data[columnIndex] as HTMLDivElement;
  }

  getColumnElement(index: number) {
    if (index == 0) {
      return this.headerIndexElement;
    }
    return this.getHeaderDataElement(index - 1);
  }

  getRowElement(index: number) {
    if (index == 0) {
      return this.headerRowElement;
    } else {
      return this.getBodyRowElement(index - 1);
    }
  }

  getLastColumnElement() {
    return this.getColumnElement(this.headers.length);
  }

  getLastRowElement() {
    return this.getRowElement(this.items.length);
  }

  getColumnRect(index: number) {
    console.assert(this.headers.length > index && index >= 0);
    const element = this.getHeaderDataElement(index);

    const elementRect = element.getBoundingClientRect();
    const tableRect = this.tableElement.getBoundingClientRect();
    const lastRect = this.getLastRowElement().getBoundingClientRect();

    const x = elementRect.x - tableRect.x;
    const y = elementRect.y - tableRect.y;
    const width = elementRect.width;
    const height = lastRect.bottom - tableRect.top;
    return {x, y, width, height} as Rect;
  }

  getRowRect(index: number) {
    console.assert(this.items.length > index && index >= 0);
    const element = this.getBodyRowElement(index);

    const elementRect = element.getBoundingClientRect();
    const tableRect = this.tableElement.getBoundingClientRect();
    const lastRect = this.getLastColumnElement().getBoundingClientRect();

    const x = elementRect.x - tableRect.x;
    const y = elementRect.y - tableRect.y;
    const width = lastRect.right - tableRect.left;
    const height = elementRect.height;
    return {x, y, width, height} as Rect;
  }

  getColumnLineRect(lineIndex: number) {
    console.assert(this.headers.length >= lineIndex && lineIndex >= 0);
    const element = this.getColumnElement(lineIndex);

    const elementRect = element.getBoundingClientRect();
    const tableRect = this.tableElement.getBoundingClientRect();
    const lastRect = this.getLastRowElement().getBoundingClientRect();

    const x = elementRect.x - tableRect.x + elementRect.width - 1;
    const y = elementRect.y - tableRect.y;
    const width = 1;
    const height = lastRect.bottom - tableRect.top;
    return {x, y, width, height} as Rect;
  }

  getRowLineRect(lineIndex: number) {
    console.assert(this.items.length >= lineIndex && lineIndex >= 0);
    const element = this.getRowElement(lineIndex);

    const elementRect = element.getBoundingClientRect();
    const tableRect = this.tableElement.getBoundingClientRect();
    const lastRect = this.getLastColumnElement().getBoundingClientRect();

    const x = elementRect.x - tableRect.x;
    const y = elementRect.y - tableRect.y + (lastRect.bottom - tableRect.top) - 1;
    const width = elementRect.width;
    const height = 1;
    return {x, y, width, height} as Rect;
  }

  createAbsoluteDivElement(rect: Rect) {
    const element = document.createElement('div');
    element.style.position = 'absolute';
    element.style.left = `${rect.x}px`;
    element.style.top = `${rect.y}px`;
    element.style.width = `${rect.width}px`;
    element.style.height = `${rect.height}px`;
    return element;
  }

  createGhostElement(rect: Rect) {
    const element = this.createAbsoluteDivElement(rect);
    element.classList.add('grid-view--ghost');
    return element;
  }

  createLineElement(rect: Rect) {
    const element = this.createAbsoluteDivElement(rect);
    element.classList.add('grid-view--insert-line');
    return element;
  }

  getColumnRanges() {
    const result = [] as Array<Range>;
    for (const element of this.headerDataElements) {
      const rect = element.getBoundingClientRect();
      result.push({begin: rect.left, end: rect.right} as Range);
    }
    return result;
  }

  getRowRanges() {
    const result = [] as Array<Range>;
    for (const element of this.bodyRowElements) {
      const rect = element.getBoundingClientRect();
      result.push({begin: rect.top, end: rect.bottom} as Range);
    }
    return result;
  }

  onMouseDownColumn(event: MouseEvent, index: number) {
    this.draggingCandidateIndex = index;
    this.cursorX = event.clientX;
    this.cursorY = event.clientY;
    this.visibleRanges = this.getColumnRanges();
    document.addEventListener('mousemove', this.onMouseMoveColumn);
    document.addEventListener('mouseup', this.onMouseUpColumn);
  }

  onMouseDownRow(event: MouseEvent, index: number) {
    this.draggingCandidateIndex = index;
    this.cursorX = event.clientX;
    this.cursorY = event.clientY;
    this.visibleRanges = this.getRowRanges();
    document.addEventListener('mousemove', this.onMouseMoveRow);
    document.addEventListener('mouseup', this.onMouseUpRow);
  }

  moveGhostElement(event: MouseEvent) {
    if (!this.ghostElement) {
      throw Error('`cursorElement` must exist');
    }

    const dx = event.clientX - this.cursorX;
    const dy = event.clientY - this.cursorY;
    this.ghostElement.style.top = `${this.ghostElement.offsetTop + dy}px`;
    this.ghostElement.style.left = `${this.ghostElement.offsetLeft + dx}px`;
    this.cursorX = event.clientX;
    this.cursorY = event.clientY;
  }

  static getRangeIndexByCursor(ranges: Array<Range>, cursor: number) {
    if (ranges.length == 0) {
      return 0;
    }
    if (cursor < ranges[0].begin) {
      return 0;
    }
    for (const [index, rect] of ranges.entries()) {
      if (rect.begin <= cursor && cursor < rect.end) {
        const half = (rect.end - rect.begin) * 0.5;
        if (cursor <= rect.begin + half) {
          return index;
        } else {
          return index + 1;
        }
      }
    }
    return ranges.length;
  }

  getRangeIndexByCursor(coordinatePosition: number) {
    return GridView.getRangeIndexByCursor(this.visibleRanges, coordinatePosition);
  }

  moveColumnLineElement(index: number) {
    if (!this.lineElement) {
      throw Error('`lineElement` must exist');
    }
    const lineRect = this.getColumnLineRect(index);
    this.lineElement.style.left = `${lineRect.x}px`;
  }

  moveRowLineElement(index: number) {
    if (!this.lineElement) {
      throw Error('`lineElement` must exist');
    }
    const lineRect = this.getRowLineRect(index);
    this.lineElement.style.top = `${lineRect.y}px`;
  }

  startColumnDragging(index: number) {
    const rect = this.getColumnRect(index);
    const lineRect = this.getColumnLineRect(index);
    this.ghostElement = this.createGhostElement(rect);
    this.lineElement = this.createLineElement(lineRect);
    this.tableElement.insertBefore(this.ghostElement, null);
    this.tableElement.insertBefore(this.lineElement, null);
  }

  startRowDragging(index: number) {
    const rect = this.getRowRect(index);
    const lineRect = this.getRowLineRect(index);
    this.ghostElement = this.createGhostElement(rect);
    this.lineElement = this.createLineElement(lineRect);
    this.tableElement.insertBefore(this.ghostElement, null);
    this.tableElement.insertBefore(this.lineElement, null);
  }

  onMouseMoveColumn(event: MouseEvent) {
    if (this.draggingIndex == NO_INDEX) {
      console.assert(this.draggingCandidateIndex != NO_INDEX);
      this.draggingIndex = this.draggingCandidateIndex;
      this.startColumnDragging(this.draggingIndex);
    }

    this.moveGhostElement(event);
    const insertLineIndex = this.getRangeIndexByCursor(event.clientX);
    this.moveColumnLineElement(insertLineIndex);
  }

  onMouseMoveRow(event: MouseEvent) {
    if (this.draggingIndex == NO_INDEX) {
      console.assert(this.draggingCandidateIndex != NO_INDEX);
      this.draggingIndex = this.draggingCandidateIndex;
      this.startRowDragging(this.draggingIndex);
    }

    this.moveGhostElement(event);
    const insertLineIndex = this.getRangeIndexByCursor(event.clientY);
    this.moveRowLineElement(insertLineIndex);
  }

  static createArrayOfMovedItem<T>(
      source: Array<any>,
      selectIndex: number,
      insertIndex: number,
  ) {
    if (selectIndex == insertIndex || selectIndex + 1 == insertIndex) {
      return;
    }

    const result = [] as Array<T>;
    const selectItem = source[selectIndex];

    for (let i = 0; i < source.length; ++i) {
      if (i == insertIndex) {
        result.push(selectItem);
      }
      if (i == selectIndex) {
        continue;
      }
      result.push(source[i]);
    }
    if (source.length == insertIndex) {
      result.push(selectItem);
    }
    return result;
  }

  moveColumn(selectIndex: number, insertIndex: number) {
    const newHeaders = GridView.createArrayOfMovedItem<string>(
        this.headers, selectIndex, insertIndex
    );
    if (typeof newHeaders !== 'undefined') {
      this.headers = newHeaders;
    }
  }

  moveRow(selectIndex: number, insertIndex: number) {
    const newItems = GridView.createArrayOfMovedItem<any>(
        this.items, selectIndex, insertIndex
    );
    if (typeof newItems !== 'undefined') {
      this.items = newItems;
    }
  }

  endColumnDragging(event: MouseEvent) {
    const selectIndex = this.draggingIndex;
    const insertIndex = this.getRangeIndexByCursor(event.clientX);
    this.moveColumn(selectIndex, insertIndex);

    if (this.lineElement) {
      this.tableElement.removeChild(this.lineElement);
    }
    if (this.ghostElement) {
      this.tableElement.removeChild(this.ghostElement);
    }

    this.draggingCandidateIndex = NO_INDEX;
    this.draggingIndex = NO_INDEX;
    this.lineElement = undefined;
    this.ghostElement = undefined;
  }

  endRowDragging(event: MouseEvent) {
    const selectIndex = this.draggingIndex;
    const insertIndex = this.getRangeIndexByCursor(event.clientY);
    this.moveRow(selectIndex, insertIndex);

    if (this.lineElement) {
      this.tableElement.removeChild(this.lineElement);
    }
    if (this.ghostElement) {
      this.tableElement.removeChild(this.ghostElement);
    }

    this.draggingCandidateIndex = NO_INDEX;
    this.draggingIndex = NO_INDEX;
    this.lineElement = undefined;
    this.ghostElement = undefined;
  }

  onMouseUpColumn(event: MouseEvent) {
    document.removeEventListener('mousemove', this.onMouseMoveColumn);
    document.removeEventListener('mouseup', this.onMouseUpColumn);

    if (this.draggingIndex != NO_INDEX) {
      this.endColumnDragging(event);
    }
  }

  onMouseUpRow(event: MouseEvent) {
    document.removeEventListener('mousemove', this.onMouseMoveRow);
    document.removeEventListener('mouseup', this.onMouseUpRow);

    if (this.draggingIndex != NO_INDEX) {
      this.endRowDragging(event);
    }
  }

  // ------
  // Resize
  // ------

  onMouseDownColumnResize(event: MouseEvent, index: number) {
    this.draggingCandidateIndex = index;
    this.cursorX = event.clientX;
    const headerDataElement = this.getHeaderDataElement(index);
    const headerDataRect = headerDataElement.getBoundingClientRect();
    this.originalWidthOfResizeCandidate = headerDataRect.width;
    document.addEventListener('mousemove', this.onMouseMoveColumnResize);
    document.addEventListener('mouseup', this.onMouseUpColumnResize);
  }

  getAdjustedWidth(event: MouseEvent) {
    return this.originalWidthOfResizeCandidate + (event.clientX - this.cursorX);
  }

  resizeColumn(width: number, index: number) {
    const w = width > DEFAULT_MIN_WIDTH ? width : DEFAULT_MIN_WIDTH;
    const widthPixel = `${w}px`;
    const headerElement = this.getHeaderDataElement(index);
    headerElement.style.width = widthPixel;

    for (let i = 0; i < this.items.length; ++i) {
      const elem = this.getBodyDataElement(i, index);
      elem.style.width = widthPixel;
      elem.style.minWidth = widthPixel;
    }
  }

  onMouseMoveColumnResize(event: MouseEvent) {
    if (this.draggingIndex == NO_INDEX) {
      console.assert(this.draggingCandidateIndex != NO_INDEX);
      this.draggingIndex = this.draggingCandidateIndex;
    }
    const width = this.getAdjustedWidth(event);
    this.resizeColumn(width, this.draggingIndex);
  }

  onMouseUpColumnResize(event: MouseEvent) {
    if (this.draggingIndex != NO_INDEX) {
      const width = this.getAdjustedWidth(event);
      this.resizeColumn(width, this.draggingIndex);

      const index = this.draggingIndex;
      const header = this.headers[index];
      this.sizes[header].width = width;

      this.draggingCandidateIndex = NO_INDEX;
      this.draggingIndex = NO_INDEX;
    }
    document.removeEventListener('mousemove', this.onMouseMoveColumnResize);
    document.removeEventListener('mouseup', this.onMouseUpColumnResize);
  }

  onClickAddHeader() {
    this.headers.push('tester');
  }

  getRandomInt(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min)) + min;
  }

  onClickAddItem() {
    const newItem = {
      id: this.items.length + 1,
      name: 'New',
      sport: 'Unknown',
      rank: this.getRandomInt(0, 100),
    };
    this.items.push(newItem);

    this.$nextTick(() => {
      this.refreshTable();
    });
  }
}
</script>

<style lang="scss">
@import '~vuetify/src/styles/styles.sass';

$ghost-transparent: 0.2;

$color-blue: map-get($colors, 'blue');
$color-blue-accent-1: map-get($color-blue, 'accent-1');
$color-blue-accent-2: map-get($color-blue, 'accent-2');

$color-light-blue: map-get($colors, 'light-blue');
$color-light-blue-accent-3: map-get($color-blue, 'accent-3');
$color-light-blue-accent-4: map-get($color-blue, 'accent-4');

.theme--light.v-application {
  .grid-view--ghost {
    background: rgba(map-get($shades, 'black'), $ghost-transparent);
  }

  .grid-view--insert-line {
    background: $color-light-blue-accent-4;
    border-width: 1px;
    border-style: solid;
    border-color: $color-light-blue-accent-3;
  }
}

.theme--dark.v-application {
  .grid-view--ghost {
    background: rgba(map-get($shades, 'white'), $ghost-transparent);
  }

  .grid-view--insert-line {
    background: $color-blue-accent-1;
    border-width: 1px;
    border-style: solid;
    border-color: $color-blue-accent-2;
  }
}

.grid-view--ghost {
  position: absolute;
  user-select: none;
  cursor: grabbing;
}
</style>

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

$color-blue-accent-4: map-deep-get($colors, 'blue', 'accent-4');

$cell-padding-size: 8px;

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

@mixin cell-header-data-aligning {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  justify-content: space-between;
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

@mixin cell-header-data-sizing {
  padding: 0;
  min-width: 100px;
  min-height: 32px;
}

@mixin cell-index-sizing {
  padding: 0 $cell-padding-size;
  min-width: 40px;
  min-height: 32px;
}

@mixin cell-data-sizing {
  padding: 0 $cell-padding-size;
  min-width: 100px;
  min-height: 32px;
}

@mixin drag-vertical-sizing {
  width: $cell-padding-size;
  height: 32px;
}

@mixin drag-vertical-coloring {
  fill: currentColor;
}

.grid-view {
  @include flex-column;
  position: relative; // It is necessary because 'div', which is 'absolute', is added.
  user-select: none;

  //overflow: auto;
  //flex: 1 1 auto;
  //height: 100%;
  //max-width: 100%;

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
        @include cell-header-data-sizing;
        @include cell-header-data-aligning;
        @include cell-outline;

        .grid-view--header-data-content {
          @include cell-data-aligning;

          padding-left: $cell-padding-size;
          width: 100%;
          height: 100%;
        }

        .grid-view--header-data-resize {
          width: $cell-padding-size;
          height: 29px;
          border-radius: 6px;
        }

        .grid-view--header-data-resize:hover {
          cursor: col-resize;
          background: $color-blue-accent-4;
        }
      }

      .grid-view--header-add {
        @include cell-data-aligning;

        margin-left: 4px;
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

        cursor: grab;
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
    }

    .grid-view--body-add {
      margin-top: 4px;
      margin-left: 4px;
    }
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
</style>
