<template>
  <p class="text-subtitle-2 my-2" :class="textClass">
    <slot></slot>
  </p>
</template>

<script lang="ts">
import {Vue, Component, Prop} from 'vue-property-decorator';

@Component
export default class Subtitle extends Vue {
  @Prop({type: String})
  readonly value!: string;

  @Prop({type: Boolean, default: false})
  readonly bold!: boolean;

  get textBoldClass(): string {
    return this.bold ? 'font-weight-bold' : '';
  }

  get textColorClass(): string {
    return this.$vuetify.theme.dark ? 'text-color-dark' : 'text-color-light';
  }

  get textClass(): string {
    return this.textBoldClass + ' ' + this.textColorClass;
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

.text-color-light {
  color: map-get(map-get($material-light, 'text'), 'secondary');
}

.text-color-dark {
  color: map-get(map-get($material-dark, 'text'), 'secondary');
}
</style>
