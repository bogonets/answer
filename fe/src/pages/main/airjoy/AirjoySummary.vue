<template>
  <view-port class="airjoy-summary">
    <div :class="themeClass">
      <div class="d-block text-center">
        <h1 class="preview-text">
          {{ items[index] }}
        </h1>
      </div>
    </div>
    <div class="control-panel">
      <v-select
          dark
          dense
          rounded
          flat
          outlined
          hide-details
          :items="items"
          :value="items[index]"
          @change="onChangeTheme"
      >
      </v-select>
    </div>
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
export default class AirjoySummary extends VueBase {
  items = ['Good', 'Normal', 'Warning', 'Danger'];
  index = 0;

  get themeClass() {
    switch (this.index) {
      case 0:
        return 'good-background';
      case 1:
        return 'normal-background';
      case 2:
        return 'warning-background';
      case 3:
        return 'danger-background';
      default:
        return 'unknown-background';
    }
  }

  onChangeTheme(item: string) {
    console.log(item);
    this.index = this.items.indexOf(item);
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

$gradient-angle: -45deg;

$background-width: 400%;
$background-height: 400%;

$animation-duration: 15s;

@keyframes background-position-gradient {
  0% {
    background-position: 0 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0 50%;
  }
}

@mixin flex-center {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-content: center;
  justify-content: center;
  align-items: center;
}

@mixin view-size {
  width: 100%;
  height: 100%;
}

@mixin gradient-background($color-name) {
  background: repeating-linear-gradient(
          $gradient-angle,
          map-deep-get($colors, $color-name, 'lighten-5'),
          map-deep-get($colors, $color-name, 'lighten-4'),
          map-deep-get($colors, $color-name, 'lighten-3'),
          map-deep-get($colors, $color-name, 'lighten-2'),
          map-deep-get($colors, $color-name, 'lighten-1'),
          map-deep-get($colors, $color-name, 'darken-1'),
          map-deep-get($colors, $color-name, 'darken-2'),
          map-deep-get($colors, $color-name, 'darken-3'),
  );
  background-size: $background-width $background-height;
  animation: background-position-gradient $animation-duration ease infinite;
}

.good-background {
  @include view-size;
  @include flex-center;
  @include gradient-background('blue');
}

.normal-background {
  @include view-size;
  @include flex-center;
  @include gradient-background('green');
}

.warning-background {
  @include view-size;
  @include flex-center;
  @include gradient-background('amber');
}

.danger-background {
  @include view-size;
  @include flex-center;
  @include gradient-background('deep-orange');
}

.unknown-background {
  @include view-size;
  @include flex-center;
  @include gradient-background('blue-grey');
}

.control-panel {
  position: absolute;
  right: 12px;
  bottom: 12px;
}

.theme--light.v-application .airjoy-summary {
  .preview-text {
    color: map-get($shades, 'white');
  }
}

.theme--dark.v-application .airjoy-summary {
  .preview-text {
    color: map-get($shades, 'white');
  }
}
</style>
