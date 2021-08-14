<template>
  <v-container>
    <v-row>
      <v-col class="pb-0" cols="0" sm="4" md="4" lg="4" xl="4">
        <v-card flat color="transparent">
          <v-card-title>
            <span :class="headerTextColor">{{ header }}</span>
          </v-card-title>
          <v-card-subtitle class="pb-0">
            <span :class="subheaderTextColor">{{ subheader }}</span>
          </v-card-subtitle>
        </v-card>
      </v-col>

      <v-col cols="12" sm="8" md="8" lg="8" xl="8">
        <div class="pa-4">
          <slot></slot>
        </div>
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

  @Prop({type: String, default: ''})
  readonly headerColor!: string;

  @Prop({type: String, default: ''})
  readonly subheaderColor!: string;

  get headerTextColor(): string {
    if (this.headerColor) {
      return this.headerColor + '--text';
    }
    return ''
  }

  get subheaderTextColor(): string {
    if (this.subheaderColor) {
      return this.subheaderColor + '--text';
    }
    return ''
  }
}
</script>
