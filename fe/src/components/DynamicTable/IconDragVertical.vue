<template>
  <svg
      xmlns="http://www.w3.org/2000/svg"
      :role="role"
      :viewBox="viewBox"
      :aria-hidden="ariaHidden"
  >
    <path :d="icon"></path>
  </svg>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';
import {mdiDragVertical} from '@mdi/js';

@Component
export default class IconDragVertical extends Vue {
  private readonly icon = mdiDragVertical;

  @Prop({type: Number, default: 8})
  readonly x!: number;

  @Prop({type: Number, default: 0})
  readonly y!: number;

  @Prop({type: Number, default: 8})
  readonly width!: number;

  @Prop({type: Number, default: 24})
  readonly height!: number;

  @Prop({type: Boolean, default: true})
  readonly ariaHidden!: boolean;

  @Prop({type: String, default: 'img'})
  readonly role!: string;

  get viewBox() {
    return [this.x, this.y, this.width, this.height].join(' ');
  }
}
</script>
