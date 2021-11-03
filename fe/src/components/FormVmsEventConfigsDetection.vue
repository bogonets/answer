<i18n lang="yaml">
en:
  labels:
    model: "Model"
    checkpoint: "Checkpoint"
    labels: "Labels"
    threshold: "Threshold"
  hints:
    model: "You can choose which model to use for object detection."
    checkpoint: "You can select checkpoints for weights to use for your model."
    labels: "You can select multiple objects to detect."
    threshold: "The larger the threshold value, the more accurate objects are detected."
  tools:
    clear: "Clear selection"
    selection: "Selection"
  no_matching: "No results matching \"{search}\". Press {key} to create a new one."

ko:
  labels:
    model: "모델"
    checkpoint: "체크포인트"
    labels: "라벨"
    threshold: "임계점"
  hints:
    model: "객체 감지에 사용할 모델을 선택할 수 있습니다."
    checkpoint: "모델에 사용할 가중치의 체크포인트를 선택할 수 있습니다."
    labels: "감지할 객체를 여러 개 선택할 수 있습니다."
    threshold: "임계점 값이 클 수록, 보다 정확도가 높은 객체만 탐지합니다."
  tools:
    clear: "영역 해제"
    selection: "영역 선택"
  no_matching: "\"{search}\" 와 일치하는 결과가 없습니다. {key} 키를 눌러 추가할 수 있습니다."
</i18n>

<template>
  <v-container fluid>
    <v-row>
      <v-col
          cols="12"
          sm="12"
          md="5"
          lg="4"
          xl="3"
      >
        <p :class="subtitleClass">{{ $t('labels.model') }}</p>
        <v-select
            dense
            outlined
            persistent-hint
            disabled
            :value="model"
            @input="inputModel"
            :items="models"
            :hint="$t('hints.model')"
        ></v-select>

        <p :class="subtitleClass">{{ $t('labels.checkpoint') }}</p>
        <v-select
            dense
            outlined
            persistent-hint
            disabled
            :value="checkpoint"
            @input="inputCheckpoint"
            :items="checkpoints"
            :hint="$t('hints.checkpoint')"
        ></v-select>

        <p :class="subtitleClass">{{ $t('labels.labels') }}</p>
        <v-combobox
            dense
            hide-selected
            multiple
            small-chips
            persistent-hint
            disabled
            :value="label"
            @input="inputLabel"
            :items="labels"
            :hint="$t('hints.labels')"
            :search-input.sync="searchLabel"
        >
          <template v-slot:no-data>
            <p>
              <i18n :class="captionClass" path="no_matching" tag="span">
                <template #search>
                  <strong>{{ searchLabel }}</strong>
                </template>
                <template #key>
                  <kbd>enter</kbd>
                </template>
              </i18n>
            </p>
          </template>
        </v-combobox>

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
          md="7"
          lg="8"
          xl="9"
      >
        <media-player
            ref="media-player"
            hover-system-bar
            hide-controller
            :value="device"
            :group="$route.params.group"
            :project="$route.params.project"
            :device="Number.parseInt($route.params.device)"
            :use-annotation-tools="annotationMode"
            @roi="onRoi"
        ></media-player>
        <div class="mt-2 d-flex justify-end">
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
import {Component, Emit, Prop, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MediaPlayer from '@/media/MediaPlayer.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from "@/styles/caption";
import type {VmsDeviceA, VmsEventConfigDetectionQ} from '@/packet/vms';

function createEmptyObject() {
  return {};
}

@Component({
  components: {
    MediaPlayer,
  }
})
export default class FormVmsEventConfigsDetection extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;

  @Prop({type: Number, default: 0})
  readonly minThreshold!: number;

  @Prop({type: Number, default: 100})
  readonly maxThreshold!: number;

  @Prop({type: Object, default: createEmptyObject})
  readonly value!: any;

  @Ref('media-player')
  readonly mediaPlayer!: MediaPlayer;

  loading = false;
  device = {} as VmsDeviceA;

  searchLabel = '';

  // model = '';
  // models = [] as Array<string>;
  models = ['seven-segment'];
  model = this.models[0];

  // checkpoint = '';
  // checkpoints = [] as Array<string>;
  checkpoints = ['seven_segment_20211028_adam.pth'];
  checkpoint = this.checkpoints[0];

  // label = ''
  // labels = [] as Array<string>;
  labels = ['screen'];
  label = [this.labels[0]];

  threshold = 50;
  x1 = 0;
  y1 = 0;
  x2 = 0;
  y2 = 0;

  annotationMode = false;

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
    return {
      model: this.model,
      checkpoint: this.checkpoint,
      label: this.label,
      threshold: this.thresholdPercentage,
      x1: this.x1,
      y1: this.y1,
      x2: this.x2,
      y2: this.y2,
    } as VmsEventConfigDetectionQ;
  }

  requestEventDetection() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const body = this.getExtra();
    this.loading = true;
    this.$api2.postVmsDeviceProcessDebugEventDetection(group, project ,device, body)
        .then(() => {
          this.loading = false;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        })
  }

  create() {
    this.requestModels();
  }

  requestModels() {
  }

  inputModel(event: string) {
    this.model = event;
    this.requestEventDetection();
    this.input();
  }

  inputCheckpoint(event: string) {
    this.checkpoint = event;
    this.requestEventDetection();
    this.input();
  }

  inputLabel(event: Array<string>) {
    this.label = event;
    this.requestEventDetection();
    this.input();
  }

  @Emit()
  input() {
    this.value.model = this.model;
    this.value.checkpoint = this.checkpoint;
    this.value.label = this.label;
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
    const valid1 = !!(this.model && this.checkpoint && this.label);
    const valid2 = !!(this.x1 && this.y1 && this.x2 && this.y2);
    return valid1 && valid2;
  }

  onChangeThreshold(value: number) {
    this.requestEventDetection();
    this.input();
  }

  onClickClear() {
    this.x1 = 0;
    this.y1 = 0;
    this.x2 = 0;
    this.y2 = 0;
    this.mediaPlayer.clearAnnotations();
    this.requestEventDetection();
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

  onRoi(roi) {
    this.x1 = roi.x1;
    this.y1 = roi.y1;
    this.x2 = roi.x2;
    this.y2 = roi.y2;
    this.annotationMode = false;
    // console.debug(`onRoi -> x1=${roi.x1},y1=${roi.y1},x2=${roi.x2},y2=${roi.y2}`);
    this.requestEventDetection();
    this.input();
  }
}
</script>
