<template>
  <div class="fill-width" :style="contentStyle">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop, Watch} from 'vue-property-decorator';

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
    return {height: `${this.contentHeight}px`};
  }

  mounted() {
    this.$nextTick(() => {
      window.addEventListener('resize', this.onResize);
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
.fill-width {
  max-width: 100%;
}

.absolute-position {
  position: absolute;
  //position: fixed;
  //transform: translateX(0%);
}
</style>
