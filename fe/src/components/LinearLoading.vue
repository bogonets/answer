<template>
  <v-container>
    <v-row class="my-12" align="center" justify="center">
      <v-progress-linear
          :color="progressColor"
          :height="progressHeight"
          :indeterminate="progressIndeterminate"
          rounded
      ></v-progress-linear>
    </v-row>
    <v-row class="my-6" align="center" justify="center">
      {{ loadingText }}
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Vue, Component, Prop } from 'vue-property-decorator';

const DEFAULT_PROGRESS_COLOR = 'primary';
const DEFAULT_PROGRESS_HEIGHT = 6;
const DEFAULT_PROGRESS_INDETERMINATE = true;
const DEFAULT_LOADING_TEXT = '';

@Component
export default class LinearLoading extends Vue {

  @Prop({type: String, default: DEFAULT_PROGRESS_COLOR})
  readonly progressColor!: string;

  @Prop({type: Number, default: DEFAULT_PROGRESS_HEIGHT})
  readonly progressHeight!: number;

  @Prop({type: Boolean, default: DEFAULT_PROGRESS_INDETERMINATE})
  readonly progressIndeterminate!: boolean;

  @Prop({type: String, default: DEFAULT_LOADING_TEXT})
  readonly loadingText!: boolean;
}
</script>
