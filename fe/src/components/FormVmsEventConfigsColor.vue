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
            :min="minSensitive"
            :max="maxSensitive"
            :label="$t('labels.sensitive')"
            :hint="$t('hints.sensitive')"
            @change="onChangeSensitive"
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
            :value="device"
            :group="$route.params.group"
            :project="$route.params.project"
            :device="Number.parseInt($route.params.device)"
            :use-color-picker="pipetteMode"
            @pipette="onPipette"
            :use-annotation-tools="annotationMode"
            @roi="onRoi"
        ></media-player>
        <div class="mt-2 d-flex justify-end">
<!--          <v-btn small rounded class="mr-2" @click="onClickSnapshot">-->
<!--            <v-icon left>mdi-camera-iris</v-icon>-->
<!--            {{ $t('tools.snapshot') }}-->
<!--          </v-btn>-->
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
import type {VmsDeviceA, VmsEventConfigColorQ} from '@/packet/vms';

function createEmptyObject() {
  return {};
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
  readonly minSensitive = 0;
  readonly maxSensitive = 100;

  @Prop({type: Object, default: createEmptyObject})
  readonly value!: any;

  @Ref('media-player')
  readonly mediaPlayer!: MediaPlayer;

  loading = false;
  device = {} as VmsDeviceA;

  color = '#FF0000';
  threshold = 50;

  x1 = 0;
  y1 = 0;
  x2 = 0;
  y2 = 0;

  pipetteMode = false;
  annotationMode = false;

  created() {
    this.requestEventColor();
  }

  requestEventColor() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;

    const red = Number.parseInt(this.color.substr(1, 2), 16);
    const green = Number.parseInt(this.color.substr(3, 2), 16);
    const blue = Number.parseInt(this.color.substr(5, 2), 16);

    const body = {
      red: red,
      green: green,
      blue: blue,
      threshold: this.threshold / this.maxSensitive,
      x1: this.x1,
      y1: this.y1,
      x2: this.x2,
      y2: this.y2,
    } as VmsEventConfigColorQ;

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
    return this.value;
  }

  onInputColor(event: string) {
    this.color = event;
    this.requestEventColor();
  }

  onChangeSensitive(value: number) {
    this.requestEventColor();
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
  }

  onRoi(roi) {
    this.x1 = roi.x1;
    this.y1 = roi.y1;
    this.x2 = roi.x2;
    this.y2 = roi.y2;
    this.annotationMode = false;
    // console.debug(`onRoi -> x1=${roi.x1},y1=${roi.y1},x2=${roi.x2},y2=${roi.y2}`);
    this.requestEventColor();
  }
}
</script>
