<template>
  <div class="title-container" ref="container">
    <span class="title-text" ref="text">{{getTitle}}</span>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator'

const DEFAULT_TITLE = "ANSWER";
const DEFAULT_UPPERCASE = false;
const DEFAULT_FONT_SIZE = 32;
const DEFAULT_FONT_STYLE = ""; // e.g. "italic";
const DEFAULT_FONT_SHADOW = "";  // e.g. "2px 2px gray";

@Component
export default class MainTitle extends Vue {

  @Prop({type: String, default: DEFAULT_TITLE})
  readonly title: string;

  @Prop({type: Boolean, default: DEFAULT_UPPERCASE})
  readonly isUppercase: boolean;

  @Prop({type: [String, Number], default: DEFAULT_FONT_SIZE})
  readonly fontSize: string | number;

  @Prop({type: String, default: DEFAULT_FONT_STYLE})
  readonly fontStyle: string;

  @Prop({type: String, default: DEFAULT_FONT_SHADOW})
  readonly fontShadow: string;

  get getTitle(): string {
    if (this.isUppercase) {
      return this.title.toUpperCase();
    } else {
      return this.title;
    }
  }

  mounted() {
    this.$nextTick(() => this.onUpdatedDom())
  }

  onUpdatedDom() {
    let text = this.$refs.text

    if (this.fontSize) {
      let sizeText: string;
      if (typeof(this.fontSize) == "string") {
        sizeText = this.fontSize;
      } else {
        sizeText = `${this.fontSize}px`;
      }
      text.style["font-size"] = sizeText;
    }

    if (this.fontStyle) {
      text.style["font-style"] = this.fontStyle;
    }

    if (this.fontShadow) {
      text.style["text-shadow"] = this.fontShadow;
    }
  }
}
</script>

<style lang="scss" scoped>
@import "~@/styles/sass/user-select-none.scss";

.title-container {
  width: fit-content;
}

.title-text {
  @include user-select-none;
  font-family: NanumSquareRoundEB, sans-serif;
}
</style>
