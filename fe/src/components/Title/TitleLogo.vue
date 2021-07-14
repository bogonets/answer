<template>
  <span
      v-if="isTextMode"
      class="title-font"
  >
    {{ titleText }}
  </span>
  <v-img
      v-else
      src="@/assets/answer-logo.svg"
      contain
      :max-width="maxWidth"
      :max-height="maxHeight"
  ></v-img>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator';

const DEFAULT_TEXT_MODE = false;
const DEFAULT_IS_UPPERCASE = false;
const DEFAULT_ALTERNATIVE_TEXT = 'Answer';
const DEFAULT_IMAGE_SCALE_BREAKPOINTS = {
  xs: {x: 160, y: 160},
  sm: {x: 160, y: 160},
  md: {x: 160, y: 160},
  lg: {x: 160, y: 160},
  xl: {x: 200, y: 200},
};

@Component
export default class TitleLogo extends Vue {

  @Prop({type: Boolean, default: DEFAULT_TEXT_MODE})
  readonly isTextMode!: boolean;

  @Prop({type: Boolean, default: DEFAULT_IS_UPPERCASE})
  readonly isUppercase!: boolean;

  @Prop({type: String, default: DEFAULT_ALTERNATIVE_TEXT})
  readonly text!: string;

  get titleText(): string {
    if (this.isUppercase) {
      return this.text.toUpperCase();
    } else {
      return this.text;
    }
  }

  get maxWidth(): number {
    return DEFAULT_IMAGE_SCALE_BREAKPOINTS[this.$vuetify.breakpoint.name].x;
  }

  get maxHeight(): number {
    return DEFAULT_IMAGE_SCALE_BREAKPOINTS[this.$vuetify.breakpoint.name].y;
  }
}
</script>

<style lang="scss" scoped>
@import '~@/styles/sass/user-select-none.scss';

.title-font {
  @include user-select-none;
  font-family: NanumSquareRoundEB, sans-serif;
  font-size: 3rem;
}
</style>
