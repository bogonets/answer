<i18n lang="yaml">
en:
  labels:
    threshold: "Threshold"
  hints:
    threshold: >
      The higher the threshold value, the more accurately the colors should match.
  tools:
    pipette: "Pipette"
    clear: "Clear selection"
    selection: "Selection"

ko:
  labels:
    threshold: "임계점"
  hints:
    threshold: "임계점 값이 클 수록, 색상과 정확히 일치해야 합니다."
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
            :value="color"
            @input="onInputColor"
            dot-size="14"
            mode="rgba"
        ></v-color-picker>
        <v-slider
            class="mt-2"
            persistent-hint
            thumb-label
            v-model="threshold"
            :min="minThreshold"
            :max="maxThreshold"
            :label="$t('labels.threshold')"
            :hint="$t('hints.threshold')"
            @change="onChangeThreshold"
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
            ref="media-player"
            hover-system-bar
            hide-controller
            :group="$route.params.group"
            :project="$route.params.project"
            :device="Number.parseInt($route.params.device)"
            :use-color-picker="pipetteMode"
            @pipette="onPipette"
            :use-annotation-tools="annotationMode"
            @roi="onRoi"
        ></media-player>
        <div class="mt-2 d-flex justify-end">
          <v-btn
              small
              rounded
              class="mr-2"
              :color="pipetteButtonColor"
              @click="onClickPipette"
          >
            <v-icon left>mdi-eyedropper-variant</v-icon>
            {{ $t('tools.pipette') }}
          </v-btn>
          <v-btn small rounded class="mr-2" @click="onClickClear">
            <v-icon left>mdi-close</v-icon>
            {{ $t('tools.clear') }}
          </v-btn>
          <v-btn
              small
              rounded
              :color="selectionButtonColor"
              @click="onClickSelection"
          >
            <v-icon left>mdi-selection-drag</v-icon>
            {{ $t('tools.selection') }}
          </v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component, Ref, Emit, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MediaPlayer from '@/media/MediaPlayer.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import type {VmsEventConfigColorQ} from '@/packet/vms';

function createEmptyObject() {
  return {} as VmsEventConfigColorQ;
}

function componentToHex(c: number) {
  const hex = c.toString(16);
  return hex.length == 1 ? '0' + hex : hex;
}

function rgbToHex(r: number, g: number, b: number) {
  return '#' + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

function hexToRgb(hex: string) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16),
  } : undefined;
}

@Component({
  components: {
    MediaPlayer,
  }
})
export default class FormVmsEventConfigsColor extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;

  @Prop({type: Number, default: 0})
  readonly minThreshold!: number;

  @Prop({type: Number, default: 100})
  readonly maxThreshold!: number;

  @Prop({type: Object, default: createEmptyObject})
  readonly value!: VmsEventConfigColorQ;

  @Prop({type: Boolean, default: false})
  readonly valid!: boolean;

  @Ref('media-player')
  readonly mediaPlayer!: MediaPlayer;

  loading = false;

  color = '#FF0000';
  threshold = 50;
  x1 = 0;
  y1 = 0;
  x2 = 0;
  y2 = 0;

  pipetteMode = false;
  annotationMode = false;

  created() {
    // TODO: read `value`, and watching ...
    this.requestEventColor();
  }

  get thresholdPercentage() {
    const min = this.minThreshold;
    const max = this.maxThreshold;
    const threshold = this.threshold;
    console.assert(min >= 0);
    console.assert(max > min);
    console.assert(min <= threshold && threshold <= max);
    const x = Math.abs(threshold - min);
    const width = Math.abs(max - min);
    return x / width;
  }

  getExtra() {
    const red = Number.parseInt(this.color.substr(1, 2), 16);
    const green = Number.parseInt(this.color.substr(3, 2), 16);
    const blue = Number.parseInt(this.color.substr(5, 2), 16);

    return {
      red: red,
      green: green,
      blue: blue,
      threshold: this.thresholdPercentage,
      x1: this.x1,
      y1: this.y1,
      x2: this.x2,
      y2: this.y2,
    } as VmsEventConfigColorQ;
  }

  requestEventColor() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const body = this.getExtra();
    this.loading = true;
    this.$api2.postVmsDeviceProcessDebugEventColor(group, project ,device, body)
        .then(() => {
          this.loading = false;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        })
  }

  @Emit()
  input() {
    const red = Number.parseInt(this.color.substr(1, 2), 16);
    const green = Number.parseInt(this.color.substr(3, 2), 16);
    const blue = Number.parseInt(this.color.substr(5, 2), 16);
    this.value.red = red;
    this.value.green = green;
    this.value.blue = blue;
    this.value.threshold = this.thresholdPercentage;
    this.value.x1 = this.x1;
    this.value.y1 = this.y1;
    this.value.x2 = this.x2;
    this.value.y2 = this.y2;
    this.updateValid();
    return this.value;
  }

  @Emit('update:valid')
  updateValid() {
    return !!this.color && !!this.x1 && !!this.y1 && !!this.x2 && !!this.y2;
  }

  onInputColor(event: string) {
    this.color = event;
    this.requestEventColor();
    this.input();
  }

  onChangeThreshold(value: number) {
    this.requestEventColor();
    this.input();
  }

  get pipetteButtonColor() {
    if (this.pipetteMode) {
      return 'primary';
    } else {
      return '';
    }
  }

  onClickPipette() {
    this.pipetteMode = !this.pipetteMode;
  }

  onClickClear() {
    this.x1 = 0;
    this.y1 = 0;
    this.x2 = 0;
    this.y2 = 0;
    this.mediaPlayer.clearAnnotations();
    this.requestEventColor();
    this.input();
  }

  get selectionButtonColor() {
    if (this.annotationMode) {
      return 'primary';
    } else {
      return '';
    }
  }

  onClickSelection() {
    this.annotationMode = !this.annotationMode;
  }

  onPipette(color) {
    this.color = rgbToHex(color.r, color.g, color.b);
    this.pipetteMode = false;
    this.requestEventColor();
    this.input();
  }

  onRoi(roi) {
    this.x1 = roi.x1;
    this.y1 = roi.y1;
    this.x2 = roi.x2;
    this.y2 = roi.y2;
    this.annotationMode = false;
    // console.debug(`onRoi -> x1=${roi.x1},y1=${roi.y1},x2=${roi.x2},y2=${roi.y2}`);
    this.requestEventColor();
    this.input();
  }
}
</script>
