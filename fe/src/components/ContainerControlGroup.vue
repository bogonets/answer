<i18n lang="yaml">
en:
  start: "Start"
  stop: "Stop"
  kill: "Kill"
  restart: "Restart"
  pause: "Pause"
  resume: "Resume"
  remove: "Remove"

ko:
  start: "Start"
  stop: "Stop"
  kill: "Kill"
  restart: "Restart"
  pause: "Pause"
  resume: "Resume"
  remove: "Remove"
</i18n>

<template>
  <div class="control-button-group">
    <v-btn
        class="control-button-group--left control-button-group--select"
        elevation="0"
        tile
        color="green"
        :disabled="disabledStart"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="start"
    >
      <v-icon :left="leftIcon">mdi-play</v-icon>
      <span v-if="showButtonText">
        {{ $t('start') }}
      </span>
    </v-btn>
    <v-btn
        class="control-button-group--center"
        elevation="0"
        tile
        color="red"
        :disabled="disabledStop"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="stop"
    >
      <v-icon :left="leftIcon">mdi-stop</v-icon>
      <span v-if="showButtonText">
        {{ $t('stop') }}
      </span>
    </v-btn>
    <v-btn
        class="control-button-group--center"
        elevation="0"
        tile
        color="red"
        :disabled="disabledKill"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="kill"
    >
      <v-icon :left="leftIcon">mdi-bomb</v-icon>
      <span v-if="showButtonText">
        {{ $t('kill') }}
      </span>
    </v-btn>
    <v-btn
        class="control-button-group--center"
        elevation="0"
        tile
        color="blue"
        :disabled="disabledRestart"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="restart"
    >
      <v-icon :left="leftIcon">mdi-cached</v-icon>
      <span v-if="showButtonText">
        {{ $t('restart') }}
      </span>
    </v-btn>
    <v-btn
        class="control-button-group--center"
        elevation="0"
        tile
        color="blue"
        :disabled="disabledPause"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="pause"
    >
      <v-icon :left="leftIcon">mdi-pause</v-icon>
      <span v-if="showButtonText">
        {{ $t('pause') }}
      </span>
    </v-btn>
    <v-btn
        class="control-button-group--center"
        elevation="0"
        tile
        color="light-green"
        :disabled="disabledResume"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="resume"
    >
      <v-icon :left="leftIcon">mdi-play</v-icon>
      <span v-if="showButtonText">
        {{ $t('resume') }}
      </span>
    </v-btn>
    <v-btn
        class="control-button-group--right"
        elevation="0"
        tile
        color="red"
        :disabled="disabledRemove"
        :x-small="xSmall"
        :small="small"
        :large="large"
        :x-large="xLarge"
        :outlined="outlined"
        @click.stop="remove"
    >
      <v-icon :left="leftIcon">mdi-delete</v-icon>
      <span v-if="showButtonText">
        {{ $t('remove') }}
      </span>
    </v-btn>
  </div>
</template>

<script lang="ts">
import {Component, Prop, Emit} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';

@Component
export default class ContainerControlGroup extends VueBase {
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

  @Prop({type: Boolean, default: false})
  readonly disabledStart!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disabledStop!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disabledKill!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disabledRestart!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disabledPause!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disabledResume!: boolean;

  @Prop({type: Boolean, default: false})
  readonly disabledRemove!: boolean;

  get leftIcon() {
    return this.$vuetify.breakpoint.mdAndUp;
  }

  get showButtonText() {
    return this.$vuetify.breakpoint.mdAndUp;
  }

  @Emit('click:start')
  start() {
  }

  @Emit('click:stop')
  stop() {
  }

  @Emit('click:kill')
  kill() {
  }

  @Emit('click:restart')
  restart() {
  }

  @Emit('click:pause')
  pause() {
  }

  @Emit('click:resume')
  resume() {
  }

  @Emit('click:remove')
  remove() {
  }
}
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/styles.sass';

$edge-rounded: 12px;
$edge-rounded-inside: $edge-rounded - 1px;

.control-button-group {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;

  border-radius: $edge-rounded;

  .control-button-group--left {
    border-radius: $edge-rounded-inside 0 0 $edge-rounded-inside;
    border-width: 1px 0 1px 1px;
    border-style: solid;
  }

  .control-button-group--center {
    border-radius: 0;
    border-width: 1px 0 1px 0;
    border-style: solid;
  }

  .control-button-group--right {
    border-radius: 0 $edge-rounded-inside $edge-rounded-inside 0;
    border-width: 1px 1px 1px 0;
    border-style: solid;
  }
}

.theme--light.v-application .control-button-group {
  .control-button-group--left {
    border-color: rgba(map-get($shades, 'black'), 0.2);
  }

  .control-button-group--center {
    border-color: rgba(map-get($shades, 'black'), 0.2);
  }

  .control-button-group--right {
    border-color: rgba(map-get($shades, 'black'), 0.2);
  }

  .v-icon {
    color: rgba(map-get($shades, 'black'), 0.6);
  }
}

.theme--dark.v-application .control-button-group {
  .control-button-group--left {
    border-color: rgba(map-get($shades, 'white'), 0.2);
  }

  .control-button-group--center {
    border-color: rgba(map-get($shades, 'white'), 0.2);
  }

  .control-button-group--right {
    border-color: rgba(map-get($shades, 'white'), 0.2);
  }

  .v-icon {
    color: rgba(map-get($shades, 'white'), 0.6);
  }
}
</style>
