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
                  @mousedown="onMouseDownHeader($event, index)"
              >
                {{ header }}
              </div>

              <div
                  class="grid-view--header-data-resize"
                  :key="`${header}-divider`"
                  @mousedown="onMouseDownHeaderResize($event, index)"
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
            @mouseenter="onEnterRowItem($event, item)"
            @mouseleave="onLeaveRowItem($event, item)"
        >
          <div
              class="grid-view--body-drag"
              @mousedown="onMouseDownBodyDrag($event, index)"
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
              @click="onClickCell(item)"
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

    <div class="grid-view--footer">
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {mdiDragVertical} from '@mdi/js';

const NO_INDEX = -1;

interface Rect {
  x: number;
  y: number;
  width: number;
  height: number;
}

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

  draggingCandidateHeader = NO_INDEX;
  draggingCandidateBody = NO_INDEX;

  draggingHeader = NO_INDEX;
  draggingBody = NO_INDEX;

  columnRects = [] as Array<DOMRect>;
  rowRects = [] as Array<DOMRect>;

  insertLineElement?: HTMLDivElement;
  cursorElement?: HTMLDivElement;
  cursorId = NO_INDEX;
  cursorX = 0;
  cursorY = 0;

  mounted() {
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

  getBodyRowDataElement(rowIndex: number, columnIndex: number) {
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
    const viewRect = this.viewElement.getBoundingClientRect();
    const lastRect = this.getLastRowElement().getBoundingClientRect();

    const x = elementRect.x - viewRect.x;
    const y = elementRect.y - viewRect.y;
    const width = elementRect.width;
    const height = lastRect.bottom - tableRect.top;
    return {x, y, width, height} as Rect;
  }

  getRowRect(index: number) {
    console.assert(this.items.length > index && index >= 0);
    const element = this.getBodyRowElement(index);

    const elementRect = element.getBoundingClientRect();
    const tableRect = this.tableElement.getBoundingClientRect();
    const viewRect = this.viewElement.getBoundingClientRect();
    const lastRect = this.getLastColumnElement().getBoundingClientRect();

    const x = elementRect.x - viewRect.x;
    const y = elementRect.y - viewRect.y;
    const width = lastRect.right - tableRect.left;
    const height = elementRect.height;
    return {x, y, width, height} as Rect;
  }

  getInsertColumnRect(lineIndex: number) {
    console.assert(this.headers.length >= lineIndex && lineIndex >= 0);
    const element = this.getColumnElement(lineIndex);

    const elementRect = element.getBoundingClientRect();
    const tableRect = this.tableElement.getBoundingClientRect();
    const viewRect = this.viewElement.getBoundingClientRect();
    const lastRect = this.getLastRowElement().getBoundingClientRect();

    const x = elementRect.x - viewRect.x + elementRect.width - 1;
    const y = elementRect.y - viewRect.y;
    const width = 1;
    const height = lastRect.bottom - tableRect.top;
    return {x, y, width, height} as Rect;
  }

  getInsertRowRect(lineIndex: number) {
    console.assert(this.items.length >= lineIndex && lineIndex >= 0);
    const element = this.getRowElement(lineIndex);

    const elementRect = element.getBoundingClientRect();
    const tableRect = this.tableElement.getBoundingClientRect();
    const viewRect = this.viewElement.getBoundingClientRect();
    const lastRect = this.getLastColumnElement().getBoundingClientRect();

    const x = elementRect.x - viewRect.x;
    const y = elementRect.y - viewRect.y + (lastRect.bottom - tableRect.top) - 1;
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

  createInsertLineElement(rect: Rect) {
    const element = this.createAbsoluteDivElement(rect);
    element.classList.add('grid-view--insert-line');
    return element;
  }

  getColumnRects() {
    const result = [] as Array<DOMRect>;
    for (const element of this.headerDataElements) {
      result.push(element.getBoundingClientRect());
    }
    return result;
  }

  getRowRects() {
    const result = [] as Array<DOMRect>;
    for (const element of this.bodyRowElements) {
      result.push(element.getBoundingClientRect());
    }
    return result;
  }

  onMouseDownHeader(event: MouseEvent, index: number) {
    this.draggingCandidateHeader = index;
    this.cursorX = event.clientX;
    this.cursorY = event.clientY;
    this.columnRects = this.getColumnRects();
    document.addEventListener('mousemove', this.onMouseMoveHeader);
    document.addEventListener('mouseup', this.onMouseUpHeader);
  }

  onMouseDownBodyDrag(event: MouseEvent, index: number) {
    this.draggingCandidateBody = index;
    this.cursorX = event.clientX;
    this.cursorY = event.clientY;
    this.rowRects = this.getRowRects();
    document.addEventListener('mousemove', this.onMouseMoveBody);
    document.addEventListener('mouseup', this.onMouseUpBody);
  }

  moveCursorElement(event: MouseEvent) {
    if (!this.cursorElement) {
      throw Error('`cursorElement` must exist');
    }

    const dx = event.clientX - this.cursorX;
    const dy = event.clientY - this.cursorY;
    this.cursorElement.style.top = `${this.cursorElement.offsetTop + dy}px`;
    this.cursorElement.style.left = `${this.cursorElement.offsetLeft + dx}px`;
    this.cursorX = event.clientX;
    this.cursorY = event.clientY;
  }

  getColumnIndexByCursor(clientX: number) {
    if (this.columnRects.length == 0) {
      return 0;
    }
    if (clientX < this.columnRects[0].left) {
      return 0;
    }
    for (const [index, rect] of this.columnRects.entries()) {
      if (rect.left <= clientX && clientX < rect.right) {
        const half = (rect.width * 0.5);
        if (clientX <= rect.left + half) {
          return index;
        } else {
          return index + 1;
        }
      }
    }
    return this.columnRects.length;
  }

  getRowIndexByCursor(clientY: number) {
    if (this.rowRects.length == 0) {
      return 0;
    }
    if (clientY < this.rowRects[0].top) {
      return 0;
    }
    for (const [index, rect] of this.rowRects.entries()) {
      if (rect.top <= clientY && clientY < rect.bottom) {
        const half = (rect.height * 0.5);
        if (clientY <= rect.top + half) {
          return index;
        } else {
          return index + 1;
        }
      }
    }
    return this.rowRects.length;
  }

  moveInsertLineElementOfColumn(index: number) {
    if (!this.insertLineElement) {
      throw Error('`insertLineElement` must exist');
    }
    const lineRect = this.getInsertColumnRect(index);
    this.insertLineElement.style.left = `${lineRect.x}px`;
  }

  moveInsertLineElementOfRow(index: number) {
    if (!this.insertLineElement) {
      throw Error('`insertLineElement` must exist');
    }
    const lineRect = this.getInsertRowRect(index);
    this.insertLineElement.style.top = `${lineRect.y}px`;
  }

  startHeaderDragging(index: number) {
    const rect = this.getColumnRect(index);
    const lineRect = this.getInsertColumnRect(index);
    this.cursorElement = this.createGhostElement(rect);
    this.insertLineElement = this.createInsertLineElement(lineRect);
    this.viewElement.insertBefore(this.cursorElement, this.tableElement);
    this.viewElement.insertBefore(this.insertLineElement, this.tableElement);
  }

  startBodyDragging(index: number) {
    const rect = this.getRowRect(index);
    const lineRect = this.getInsertRowRect(index);
    this.cursorElement = this.createGhostElement(rect);
    this.insertLineElement = this.createInsertLineElement(lineRect);
    this.viewElement.insertBefore(this.cursorElement, this.tableElement);
    this.viewElement.insertBefore(this.insertLineElement, this.tableElement);
  }

  onMouseMoveHeader(event: MouseEvent) {
    if (this.draggingHeader == NO_INDEX) {
      console.assert(this.draggingCandidateHeader != NO_INDEX);
      this.draggingHeader = this.draggingCandidateHeader;
      this.startHeaderDragging(this.draggingHeader);
    }

    this.moveCursorElement(event);
    const insertLineIndex = this.getColumnIndexByCursor(event.clientX);
    this.moveInsertLineElementOfColumn(insertLineIndex);
  }

  onMouseMoveBody(event: MouseEvent) {
    if (this.draggingBody == NO_INDEX) {
      console.assert(this.draggingCandidateBody != NO_INDEX);
      this.draggingBody = this.draggingCandidateBody;
      this.startBodyDragging(this.draggingBody);
    }

    this.moveCursorElement(event);
    const insertLineIndex = this.getRowIndexByCursor(event.clientY);
    this.moveInsertLineElementOfRow(insertLineIndex);
  }

  moveHeader(selectIndex: number, insertIndex: number) {
    if (selectIndex == insertIndex || selectIndex + 1 == insertIndex) {
      return;
    }

    const buffer = [] as Array<string>;
    const selectItem = this.headers[selectIndex];

    for (let i = 0; i < this.headers.length; ++i) {
      if (i == insertIndex) {
        buffer.push(selectItem);
      }
      if (i == selectIndex) {
        continue;
      }
      buffer.push(this.headers[i]);
    }
    if (this.headers.length == insertIndex) {
      buffer.push(selectItem);
    }

    this.headers = buffer;
  }

  moveBody(selectIndex: number, insertIndex: number) {
    if (selectIndex == insertIndex || selectIndex + 1 == insertIndex) {
      return;
    }

    const buffer = [] as Array<any>;
    const selectItem = this.items[selectIndex];

    for (let i = 0; i < this.items.length; ++i) {
      if (i == insertIndex) {
        buffer.push(selectItem);
      }
      if (i == selectIndex) {
        continue;
      }
      buffer.push(this.items[i]);
    }
    if (this.items.length == insertIndex) {
      buffer.push(selectItem);
    }

    this.items = buffer;
  }

  endHeaderDragging(event: MouseEvent) {
    const selectIndex = this.draggingHeader;
    const insertIndex = this.getColumnIndexByCursor(event.clientX);
    this.moveHeader(selectIndex, insertIndex);

    if (this.insertLineElement) {
      this.viewElement.removeChild(this.insertLineElement);
    }
    if (this.cursorElement) {
      this.viewElement.removeChild(this.cursorElement);
    }

    this.draggingCandidateHeader = NO_INDEX;
    this.draggingHeader = NO_INDEX;
    this.insertLineElement = undefined;
    this.cursorElement = undefined;
  }

  endBodyDragging(event: MouseEvent) {
    const selectIndex = this.draggingBody;
    const insertIndex = this.getRowIndexByCursor(event.clientY);
    this.moveBody(selectIndex, insertIndex);

    if (this.insertLineElement) {
      this.viewElement.removeChild(this.insertLineElement);
    }
    if (this.cursorElement) {
      this.viewElement.removeChild(this.cursorElement);
    }

    this.draggingCandidateBody = NO_INDEX;
    this.draggingBody = NO_INDEX;
    this.insertLineElement = undefined;
    this.cursorElement = undefined;
  }

  onMouseUpHeader(event: MouseEvent) {
    document.removeEventListener('mousemove', this.onMouseMoveHeader);
    document.removeEventListener('mouseup', this.onMouseUpHeader);

    if (this.draggingHeader != NO_INDEX) {
      this.endHeaderDragging(event);
    }
  }

  onMouseUpBody(event: MouseEvent) {
    document.removeEventListener('mousemove', this.onMouseMoveBody);
    document.removeEventListener('mouseup', this.onMouseUpBody);

    if (this.draggingBody != NO_INDEX) {
      this.endBodyDragging(event);
    }
  }

  // ------
  // Resize
  // ------

  resizeCandidateHeader = NO_INDEX;
  resizeHeader = NO_INDEX;
  saveCursorX = 0;
  saveWidth = 0;

  onMouseDownHeaderResize(event: MouseEvent, index: number) {
    this.resizeCandidateHeader = index;
    this.saveCursorX = event.clientX;
    const headerDataElement = this.getHeaderDataElement(index);
    const headerDataRect = headerDataElement.getBoundingClientRect();
    this.saveWidth = headerDataRect.width;
    document.addEventListener('mousemove', this.onMouseMoveHeaderResize);
    document.addEventListener('mouseup', this.onMouseUpHeaderResize);
  }

  getResizeWidth(event: MouseEvent) {
    return this.saveWidth + (event.clientX - this.saveCursorX);
  }

  resizeColumn(width: number, index: number) {
    const widthPixel = `${width}px`;
    const headerElement = this.getHeaderDataElement(index);
    headerElement.style.width = widthPixel;

    for (let i = 0; i < this.items.length; ++i) {
      const elem = this.getBodyRowDataElement(i, index);
      elem.style.width = widthPixel;
    }
  }

  onMouseMoveHeaderResize(event: MouseEvent) {
    if (this.resizeHeader == NO_INDEX) {
      console.assert(this.resizeCandidateHeader != NO_INDEX);
      this.resizeHeader = this.resizeCandidateHeader;
    }
    const width = this.getResizeWidth(event);
    this.resizeColumn(width, this.resizeHeader);
  }

  onMouseUpHeaderResize(event: MouseEvent) {
    if (this.resizeHeader != NO_INDEX) {
      const width = this.getResizeWidth(event);
      this.resizeColumn(width, this.resizeHeader);

      const index = this.resizeHeader;
      const header = this.headers[index];
      this.sizes[header].width = width;

      this.resizeCandidateHeader = NO_INDEX;
      this.resizeHeader = NO_INDEX;
    }
    document.removeEventListener('mousemove', this.onMouseMoveHeaderResize);
    document.removeEventListener('mouseup', this.onMouseUpHeaderResize);
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
      user-select: none;

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

            padding-left: 8px;
            width: 100%;
            height: 100%;
          }

          .grid-view--header-data-resize {
            width: 8px;
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
</style>
