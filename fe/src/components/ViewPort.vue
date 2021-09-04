<template>
  <div class="viewport" :style="contentStyle">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop, Watch} from 'vue-property-decorator';

const APP_BAR_HEIGHT = 48;

@Component
export default class ViewPort extends Vue {
  @Prop({type: Number, default: APP_BAR_HEIGHT})
  readonly marginTop!: number;

  @Prop({type: Number, default: 0})
  readonly marginBottom!: number;

  @Prop({type: Number, default: 0})
  readonly marginLeft!: number;

  @Prop({type: Number, default: 0})
  readonly marginRight!: number;

  contentWidth = window.innerWidth;
  contentHeight = window.innerHeight;

  @Watch('contentWidth')
  onChangeContentWidth(newVal: string, oldVal: string) {
    console.debug(`Update content-width: ${oldVal} -> ${newVal}`);
  }

  @Watch('contentHeight')
  onChangeContentHeight(newVal: string, oldVal: string) {
    console.debug(`Update content-height: ${oldVal} -> ${newVal}`);
  }

  get contentStyle() {
    return {
      'height': `${this.contentHeight}px`,
      'max-height': `${this.contentHeight}px`
    };
  }

  mounted() {
    window.addEventListener('resize', this.onResize);

    this.$nextTick(() => {
      this.onResize();
    })
  }

  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  }

  onResize() {
    const width = window.innerWidth - this.marginLeft - this.marginRight;
    const height = window.innerHeight - this.marginTop - this.marginBottom;

    if (this.contentWidth != width) {
      this.contentWidth = width;
    }
    if (this.contentHeight != height) {
      this.contentHeight = height;
    }
  }
}
</script>

<style lang="scss" scoped>
@mixin fill-width {
  max-width: 100%;
}

@mixin absolute-position {
  position: absolute;
}

@mixin fixed-position {
  position: fixed;
  transform: translateX(0%);
}

.viewport {
  @include fill-width;
}
</style>
