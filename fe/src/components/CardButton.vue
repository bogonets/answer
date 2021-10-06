<template>
  <div v-ripple class="card" @click="click">
    <slot></slot>
  </div>
</template>

<script lang="ts">
import {Vue, Component, Emit} from 'vue-property-decorator';

@Component
export default class CardButton extends Vue {
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

  height: 120px;

  padding: 24px;
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
