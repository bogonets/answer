<i18n lang="yaml">
en:
  labels:
    sensitive: "Sensitive"
  hints:
    sensitive: >
      The higher the sensitivity value, the more accurately the colors should match.
  tools:
    pipette: "Pipette"
    clear: "Clear selection"
    selection: "Selection"

ko:
  labels:
    sensitive: "민감도"
  hints:
    sensitive: "민감도 값이 클 수록, 색상과 정확히 일치해야 합니다."
  tools:
    pipette: "스포이드"
    clear: "영역 해제"
    selection: "영역 선택"
</i18n>

<template>
  <v-container fluid>
    <v-row>
      <v-col
          cols="12"
          sm="12"
          md="4"
          lg="3"
          xl="2"
      >
        <v-color-picker
            elevation="1"
            v-model="color"
            dot-size="14"
            mode="rgba"
        ></v-color-picker>
        <v-slider
            class="mt-2"
            persistent-hint
            thumb-label
            v-model="sensitive"
            :min="minSensitive"
            :max="maxSensitive"
            :label="$t('labels.sensitive')"
            :hint="$t('hints.sensitive')"
        ></v-slider>
      </v-col>
      <v-col
          cols="12"
          sm="12"
          md="8"
          lg="9"
          xl="10"
      >
        <media-player
            hover-system-bar
            use-color-picker
            :value="device"
            :group="$route.params.group"
            :project="$route.params.project"
            :device="Number.parseInt($route.params.device)"
        ></media-player>
        <div class="mt-2 d-flex justify-end">
          <v-btn small rounded class="mr-2">
            <v-icon left>mdi-eyedropper-variant</v-icon>
            {{ $t('tools.pipette') }}
          </v-btn>
          <v-btn small rounded class="mr-2">
            <v-icon left>mdi-close</v-icon>
            {{ $t('tools.clear') }}
          </v-btn>
          <v-btn small rounded>
            <v-icon left>mdi-selection-drag</v-icon>
            {{ $t('tools.selection') }}
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component, Emit, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MediaPlayer from '@/media/MediaPlayer.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import type {VmsDeviceA} from '@/packet/vms';
import * as _ from 'lodash';

function createEmptyObject() {
  return {};
}

@Component({
  components: {
    MediaPlayer,
  }
})
export default class FormVmsEventConfigsColor extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly minSensitive = 0;
  readonly maxSensitive = 100;

  @Prop({type: Object, default: createEmptyObject})
  readonly value!: any;

  loading = false;
  device = {} as VmsDeviceA;

  color = '#FF0000';
  sensitive = 50;

  @Emit()
  input() {
    return this.value;
  }
}
</script>
