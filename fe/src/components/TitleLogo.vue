<template>
  <v-container>
    <v-row align="center" justify="center">
      <span v-if="isTextMode" class="title-font">
        {{ titleText }}
      </span>
      <v-img
          v-else
          src="@/assets/logo/answer-logo.svg"
          contain
          :alt="titleText"
          :max-width="maxWidth"
          :max-height="maxHeight"
      ></v-img>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

const DEFAULT_TEXT_MODE = false;
const DEFAULT_IS_UPPERCASE = false;
const DEFAULT_ALTERNATIVE_TEXT = 'Answer';
const DEFAULT_MAX_WIDTH = 160;
const DEFAULT_MAX_HEIGHT = 160;

@Component
export default class TitleLogo extends Vue {

  @Prop({type: Boolean, default: DEFAULT_TEXT_MODE})
  readonly isTextMode!: boolean;

  @Prop({type: Boolean, default: DEFAULT_IS_UPPERCASE})
  readonly isUppercase!: boolean;

  @Prop({type: String, default: DEFAULT_ALTERNATIVE_TEXT})
  readonly text!: string;

  @Prop({type: Number, default: DEFAULT_MAX_WIDTH})
  readonly maxWidth!: number;

  @Prop({type: Number, default: DEFAULT_MAX_HEIGHT})
  readonly maxHeight!: number;

  get titleText(): string {
    if (this.isUppercase) {
      return this.text.toUpperCase();
    } else {
      return this.text;
    }
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
