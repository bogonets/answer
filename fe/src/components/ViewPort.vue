<template>
  <div class="viewport" ref="root" :style="contentStyle">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Ref, Prop, Watch} from 'vue-property-decorator';

@Component
export default class ViewPort extends Vue {
  @Prop({type: Number, default: 0})
  readonly marginTop!: number;

  @Prop({type: Number, default: 0})
  readonly marginBottom!: number;

  @Prop({type: Number, default: 0})
  readonly marginLeft!: number;

  @Prop({type: Number, default: 0})
  readonly marginRight!: number;

  @Prop({type: Boolean, default: false})
  readonly flex!: boolean;

  @Ref()
  readonly root!: HTMLDivElement;

  contentWidth = window.innerWidth;
  contentHeight = window.innerHeight;

  @Watch('marginTop')
  onWatchMarginTop() {
    this.onResize();
  }

  @Watch('marginBottom')
  onWatchMarginBottom() {
    this.onResize();
  }

  @Watch('marginLeft')
  onWatchMarginLeft() {
    this.onResize();
  }

  @Watch('marginRight')
  onWatchMarginRight() {
    this.onResize();
  }

  @Watch('contentWidth')
  onWatchContentWidth(newVal: string, oldVal: string) {
    console.debug(`ViewPort width: ${oldVal} -> ${newVal}`);
  }

  @Watch('contentHeight')
  onWatchContentHeight(newVal: string, oldVal: string) {
    console.debug(`ViewPort height: ${oldVal} -> ${newVal}`);
  }

  get contentStyle() {
    const result = {
      height: `${this.contentHeight}px`,
      'max-height': `${this.contentHeight}px`,
    };

    if (this.flex) {
      return {display: 'flex', ...result};
    } else {
      return result;
    }
  }

  mounted() {
    window.addEventListener('resize', this.onResize);

    this.$nextTick(() => {
      this.onResize();
    });
  }

  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  }

  onResize() {
    const rootRect = this.root.getBoundingClientRect();
    const width = window.innerWidth - this.marginLeft - this.marginRight;
    const height = window.innerHeight - rootRect.y - this.marginTop - this.marginBottom;

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
