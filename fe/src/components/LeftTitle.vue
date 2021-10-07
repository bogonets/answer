<template>
  <v-container>
    <v-row>
      <v-col
          :class="leftClass"
          :cols="leftXsRatio"
          :sm="leftRatio"
          :md="leftRatio"
          :lg="leftRatio"
          :xl="leftRatio"
      >
        <div class="text--primary text-h6" :class="headerClass">
          {{ header }}
        </div>
        <div class="text--secondary text-subtitle-2" :class="subheaderClass">
          {{ subheader }}
        </div>
      </v-col>

      <v-col
          :class="rightClass"
          :cols="rightXsRatio"
          :sm="rightRatio"
          :md="rightRatio"
          :lg="rightRatio"
          :xl="rightRatio"
      >
        <slot></slot>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

@Component
export default class LeftTitle extends Vue {
  @Prop({type: String, default: ''})
  readonly header!: string;

  @Prop({type: String, default: ''})
  readonly subheader!: string;

  @Prop({type: Number, default: 4})
  readonly leftRatio!: number;

  @Prop({type: Number, default: 8})
  readonly rightRatio!: number;

  @Prop({type: Boolean, default: false})
  readonly noWrapXs!: boolean;

  @Prop({type: Boolean, default: false})
  readonly xSmall!: boolean;

  @Prop({type: Boolean, default: false})
  readonly small!: boolean;

  @Prop({type: Boolean, default: false})
  readonly noGutter!: boolean;

  get leftXsRatio() {
    return this.noWrapXs ? this.leftRatio : 12;
  }

  get rightXsRatio() {
    return this.noWrapXs ? this.rightRatio : 12;
  }

  get headerClass() {
    if (this.xSmall) {
      return 'text-subtitle-2';
    } else if (this.small) {
      return 'text-subtitle-1';
    } else {
      return 'text-h6';
    }
  }

  get subheaderClass() {
    if (this.xSmall) {
      return 'text-caption';
    } else if (this.small) {
      return 'text-body-2';
    } else {
      return 'text-subtitle-2';
    }
  }

  get leftClass() {
    return this.noGutter ? '' : 'px-4 pt-4';
  }

  get rightClass() {
    return this.noGutter ? '' : 'pa-4';
  }
}
</script>
