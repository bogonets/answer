<template>
  <div class="fan-button-group">
    <v-btn
        class="fan-button-group--left fan-button-group--select"
        elevation="0"
        tile
        :color="colorWeak"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="fanWeak"
    >
      <v-icon>mdi-fan-speed-1</v-icon>
    </v-btn>
    <v-btn
        class="fan-button-group--center"
        elevation="0"
        tile
        :color="colorMedium"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="fanMedium"
    >
      <v-icon>mdi-fan-speed-2</v-icon>
    </v-btn>
    <v-btn
        class="fan-button-group--right"
        elevation="0"
        tile
        :color="colorHigh"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="fanHigh"
    >
      <v-icon>mdi-fan-speed-3</v-icon>
    </v-btn>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class AirjoyFanSpeedGroup extends VueBase {
  @Prop({type: Boolean, default: false})
  readonly xSmall!: boolean;

  @Prop({type: Boolean, default: false})
  readonly small!: boolean;

  @Prop({type: Boolean, default: false})
  readonly large!: boolean;

  @Prop({type: Boolean, default: false})
  readonly xLarge!: boolean;

  @Prop({type: Boolean, default: false})
  readonly outlined!: boolean;

  @Prop({type: Number, default: 0})
  readonly speed!: number;

  get isWeak() {
    return this.speed == 1;
  }

  get isMedium() {
    return this.speed == 2;
  }

  get isHigh() {
    return this.speed == 3;
  }

  get colorWeak() {
    return this.isWeak ? 'primary' : '';
  }

  get colorMedium() {
    return this.isMedium ? 'primary' : '';
  }

  get colorHigh() {
    return this.isHigh ? 'primary' : '';
  }

  @Emit('click:fan-weak')
  fanWeak() {
  }

  @Emit('click:fan-medium')
  fanMedium() {
  }

  @Emit('click:fan-high')
  fanHigh() {
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

$edge-rounded: 12px;
$edge-rounded-inside: $edge-rounded - 1px;

.fan-button-group {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;

  .fan-button-group--left {
    border-radius: $edge-rounded-inside 0 0 $edge-rounded-inside;
    border-width: 1px 0 1px 1px;
    border-style: solid;
  }

  .fan-button-group--center {
    border-radius: 0;
    border-width: 1px 0 1px 0;
    border-style: solid;
  }

  .fan-button-group--right {
    border-radius: 0 $edge-rounded-inside $edge-rounded-inside 0;
    border-width: 1px 1px 1px 0;
    border-style: solid;
  }
}

.theme--light.v-application .fan-button-group {
  .fan-button-group--left {
    border-color: rgba(map-get($shades, 'black'), 0.2);
  }

  .fan-button-group--center {
    border-color: rgba(map-get($shades, 'black'), 0.2);
  }

  .fan-button-group--right {
    border-color: rgba(map-get($shades, 'black'), 0.2);
  }

  .v-icon {
    color: rgba(map-get($shades, 'black'), 0.6);
  }
}

.theme--dark.v-application .fan-button-group {
  .fan-button-group--left {
    border-color: rgba(map-get($shades, 'white'), 0.2);
  }

  .fan-button-group--center {
    border-color: rgba(map-get($shades, 'white'), 0.2);
  }

  .fan-button-group--right {
    border-color: rgba(map-get($shades, 'white'), 0.2);
  }

  .v-icon {
    color: rgba(map-get($shades, 'white'), 0.6);
  }
}
</style>
