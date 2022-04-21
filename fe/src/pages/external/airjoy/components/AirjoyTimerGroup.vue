<i18n lang="yaml">
en:
  cancel: 'Cancel'
  off: 'Off'
  one: '1h'
  two: '2h'
  four: '4h'
  eight: '8h'
  unknown: 'Timer/Unknown'

ko:
  cancel: '예약을 취소합니다'
  off: '예약이 설정되어 있지 않습니다'
  one: '1시간'
  two: '2시간'
  four: '4시간'
  eight: '8시간'
  unknown: '알 수 없는 예약 시간 입니다'
</i18n>

<template>
  <div class="timer-button-group">
    <v-tooltip bottom>
      <template v-slot:activator="{on, attrs}">
        <v-btn
          class="timer-button-group--left timer-button-group--select"
          elevation="0"
          tile
          :color="colorOff"
          :x-small="xSmall"
          :small="small"
          :large="large"
          :x-large="xLarge"
          :outlined="outlined"
          v-bind="attrs"
          v-on="on"
          @click.stop="timerOff"
        >
          <v-icon>mdi-timer-off-outline</v-icon>
        </v-btn>
      </template>
      <span>{{ $t('cancel') }}</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{on, attrs}">
        <v-btn
          class="timer-button-group--center"
          elevation="0"
          tile
          :color="colorOne"
          :x-small="xSmall"
          :small="small"
          :large="large"
          :x-large="xLarge"
          :outlined="outlined"
          v-bind="attrs"
          v-on="on"
          @click.stop="timerOne"
        >
          <v-icon>mdi-clock-time-one-outline</v-icon>
        </v-btn>
      </template>
      <span>{{ $t('one') }}</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{on, attrs}">
        <v-btn
          class="timer-button-group--center"
          elevation="0"
          tile
          :color="colorTwo"
          :x-small="xSmall"
          :small="small"
          :large="large"
          :x-large="xLarge"
          :outlined="outlined"
          v-bind="attrs"
          v-on="on"
          @click.stop="timerTwo"
        >
          <v-icon>mdi-clock-time-two-outline</v-icon>
        </v-btn>
      </template>
      <span>{{ $t('two') }}</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{on, attrs}">
        <v-btn
          class="timer-button-group--center"
          elevation="0"
          tile
          :color="colorFour"
          :x-small="xSmall"
          :small="small"
          :large="large"
          :x-large="xLarge"
          :outlined="outlined"
          v-bind="attrs"
          v-on="on"
          @click.stop="timerFour"
        >
          <v-icon>mdi-clock-time-four-outline</v-icon>
        </v-btn>
      </template>
      <span>{{ $t('four') }}</span>
    </v-tooltip>

    <v-tooltip bottom>
      <template v-slot:activator="{on, attrs}">
        <v-btn
          class="timer-button-group--right"
          elevation="0"
          tile
          :color="colorEight"
          :x-small="xSmall"
          :small="small"
          :large="large"
          :x-large="xLarge"
          :outlined="outlined"
          v-bind="attrs"
          v-on="on"
          @click.stop="timerEight"
        >
          <v-icon>mdi-clock-time-eight-outline</v-icon>
        </v-btn>
      </template>
      <span>{{ $t('eight') }}</span>
    </v-tooltip>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class AirjoyTimerGroup extends VueBase {
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

  @Prop({type: Number, default: -1})
  readonly timer!: number;

  @Prop({type: String, default: 'primary'})
  readonly activeColor!: string;

  @Prop({type: String, default: ''})
  readonly inactiveColor!: string;

  get isOff() {
    return this.timer == 0;
  }

  get isOne() {
    return this.timer == 1;
  }

  get isTwo() {
    return this.timer == 2;
  }

  get isFour() {
    return this.timer == 4;
  }

  get isEight() {
    return this.timer == 8;
  }

  get colorOff() {
    return this.isOff ? this.activeColor : this.inactiveColor;
  }

  get colorOne() {
    return this.isOne ? this.activeColor : this.inactiveColor;
  }

  get colorTwo() {
    return this.isTwo ? this.activeColor : this.inactiveColor;
  }

  get colorFour() {
    return this.isFour ? this.activeColor : this.inactiveColor;
  }

  get colorEight() {
    return this.isEight ? this.activeColor : this.inactiveColor;
  }

  @Emit('click:timer-off')
  timerOff() {}

  @Emit('click:timer-one')
  timerOne() {}

  @Emit('click:timer-two')
  timerTwo() {}

  @Emit('click:timer-four')
  timerFour() {}

  @Emit('click:timer-eight')
  timerEight() {}
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

$edge-rounded: 12px;
$edge-rounded-inside: $edge-rounded - 1px;

.timer-button-group {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;

  .timer-button-group--left {
    border-radius: $edge-rounded-inside 0 0 $edge-rounded-inside;
    border-width: 1px 0 1px 1px;
    border-style: solid;
  }

  .timer-button-group--center {
    border-radius: 0;
    border-width: 1px 0 1px 0;
    border-style: solid;
  }

  .timer-button-group--right {
    border-radius: 0 $edge-rounded-inside $edge-rounded-inside 0;
    border-width: 1px 1px 1px 0;
    border-style: solid;
  }
}

.theme--light.v-application .timer-button-group {
  .timer-button-group--left {
    border-color: rgba(map-get($shades, 'black'), 0.2);
  }

  .timer-button-group--center {
    border-color: rgba(map-get($shades, 'black'), 0.2);
  }

  .timer-button-group--right {
    border-color: rgba(map-get($shades, 'black'), 0.2);
  }

  .v-icon {
    color: rgba(map-get($shades, 'black'), 0.6);
  }
}

.theme--dark.v-application .timer-button-group {
  .timer-button-group--left {
    border-color: rgba(map-get($shades, 'white'), 0.2);
  }

  .timer-button-group--center {
    border-color: rgba(map-get($shades, 'white'), 0.2);
  }

  .timer-button-group--right {
    border-color: rgba(map-get($shades, 'white'), 0.2);
  }

  .v-icon {
    color: rgba(map-get($shades, 'white'), 0.6);
  }
}
</style>
