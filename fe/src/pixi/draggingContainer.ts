import {Container, InteractionData, InteractionEvent} from 'pixi.js';
import {UndefinedException} from '@/exceptions';

export class DraggingContainer extends Container {
  dragAlpha?: number;
  dragAlphaPrev?: number;

  dragCursorOffsetX: number;
  dragCursorOffsetY: number;

  dragEventData?: InteractionData;

  constructor(dragAlpha?: number) {
    super();
    this.dragAlpha = dragAlpha;
    this.dragAlphaPrev = undefined;

    this.dragCursorOffsetX = 0;
    this.dragCursorOffsetY = 0;

    this.dragEventData = undefined;
  }

  get dragging() {
    return !!this.dragEventData;
  }

  get dragData() {
    if (!this.dragEventData) {
      throw new UndefinedException('Did not start dragging');
    }
    return this.dragEventData;
  }

  private onDragStart(event: InteractionEvent) {
    if (typeof this.dragAlpha !== 'undefined') {
      this.dragAlphaPrev = this.alpha;
      this.alpha = this.dragAlpha;
    } else {
      this.dragAlphaPrev = undefined;
    }

    this.dragEventData = event.data;
    const begin = event.data.getLocalPosition(this.parent);
    this.dragCursorOffsetX = begin.x - this.x;
    this.dragCursorOffsetY = begin.y - this.y;
  }

  private onDragMove(_: InteractionEvent) {
    if (this.dragging) {
      const pos = this.dragData.getLocalPosition(this.parent);
      this.x = pos.x - this.dragCursorOffsetX;
      this.y = pos.y - this.dragCursorOffsetY;
    }
  }

  private onDragEnd(_: InteractionEvent) {
    if (this.dragging) {
      if (typeof this.dragAlphaPrev !== 'undefined') {
        this.alpha = this.dragAlphaPrev;
        this.dragAlphaPrev = undefined;
      }

      this.dragCursorOffsetX = 0;
      this.dragCursorOffsetY = 0;
      this.dragEventData = undefined;
    }
  }

  registerDragging() {
    this.on('pointerdown', this.onDragStart);
    this.on('pointermove', this.onDragMove);
    this.on('pointerup', this.onDragEnd);
    // noinspection SpellCheckingInspection
    this.on('pointerupoutside', this.onDragEnd);
  }

  registerDraggingOnlyMouse() {
    this.on('mousedown', this.onDragStart);
    this.on('mousemove', this.onDragMove);
    this.on('mouseup', this.onDragEnd);
    // noinspection SpellCheckingInspection
    this.on('mouseupoutside', this.onDragEnd);
  }

  registerDraggingOnlyTouch() {
    this.on('touchstart', this.onDragStart);
    this.on('touchmove', this.onDragMove);
    this.on('touchend', this.onDragEnd);
    // noinspection SpellCheckingInspection
    this.on('touchendoutside', this.onDragEnd);
  }
}
