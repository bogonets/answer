<template>
  <div class="record-controller">
    <canvas
      class="record-timeline"
      ref="record-timeline"
      :style="recordTimelineStyle"
      @click="onClick"
      @resize="onResize"
      v-resize="onWindowResize"
    ></canvas>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Ref, Watch, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import colors from 'vuetify/lib/util/colors';
import {ContextException, InvalidRangeException} from '@/exceptions';
import moment from 'moment';

export const MILLISECONDS_TO_DAY = 24 * 60 * 60 * 1000;

export interface RatioRange {
  /** Absolute start time. */
  startTime: moment.Moment;

  /** Absolute last time. */
  lastTime: moment.Moment;

  /** percentage of the day. (0~1) */
  start: number;

  /** percentage of the day. (0~1) */
  last: number;

  /** Not a percentage of the day, Percentage of the existing range. */
  ratio: number;
}

@Component
export default class RecordController extends VueBase {
  @Prop({type: [Number, String], default: '100%'})
  readonly width!: number | string;

  @Prop({type: Number, default: 8})
  readonly paddingLeft!: number;

  @Prop({type: Number, default: 8})
  readonly paddingRight!: number;

  // ------------------------
  // [Drawing Order #1] Ruler
  // ------------------------

  @Prop({type: Number, default: 20})
  readonly rulerHeight!: number;

  @Prop({type: Number, default: 1.0})
  readonly rulerLineWidth!: number;

  @Prop({type: String, default: '.75rem Roboto'})
  readonly rulerFontStyle!: string;

  // -------------------------
  // [Drawing Order #2] Record
  // -------------------------

  @Prop({type: Number, default: 4})
  readonly recordHeight!: number;

  @Prop({type: Array, default: () => []})
  readonly recordRanges!: Array<RatioRange>;

  // --------------------------------
  // [Drawing Order #3] Record Buffer
  // --------------------------------

  @Prop({type: Number, default: 4})
  readonly recordBufferHeight!: number;

  // ------------------------
  // [Drawing Order #4] Event
  // ------------------------

  @Prop({type: Number, default: 4})
  readonly eventHeight!: number;

  @Prop({type: Number, default: 1.0})
  readonly eventLineWidth!: number;

  @Prop({type: Array, default: () => []})
  readonly eventOffsets!: Array<number>;

  // -------------------------------
  // [Drawing Order #5] Event Buffer
  // -------------------------------

  @Prop({type: Number, default: 4})
  readonly eventBufferHeight!: number;

  // -------------------------
  // [Drawing Order #6] Cursor
  // -------------------------

  @Prop({type: Number, default: 0.0})
  readonly cursorPosition!: number;

  @Prop({type: Number, default: 2})
  readonly cursorWidth!: number;

  @Prop({type: String})
  readonly cursorColor?: string;

  // -------------------------

  @Prop({type: Boolean, default: false})
  readonly disabled!: boolean;

  @Ref('record-timeline')
  readonly recordTimelineCanvas!: HTMLCanvasElement;

  backgroundOffscreenCanvas!: HTMLCanvasElement;

  mounted() {
    this.updateRecordTimeline();
  }

  @Watch('width')
  watchWidth() {
    this.updateRecordTimeline();
  }

  @Watch('paddingLeft')
  watchPaddingLeft() {
    this.updateRecordTimeline();
  }

  @Watch('paddingRight')
  watchPaddingRight() {
    this.updateRecordTimeline();
  }

  @Watch('rulerHeight')
  watchRulerHeight() {
    this.updateRecordTimeline();
  }

  @Watch('rulerLineWidth')
  watchRulerLineWidth() {
    this.updateRecordTimeline();
  }

  @Watch('rulerFontStyle')
  watchRulerFontStyle() {
    this.updateRecordTimeline();
  }

  @Watch('recordHeight')
  watchRecordHeight() {
    this.updateRecordTimeline();
  }

  @Watch('recordRanges')
  watchRecordRanges() {
    this.updateRecordTimeline();
  }

  @Watch('recordBufferHeight')
  watchRecordBufferHeight() {
    this.updateRecordTimeline();
  }

  @Watch('eventHeight')
  watchEventHeight() {
    this.updateRecordTimeline();
  }

  @Watch('eventLineWidth')
  watchEventLineWidth() {
    this.updateRecordTimeline();
  }

  @Watch('eventOffsets')
  watchEventOffsets() {
    this.updateRecordTimeline();
  }

  @Watch('eventBufferHeight')
  watchEventBufferHeight() {
    this.updateRecordTimeline();
  }

  @Watch('cursorPosition')
  watchCursorPosition() {
    this.updateRecordTimelineForCursor();
  }

  @Watch('cursorWidth')
  watchCursorWidth() {
    this.updateRecordTimelineForCursor();
  }

  @Watch('cursorColor')
  watchCursorColor() {
    this.updateRecordTimelineForCursor();
  }

  @Watch('disabled')
  watchDisabled() {
    this.updateRecordTimeline();
  }

  get recordTimelineHeight() {
    return (
      this.rulerHeight +
      this.recordHeight +
      this.recordBufferHeight +
      this.eventHeight +
      this.eventBufferHeight
    );
  }

  get recordTimelineStyle() {
    let style = '';
    style += `width: ${this.width};`;
    style += `height: ${this.recordTimelineHeight}px;`;
    return style;
  }

  update() {
    this.updateRecordTimeline();
  }

  updateRecordTimelineForCursor() {
    this.updateRecordTimeline(undefined, undefined, false);
  }

  updateRecordTimeline(width?: number, height?: number, refresh = true) {
    const w = width ?? this.recordTimelineCanvas.offsetWidth;
    const h = height ?? this.recordTimelineCanvas.offsetHeight;

    this.recordTimelineCanvas.width = w;
    this.recordTimelineCanvas.height = h;

    let updateBackgroundOffscreenCanvas = refresh;
    if (!this.backgroundOffscreenCanvas) {
      this.backgroundOffscreenCanvas = document.createElement('canvas');
      updateBackgroundOffscreenCanvas = true;
    }
    if (
      this.backgroundOffscreenCanvas.width != w ||
      this.backgroundOffscreenCanvas.height != h
    ) {
      this.backgroundOffscreenCanvas.width = w;
      this.backgroundOffscreenCanvas.height = h;
      updateBackgroundOffscreenCanvas = true;
    }
    if (updateBackgroundOffscreenCanvas) {
      const bgContext = this.backgroundOffscreenCanvas.getContext('2d');
      if (!bgContext) {
        throw new ContextException('Unable to get context for 2D canvas');
      }
      this.drawBackground(bgContext, w, h);
    }

    const context = this.recordTimelineCanvas.getContext('2d');
    if (!context) {
      throw new ContextException('Unable to get context for 2D canvas');
    }

    context.clearRect(0, 0, w, h);
    context.drawImage(this.backgroundOffscreenCanvas, 0, 0);

    const rulerWidth = w - this.paddingLeft - this.paddingRight;
    this.drawCursor(context, this.paddingLeft, this.rulerHeight, rulerWidth, h);
  }

  drawBackground(context: CanvasRenderingContext2D, width: number, height: number) {
    context.clearRect(0, 0, width, height);

    const rulerWidth = width - this.paddingLeft - this.paddingRight;
    const timelineRulerY = 0;
    this.drawTimelineRuler(
      context,
      this.paddingLeft,
      timelineRulerY,
      rulerWidth,
      this.rulerHeight,
    );

    const navigationY = timelineRulerY + this.rulerHeight;
    const navigationHeight = this.recordTimelineHeight - this.rulerHeight;
    context.strokeStyle = this.timelineColor;
    context.lineWidth = 1;
    context.fillStyle = this.navigationColor;
    context.fillRect(this.paddingLeft, navigationY, rulerWidth, navigationHeight);
    context.strokeRect(this.paddingLeft, navigationY, rulerWidth, navigationHeight);

    const recordY = navigationY;
    this.drawRecord(context, this.paddingLeft, recordY, rulerWidth, this.recordHeight);

    const recordBufferY = recordY + this.recordHeight;
    this.drawRecordBuffer(
      context,
      this.paddingLeft,
      recordBufferY,
      rulerWidth,
      this.recordBufferHeight,
    );

    const eventY = recordBufferY + this.recordBufferHeight;
    this.drawEvent(context, this.paddingLeft, eventY, rulerWidth, this.eventHeight);

    // const eventBufferY = eventY + this.eventHeight;
    // this.drawEvent(
    //     context,
    //     this.paddingLeft,
    //     eventBufferY,
    //     rulerWidth,
    //     this.eventBufferHeight,
    // );
  }

  get timelineColor() {
    if (this.$vuetify.theme.dark) {
      return colors.grey.darken2;
    } else {
      return colors.grey.base;
    }
  }

  get navigationColor() {
    if (this.$vuetify.theme.dark) {
      return colors.grey.darken2;
    } else {
      return colors.grey.base;
    }
  }

  get recordColor() {
    const color = this.$vuetify.theme.currentTheme.info;
    if (color) {
      return color.toString();
    } else {
      return colors.blue.base;
    }
  }

  get eventColor() {
    const color = this.$vuetify.theme.currentTheme.warning;
    if (color) {
      return color.toString();
    }
    return colors.amber.base;
  }

  get cursorStyle() {
    if (this.cursorColor) {
      return this.cursorColor;
    }

    let color;
    if (this.disabled) {
      color = this.$vuetify.theme.currentTheme.secondary;
    } else {
      color = this.$vuetify.theme.currentTheme.primary;
    }

    if (color) {
      return color.toString();
    } else {
      return colors.blue.darken2;
    }
  }

  drawTimelineRuler(
    context: CanvasRenderingContext2D,
    x: number,
    y: number,
    w: number,
    h: number,
  ) {
    context.lineWidth = this.rulerLineWidth;
    context.strokeStyle = this.timelineColor;
    context.font = this.rulerFontStyle;
    context.textAlign = 'center';
    context.fillStyle = this.timelineColor;

    const DAY_TO_HOURS = 24;
    const TEXT_BOTTOM_MARGIN = 2;

    const stepWidth = w / DAY_TO_HOURS;
    const stepHeight = h / 2;
    for (let i = 0; i <= DAY_TO_HOURS; ++i) {
      const pos = x + stepWidth * i;
      context.beginPath();
      context.moveTo(pos, y + stepHeight + TEXT_BOTTOM_MARGIN);
      context.lineTo(pos, h);
      context.stroke();
      context.fillText(i.toString(), pos, y + stepHeight);
    }
  }

  drawRecord(
    context: CanvasRenderingContext2D,
    x: number,
    y: number,
    w: number,
    h: number,
  ) {
    context.fillStyle = this.recordColor;
    for (const range of this.recordRanges) {
      const left = x + range.start * w;
      const right = x + range.last * w;
      context.fillRect(left, y, Math.abs(right - left), h);
    }
  }

  drawEvent(
    context: CanvasRenderingContext2D,
    x: number,
    y: number,
    w: number,
    h: number,
  ) {
    context.lineWidth = this.eventLineWidth;
    context.strokeStyle = this.eventColor;
    for (const offset of this.eventOffsets) {
      const pos = x + offset * w;
      context.beginPath();
      context.moveTo(pos, y);
      context.lineTo(pos, y + h);
      context.stroke();
    }
  }

  drawRecordBuffer(
    context: CanvasRenderingContext2D,
    x: number,
    y: number,
    w: number,
    h: number,
  ) {}

  drawEventBuffer(
    context: CanvasRenderingContext2D,
    x: number,
    y: number,
    w: number,
    h: number,
  ) {}

  drawCursor(
    context: CanvasRenderingContext2D,
    x: number,
    y: number,
    w: number,
    h: number,
  ) {
    if (this.cursorPosition < 0 || 1 < this.cursorPosition) {
      throw new InvalidRangeException(
        `Invalid range of position: ${this.cursorPosition} (Expect range: 0 <= pos <= 1)`,
      );
    }

    const pos = x + w * this.cursorPosition;
    context.lineWidth = this.cursorWidth;
    context.strokeStyle = this.cursorStyle;
    context.beginPath();
    context.moveTo(pos, y);
    context.lineTo(pos, h);
    context.stroke();
  }

  onClick(event: PointerEvent) {
    const canvasWidth = this.recordTimelineCanvas.width;

    let x;
    if (event.offsetX >= canvasWidth - this.paddingRight) {
      x = 1.0;
    } else if (event.offsetX <= this.paddingLeft) {
      x = 0.0;
    } else {
      const width = canvasWidth - this.paddingLeft - this.paddingRight;
      x = (event.offsetX - this.paddingLeft) / width;
    }

    this.click(x);
  }

  onResize() {
    this.updateRecordTimeline();
  }

  onWindowResize() {
    this.updateRecordTimeline();
  }

  @Emit('click')
  click(pos: number) {
    if (pos < 0 || 1 < pos) {
      throw new InvalidRangeException(
        `Invalid range of position: ${pos} (Expect range: 0 <= pos <= 1)`,
      );
    }
    return pos;
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

.theme--light.v-application {
  //.record-controller {
  //  background-color: $color-grey-lighten-1;
  //}
}

.theme--dark.v-application {
  //.record-controller {
  //  background-color: $color-grey-darken-3;
  //}
}

.record-controller {
  display: flex;
  flex-direction: column;

  padding: 0;
  margin: 0;

  width: 100%;

  .record-timeline {
  }
}
</style>
