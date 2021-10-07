<template>
  <div v-ripple class="card" @click="click" :style="styleText">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Prop, Emit} from 'vue-property-decorator';

@Component
export default class CardButton extends Vue {
  @Prop({type: String, default: '120px'})
  readonly height!: string;

  get styleText() {
    return `height: ${this.height};`;
  }

  @Emit()
  click() {
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

.card {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  justify-content: center;
  align-content: center;
  align-items: center;

  border-radius: 12px;
  border-style: solid;
  border-width: 1px;

  cursor: pointer;
}

.theme--light.v-application .card {
  border-color: rgba(map-get($shades, 'black'), 0.2);
}

.theme--dark.v-application .card {
  border-color: rgba(map-get($shades, 'white'), 0.2);
}
</style>
