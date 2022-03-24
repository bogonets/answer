<i18n lang="yaml">
en:
  vp: "VP"

ko:
  vp: "VP"
</i18n>

<template>
  <view-port>
  </view-port>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import ViewPort from '@/components/ViewPort.vue';

@Component({
  components: {
    ViewPort,
  }
})
export default class MainVisualProgramming extends VueBase {
}
</script>

<style lang="scss" scoped>
</style>
