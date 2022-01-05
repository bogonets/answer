<i18n lang="yaml">
en:
  labels:
    distance: "Distance"
    threshold: "Threshold"
    operator: "Operator"
    emit_condition: "Emit Condition"
    train_image: "Train Image"
    query_image: "Query Image"
    snapshots: "Snapshots"
    true: "True"
    false: "False"
  hints:
    distance: >
      Hamming distance. The higher the value, the more feature points.
    threshold: >
      The higher the threshold value, the more exact the similarity must be.
    operator: >
      An event is raised when the result
      of the comparison operation becomes {0}.
    emit_condition: >
      An event is emitted when the result
      of the comparison operation becomes {condition}.
    snapshots: "You can select an existing snapshot."
  tools:
    snapshot: "Snapshot"
    clear: "Clear selection"
    selection: "Selection"
    copy: "Copy"

ko:
  labels:
    distance: "거리 임계점"
    threshold: "임계점"
    operator: "비교 연산자"
    emit_condition: "방출 조건"
    train_image: "기준 이미지"
    query_image: "비교 대상"
    snapshots: "스냅샷"
    true: "참"
    false: "거짓"
  hints:
    distance: "해밍 거리 (Hamming distance) 임계점. 값이 클 수록, 특징점이 많아집니다."
    threshold: "임계점 값이 클 수록, 유사도가 정확히 일치해야 합니다."
    operator: "비교 연산 결과가 {0}이 되면 이벤트가 발생됩니다."
    emit_condition: "비교 연산 결과가 {condition}이 되면 이벤트가 방출됩니다."
    snapshots: "기존에 사용한 스냅샷을 선택할 수 있습니다."
  tools:
    snapshot: "캡쳐"
    clear: "영역 해제"
    selection: "영역 선택"
    copy: "영역 복사"
</i18n>

<template>
  <v-container fluid>
    <v-row>
      <v-col
          cols="12"
          sm="6"
          md="6"
          lg="6"
          xl="6"
      >
        <p :class="subtitleClass">{{ $t('labels.train_image') }}</p>
        <v-card
            outlined
            tile
            ref="train-content"
            class="train-content"
            height="300px"
        >
          <div class="media-content">
            <canvas
                class="train-canvas"
                ref="train-canvas"
                :width="videoWidth"
                :height="videoHeight"
                @mousedown="onMouseDownTrainCanvas"
                @mousemove="onMouseMoveTrainCanvas"
                @mouseup="onMouseUpTrainCanvas"
            ></canvas>
            <canvas
                v-show="false"
                class="train-snap"
                ref="train-snap"
                :width="videoWidth"
                :height="videoHeight"
            ></canvas>
            <img
                class="train-image"
                ref="train-image"
                :src="snapshotDataUrl"
            />
          </div>
        </v-card>

        <div class="mt-2 d-flex justify-start">
          <v-btn small rounded class="mr-2" @click="onClickTrainClear">
            <v-icon left>mdi-close</v-icon>
            {{ $t('tools.clear') }}
          </v-btn>
          <v-btn
              small
              rounded
              class="mr-2"
              :color="trainSelectionButtonColor"
              @click="onClickTrainSelection"
          >
            <v-icon left>mdi-selection-drag</v-icon>
            {{ $t('tools.selection') }}
          </v-btn>
          <v-btn small rounded @click="onClickSelectionCopy">
            <v-icon left>mdi-vector-selection</v-icon>
            {{ $t('tools.copy') }}
          </v-btn>
        </div>

        <p :class="subtitleClass">{{ $t('labels.snapshots') }}</p>
        <v-select
            dense
            outlined
            persistent-hint
            :value="snapshotName"
            @input="onInputSnapshot"
            append-outer-icon="mdi-delete"
            @click:append-outer="onClickRemoveSnapshot"
            :items="snapshotNames"
            :hint="$t('hints.snapshots')"
        ></v-select>

        <v-slider
            class="mt-2"
            persistent-hint
            thumb-label
            v-model="distance"
            :min="minDistance"
            :max="maxDistance"
            :label="$t('labels.distance')"
            :hint="$t('hints.distance')"
            @change="onChangeDistance"
        ></v-slider>

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

        <v-select
            v-if="showOperator"
            class="mt-2"
            dense
            persistent-hint
            v-model="operator"
            :items="operators"
            :hint="$t('hints.operator', [emitConditionText])"
            @change="onChangeOperator"
        ></v-select>

        <div class="d-flex flex-column mt-2">
          <div class="d-flex flex-row align-center">
            <span class="text-body-1 text--secondary">
              {{ $t('labels.emit_condition') }}
            </span>
            <v-spacer></v-spacer>
            <v-switch
                class="mt-0"
                dense
                inset
                v-model="emitCondition"
                hide-details
            ></v-switch>
          </div>
          <i18n
              class="text-caption text--secondary mt-1"
              path="hints.emit_condition"
              tag="span"
          >
            <template #condition>
              <strong :class="emitConditionClass">{{ emitConditionText }}</strong>
            </template>
          </i18n>
        </div>

      </v-col>

      <v-col
          cols="12"
          sm="6"
          md="6"
          lg="6"
          xl="6"
      >
        <p :class="subtitleClass">{{ $t('labels.query_image') }}</p>
        <div
            ref="media-player-placeholder"
        >
          <media-player
              ref="media-player"
              hover-system-bar
              hide-controller
              height="300px"
              :value="device"
              :group="$route.params.group"
              :project="$route.params.project"
              :device="$route.params.device"
              :use-annotation-tools="annotationMode"
              :use-roi-absolute-position="useRoiAbsolutePosition"
              @roi="onRoi"
              @video:resize="onVideoResize"
          ></media-player>
        </div>
        <div class="mt-2 d-flex justify-end">
          <v-btn small rounded class="mr-2" @click="onClickSnapshot">
            <v-icon left>mdi-camera-iris</v-icon>
            {{ $t('tools.snapshot') }}
          </v-btn>
          <v-btn small rounded class="mr-2" @click="onClickClear">
            <v-icon left>mdi-close</v-icon>
            {{ $t('tools.clear') }}
          </v-btn>
          <v-btn small rounded :color="selectionButtonColor" @click="onClickSelection">
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
import {VImg} from 'vuetify/lib/components/VImg';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from "@/styles/caption";
import type {
  VmsDeviceA,
  VmsEventConfigMatchingQ,
} from '@/packet/vms';
import {imageDataUrlToVmsUploadImageQ} from '@/packet/vms';

function createEmptyObject() {
  return {};
}

@Component({
  components: {
    MediaPlayer,
  }
})
export default class FormVmsEventConfigsMatching extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;

  readonly operators = [
    '=',
    '!=',
    '>',
    '<',
    '>=',
    '<=',
  ];

  @Prop({type: Boolean})
  readonly showOperator!: boolean;

  @Prop({type: Number, default: 0})
  readonly minDistance!: number;

  @Prop({type: Number, default: 100})
  readonly maxDistance!: number;

  @Prop({type: Number, default: 0})
  readonly minThreshold!: number;

  @Prop({type: Number, default: 100})
  readonly maxThreshold!: number;

  @Prop({type: Boolean})
  readonly useRoiAbsolutePosition!: boolean;

  @Prop({type: Object, default: createEmptyObject})
  readonly value!: any;

  @Prop({type: Boolean, default: false})
  readonly valid!: boolean;

  @Ref('train-canvas')
  readonly canvasTrain!: HTMLCanvasElement;

  @Ref('train-snap')
  readonly canvasSnap!: HTMLCanvasElement;

  @Ref('media-player')
  readonly mediaPlayer!: MediaPlayer;

  @Ref('train-content')
  readonly trainContent!: HTMLDivElement;

  @Ref('train-image')
  readonly trainImage!: VImg;

  @Ref('media-player-placeholder')
  readonly mediaPlayerPlaceholder!: HTMLDivElement;

  loading = false;
  device = {} as VmsDeviceA;

  snapshotNames = [] as Array<string>;
  snapshotName = '';

  videoWidth = 0;
  videoHeight = 0;

  uploading = false;
  snapshotDataUrl = '';

  trainRoiLeft = 0;
  trainRoiRight = 0;
  trainRoiTop = 0;
  trainRoiBottom = 0;
  trainRoiButtonPressed = false;
  enableTrainAnnotation = false;

  distance = 50;
  threshold = 50;
  operator = '>=';
  emitCondition = true;

  trainX1 = 0;
  trainY1 = 0;
  trainX2 = 0;
  trainY2 = 0;

  x1 = 0;
  y1 = 0;
  x2 = 0;
  y2 = 0;

  annotationMode = false;

  created() {
    this.setup();
  }

  updateVideoSize() {
    if (this.videoWidth && this.videoHeight) {
      this.onVideoResize({
        width: this.videoWidth,
        height: this.videoHeight,
      });
    }
  }

  setup() {
    this.loading = true;
    (async () => {
      await this.requestSetup();
    })();
  }

  async requestSetup() {
    try {
      const group = this.$route.params.group;
      const project = this.$route.params.project;
      const device = this.$route.params.device;

      this.snapshotNames = await this.$api2.getVmsDeviceProcessDebugEventMatchingTrainSnapshots(
          group, project, device
      );

      const body = this.getExtra();
      await this.$api2.postVmsDeviceProcessDebugEventMatching(
          group, project, device, body
      );
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  get distancePercentage() {
    const min = this.minDistance;
    const max = this.maxDistance;
    const distance = this.distance;
    console.assert(min >= 0);
    console.assert(max > min);
    console.assert(min <= distance && distance <= max);
    const x = Math.abs(distance - min);
    const width = Math.abs(max - min);
    return x / width;
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

  get emitConditionText() {
    if (this.emitCondition) {
      return this.$t('labels.true');
    } else {
      return this.$t('labels.false');
    }
  }

  get emitConditionClass() {
    if (this.emitCondition) {
      return 'green--text';
    } else {
      return 'red--text';
    }
  }

  getExtra() {
    return {
      train_image_uuid: this.snapshotName,
      train_x1: this.trainX1,
      train_y1: this.trainY1,
      train_x2: this.trainX2,
      train_y2: this.trainY2,
      distance: this.distancePercentage,
      threshold: this.thresholdPercentage,
      operator: this.operator,
      emit_condition: this.emitCondition,
      x1: this.x1,
      y1: this.y1,
      x2: this.x2,
      y2: this.y2,
    } as VmsEventConfigMatchingQ;
  }

  requestEventMatching() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const body = this.getExtra();
    this.loading = true;
    this.$api2.postVmsDeviceProcessDebugEventMatching(group, project, device, body)
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
    this.value.train_image_uuid = this.snapshotName;
    this.value.train_x1 = this.trainX1;
    this.value.train_y1 = this.trainY1;
    this.value.train_x2 = this.trainX2;
    this.value.train_y2 = this.trainY2;
    this.value.distance = this.distancePercentage;
    this.value.threshold = this.thresholdPercentage;
    this.value.operator = this.operator;
    this.value.emit_condition = this.emitCondition;
    this.value.x1 = this.x1;
    this.value.y1 = this.y1;
    this.value.x2 = this.x2;
    this.value.y2 = this.y2;
    this.updateValid();
    return this.value;
  }

  @Emit('update:valid')
  updateValid() {
    const valid1 = !!this.trainX1 && !!this.trainY1 && !!this.trainX2 && !!this.trainY2;
    const valid2 = !!this.x1 && !!this.y1 && !!this.x2 && !!this.y2;
    return !!this.snapshotName && valid1 && valid2;
  }

  onInputSnapshot(value: string) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;

    this.loading = true;
    this.$api2.getVmsDeviceProcessDebugEventMatchingTrainSnapshotsPsnapshot(
        group, project, device, value
    )
        .then(item => {
          this.loading = false;
          this.snapshotDataUrl = `data:${item.content_type};${item.encoding},${item.content}`;
          this.snapshotName = value;
          this.updateVideoSize();

          // const context = this.canvasSnap.getContext('2d');
          // if (context) {
          //   const img = new Image();
          //   img.src = this.snapshotDataUrl;
          //   context.drawImage(img,0,0);
          // }

          this.requestEventMatching();
          this.input();
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }

  onClickRemoveSnapshot() {
    if (this.snapshotName) {
      const group = this.$route.params.group;
      const project = this.$route.params.project;
      const device = this.$route.params.device;
      const snapshot = this.snapshotName;
      this.$api2.deleteVmsDeviceProcessDebugEventMatchingTrainSnapshotsPsnapshot(
          group, project, device, snapshot
      )
          .then(() => {
            const index = this.snapshotNames.findIndex(n => n === this.snapshotName);
            if (index >= 0) {
              this.snapshotNames.splice(index, 1);
            }
            this.snapshotName = '';
            this.snapshotDataUrl = '';

            this.requestEventMatching();
            this.input();
          })
          .catch(error => {
            this.toastRequestFailure(error);
          });
    }
  }

  onChangeDistance(value: number) {
    this.requestEventMatching();
    this.input();
  }

  onChangeThreshold(value: number) {
    this.requestEventMatching();
    this.input();
  }

  onChangeOperator(value: string) {
    this.requestEventMatching();
    this.input();
  }

  onClickSnapshot() {
    const image = this.mediaPlayer.snapshotVideoAsDataUrl();
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const body = imageDataUrlToVmsUploadImageQ(image);

    this.uploading = true;
    this.$api2.postVmsDeviceProcessDebugEventMatchingTrainSnapshots(
        group, project, device, body
    )
        .then(item => {
          this.uploading = false;
          this.snapshotDataUrl = image;
          this.snapshotNames.push(item.name);
          this.snapshotName = item.name;
          this.updateVideoSize();
        })
        .catch(error => {
          this.uploading = false;
          this.snapshotDataUrl = '';
          this.toastRequestFailure(error);
        });
  }

  onClickClear() {
    this.x1 = 0;
    this.y1 = 0;
    this.x2 = 0;
    this.y2 = 0;
    this.mediaPlayer.clearAnnotations();
    this.requestEventMatching();
    this.input();
  }

  get trainSelectionButtonColor() {
    if (this.enableTrainAnnotation) {
      return 'primary';
    } else {
      return '';
    }
  }

  get selectionButtonColor() {
    if (this.annotationMode) {
      return 'primary';
    } else {
      return '';
    }
  }

  onClickTrainClear() {
    this.trainX1 = 0;
    this.trainY1 = 0;
    this.trainX2 = 0;
    this.trainY2 = 0;

    const context = this.canvasTrain.getContext('2d');
    const width = this.canvasTrain.width;
    const height = this.canvasTrain.height;
    console.debug(`onClickTrainClear(w=${width},h=${height})`);
    if (!context) {
      throw new Error('Not exists 2d context from user-canvas.');
    }
    context.clearRect(0, 0, width, height);

    this.requestEventMatching();
    this.input();
  }

  onClickTrainSelection() {
    this.enableTrainAnnotation = !this.enableTrainAnnotation;
  }

  onClickSelectionCopy() {
    this.trainX1 = this.x1;
    this.trainY1 = this.y1;
    this.trainX2 = this.x2;
    this.trainY2 = this.y2;

    const context = this.canvasTrain.getContext('2d');
    const width = this.canvasTrain.width;
    const height = this.canvasTrain.height;
    if (!context) {
      throw new Error('Not exists 2d context from user-canvas.');
    }

    context.lineWidth = 5;
    context.strokeStyle = 'red';
    context.clearRect(0, 0, width, height);
    if (this.useRoiAbsolutePosition) {
      context.strokeRect(
          this.trainX1,
          this.trainY1,
          this.trainX2 - this.trainX1,
          this.trainY2 - this.trainY1,
      );
    } else {
      context.strokeRect(
          this.trainX1 * width,
          this.trainY1 * height,
          (this.trainX2 - this.trainX1) * width,
          (this.trainY2 - this.trainY1) * height,
      );
    }

    this.requestEventMatching();
    this.input();
  }

  onClickSelection() {
    this.annotationMode = !this.annotationMode;
  }

  onMouseDownTrainCanvas(event: MouseEvent) {
    if (this.enableTrainAnnotation) {
      const clientRect = this.canvasTrain.getBoundingClientRect();
      const x = Math.round(event.clientX - clientRect.left);
      const y = Math.round(event.clientY - clientRect.top);
      const ratioX = x / clientRect.width;
      const ratioY = y / clientRect.height;
      const imageX = Math.round(ratioX * this.canvasTrain.width);
      const imageY = Math.round(ratioY * this.canvasTrain.height);
      this.trainRoiLeft = imageX;
      this.trainRoiTop = imageY;
      this.trainRoiButtonPressed = true;
    }
  }

  onMouseMoveTrainCanvas(event) {
    if (this.enableTrainAnnotation && this.trainRoiButtonPressed) {
      const clientRect = this.canvasTrain.getBoundingClientRect();
      const x = Math.round(event.clientX - clientRect.left);
      const y = Math.round(event.clientY - clientRect.top);
      const ratioX = x / clientRect.width;
      const ratioY = y / clientRect.height;
      const imageX = Math.round(ratioX * this.canvasTrain.width);
      const imageY = Math.round(ratioY * this.canvasTrain.height);

      const context = this.canvasTrain.getContext('2d');
      const width = this.canvasTrain.width;
      const height = this.canvasTrain.height;
      if (!context) {
        throw new Error('Not exists 2d context from user-canvas.');
      }
      const roiWidth = imageX - this.trainRoiLeft;
      const roiHeight = imageY - this.trainRoiTop;
      context.lineWidth = 5;
      context.strokeStyle = 'red';
      context.clearRect(0, 0, width, height);
      context.strokeRect(this.trainRoiLeft, this.trainRoiTop, roiWidth, roiHeight);
    }
  }

  onMouseUpTrainCanvas(event) {
    if (this.enableTrainAnnotation && this.trainRoiButtonPressed) {
      const clientRect = this.canvasTrain.getBoundingClientRect();
      const x = Math.round(event.clientX - clientRect.left);
      const y = Math.round(event.clientY - clientRect.top);
      const ratioX = x / clientRect.width;
      const ratioY = y / clientRect.height;
      const imageX = Math.round(ratioX * this.canvasTrain.width);
      const imageY = Math.round(ratioY * this.canvasTrain.height);

      const context = this.canvasTrain.getContext('2d');
      const width = this.canvasTrain.width;
      const height = this.canvasTrain.height;
      if (!context) {
        throw new Error('Not exists 2d context from user-canvas.');
      }
      const roiWidth = imageX - this.trainRoiLeft;
      const roiHeight = imageY - this.trainRoiTop;
      context.lineWidth = 5;
      context.clearRect(0, 0, width, height);
      context.strokeRect(this.trainRoiLeft, this.trainRoiTop, roiWidth, roiHeight);
      this.trainRoiRight = imageX;
      this.trainRoiBottom = imageY;
      this.trainRoiButtonPressed = false;
      if (this.useRoiAbsolutePosition) {
        this.onTrainRoi(
            this.trainRoiLeft,
            this.trainRoiRight,
            this.trainRoiTop,
            this.trainRoiBottom
        );
      } else {
        this.onTrainRoi(
            this.trainRoiLeft / width,
            this.trainRoiRight / width,
            this.trainRoiTop / height,
            this.trainRoiBottom / height,
        );
      }
    }
  }

  onTrainRoi(left, right, top, bottom) {
    this.trainX1 = left;
    this.trainY1 = top;
    this.trainX2 = right;
    this.trainY2 = bottom;
    this.enableTrainAnnotation = false;
    this.requestEventMatching();
    this.input();
  }

  onRoi(roi) {
    this.x1 = roi.x1;
    this.y1 = roi.y1;
    this.x2 = roi.x2;
    this.y2 = roi.y2;
    this.annotationMode = false;
    // console.debug(`onRoi -> x1=${roi.x1},y1=${roi.y1},x2=${roi.x2},y2=${roi.y2}`);
    this.requestEventMatching();
    this.input();
  }

  onVideoResize({width, height}) {
    console.debug(`onVideoResize(width=${width},height=${height})`);
    this.videoWidth = width;
    this.videoHeight = height;

    // const rect = this.mediaPlayerPlaceholder.getBoundingClientRect();
    // this.trainContent.style.width = `${rect.width}px`;
    // this.trainContent.style.height = `${rect.height}px`;
    // this.trainContent.style.maxWidth = `${rect.width}px`;
    // this.trainContent.style.maxHeight = `${rect.height}px`;
    // this.trainContent.style.minWidth = `${rect.width}px`;
    // this.trainContent.style.minHeight = `${rect.height}px`;
    //
    // this.canvasTrain.style.width = `${rect.width}px`;
    // this.canvasTrain.style.height = `${rect.height}px`;
    // this.canvasTrain.style.maxWidth = `${rect.width}px`;
    // this.canvasTrain.style.maxHeight = `${rect.height}px`;

    // const imgElement = this.trainImage.$el;
    // imgElement.style.width = `${rect.width}px`;
    // imgElement.style.height = `${rect.height}px`;
    // imgElement.style.maxWidth = `${rect.width}px`;
    // imgElement.style.maxHeight = `${rect.height}px`;
  }
}
</script>

<style lang="scss" scoped>
@mixin common-media {
  position: absolute;

  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);

  object-fit: contain;
  object-position: center;

  max-width: 100%;
  max-height: 100%;

  padding: 0;
  margin: 0;
}

.train-content {
  display: flex;

  padding: 0;
  margin: 0;

  background: gray;

  min-width: 100px;
  min-height: 100px;

  .media-content {
    flex: 1;

    padding: 0;
    border: 0;

    .train-canvas {
      @include common-media;
      z-index: 30;
    }

    .train-snap {
      @include common-media;
      z-index: 20;
    }

    .train-image {
      @include common-media;
      z-index: 10;
    }
  }
}
</style>
