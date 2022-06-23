<template>
  <!-- IMPORTANT: Do not remove the <div> tag. -->
  <!-- You must be able to assign the properties of the parent component. -->
  <div>
    <span :class="classes" :style="styles">
      <slot></slot>
    </span>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

type SizeType =
  | 'h1'
  | 'h2'
  | 'h3'
  | 'h4'
  | 'h5'
  | 'h6'
  | 'subtitle-1'
  | 'subtitle-2'
  | 'body-1'
  | 'body-2'
  | 'button'
  | 'caption'
  | 'overline';

type WeightType = 'black' | 'bold' | 'medium' | 'normal' | 'light' | 'thin';

type AlignType = 'left' | 'center' | 'right';

type DecorationType = 'none' | 'line-through' | 'overline' | 'underline';

type OpacityType = 'primary' | 'secondary' | 'disabled';

type TransformType = 'lowercase' | 'uppercase' | 'capitalize';

type RtlAlignmentType = 'start' | 'end';

type ColorType =
  | string
  | 'primary'
  | 'secondary'
  | 'accent'
  | 'error'
  | 'info'
  | 'success'
  | 'warning';

type BrightnessType =
  | 'lighten-1'
  | 'lighten-2'
  | 'lighten-3'
  | 'lighten-4'
  | 'lighten-5'
  | 'darken-1'
  | 'darken-2'
  | 'darken-3'
  | 'darken-4'
  | 'accent-1'
  | 'accent-2'
  | 'accent-3'
  | 'accent-4';

@Component
export default class LabelSpan extends Vue {
  @Prop({default: ''})
  readonly size!: SizeType;

  @Prop({default: ''})
  readonly weight!: WeightType;

  @Prop({default: false})
  readonly italic!: boolean;

  @Prop({default: false})
  readonly justify!: boolean;

  @Prop({default: ''})
  readonly align!: AlignType;

  @Prop({default: ''})
  readonly decoration!: DecorationType;

  @Prop({default: ''})
  readonly opacity!: OpacityType;

  @Prop({default: ''})
  readonly transform!: TransformType;

  @Prop({default: false})
  readonly noWrap!: boolean;

  // Requires `display: inline-block` or `display: block`.
  @Prop({default: false})
  readonly truncate!: boolean;

  @Prop({default: ''})
  readonly rtlAlignment!: RtlAlignmentType;

  @Prop({default: ''})
  readonly color!: ColorType;

  @Prop({default: ''})
  readonly brightness!: BrightnessType;

  @Prop({default: ''})
  readonly backgroundColor!: ColorType;

  @Prop({default: ''})
  readonly backgroundBrightness!: BrightnessType;

  get sizeClassName() {
    if (this.size) {
      return 'text-' + this.size;
    } else {
      return '';
    }
  }

  get weightClassName() {
    if (this.weight) {
      return 'font-weight-' + this.weight;
    } else {
      return '';
    }
  }

  get italicClassName() {
    if (this.italic) {
      return 'font-italic';
    } else {
      return '';
    }
  }

  get justifyClassName() {
    if (this.justify) {
      return 'text-justify';
    } else {
      return '';
    }
  }

  get alignClassName() {
    if (this.align) {
      return 'text-' + this.align;
    } else {
      return '';
    }
  }

  get decorationClassName() {
    if (this.decoration) {
      return 'text-decoration-' + this.decoration;
    } else {
      return '';
    }
  }

  get opacityClassName() {
    if (this.opacity) {
      return 'text--' + this.opacity;
    } else {
      return '';
    }
  }

  get transformClassName() {
    if (this.transform) {
      return 'text-' + this.transform;
    } else {
      return '';
    }
  }

  get noWrapClassName() {
    if (this.noWrap) {
      return 'text-no-wrap';
    } else {
      return '';
    }
  }

  get truncateClassName() {
    if (this.truncate) {
      return 'text-truncate';
    } else {
      return '';
    }
  }

  get rtlAlignmentClassName() {
    if (this.rtlAlignment) {
      return 'text-' + this.rtlAlignment;
    } else {
      return '';
    }
  }

  get colorClassName() {
    if (this.color && this.color[0] !== '#') {
      return this.color + '--text';
    } else {
      return '';
    }
  }

  get brightnessClassName() {
    if (this.brightness) {
      return 'text--' + this.brightness;
    } else {
      return '';
    }
  }

  get backgroundColorClassName() {
    if (this.backgroundColor && this.backgroundColor[0] !== '#') {
      return this.backgroundColor;
    } else {
      return '';
    }
  }

  get backgroundBrightnessClassName() {
    if (this.backgroundBrightness) {
      return this.backgroundBrightness;
    } else {
      return '';
    }
  }

  get classes() {
    const styles = [
      this.sizeClassName,
      this.weightClassName,
      this.italicClassName,
      this.justifyClassName,
      this.alignClassName,
      this.decorationClassName,
      this.opacityClassName,
      this.transformClassName,
      this.noWrapClassName,
      this.truncateClassName,
      this.rtlAlignmentClassName,
      this.colorClassName,
      this.brightnessClassName,
      this.backgroundColorClassName,
      this.backgroundBrightnessClassName,
    ];
    return styles.filter(x => !!x).join(' ');
  }

  get colorStyle() {
    if (this.color && this.color[0] === '#') {
      return this.color;
    } else {
      return '';
    }
  }

  get backgroundColorStyle() {
    if (this.backgroundColor && this.backgroundColor[0] === '#') {
      return this.backgroundColor;
    } else {
      return '';
    }
  }

  get styles() {
    const color = this.colorStyle;
    const background = this.backgroundColorStyle;
    let style = '';
    if (color) {
      style += `color: ${color};`;
    }
    if (background) {
      style += `background-color: ${background};`;
    }
    return style;
  }
}
</script>
