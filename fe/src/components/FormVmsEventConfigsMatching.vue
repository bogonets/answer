<i18n lang="yaml">
en:
  labels:
    distance: 'Distance'
    threshold: 'Threshold'
    operator: 'Operator'
    emit_condition: 'Emit Condition'
    train_image: 'Train Image'
    query_image: 'Query Image'
    snapshots: 'Snapshots'
    true: 'True'
    false: 'False'
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
    snapshots: 'You can select an existing snapshot.'
    train_snapshot_alt: 'Train Snapshot'
    logo_alt: 'Answer'
  tools:
    snapshot: 'Snapshot'
    clear: 'Clear selection'
    selection: 'Selection'
    copy: 'Copy'

ko:
  labels:
    distance: '거리 임계점'
    threshold: '임계점'
    operator: '비교 연산자'
    emit_condition: '방출 조건'
    train_image: '기준 이미지'
    query_image: '비교 대상'
    snapshots: '스냅샷'
    true: '참'
    false: '거짓'
  hints:
    distance: '해밍 거리 (Hamming distance) 임계점. 값이 클 수록, 특징점이 많아집니다.'
    threshold: '임계점 값이 클 수록, 유사도가 정확히 일치해야 합니다.'
    operator: '비교 연산 결과가 {0}이 되면 이벤트가 발생됩니다.'
    emit_condition: '비교 연산 결과가 {condition}이 되면 이벤트가 방출됩니다.'
    snapshots: '기존에 사용한 스냅샷을 선택할 수 있습니다.'
    train_snapshot_alt: '훈련 스냅샷'
    logo_alt: 'Answer'
  tools:
    snapshot: '캡쳐'
    clear: '영역 해제'
    selection: '영역 선택'
    copy: '영역 복사'
</i18n>

<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" sm="6" md="6" lg="6" xl="6">
        <p :class="subtitleClass">{{ $t('labels.train_image') }}</p>
        <v-card
          outlined
          tile
          class="train-content"
          ref="train-content"
          :style="`aspect-ratio: ${this.videoWidth}/${this.videoHeight};`"
        >
          <div class="train-placeholder">
            <canvas
              v-show="existsSnapshot"
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
              v-show="existsSnapshot"
              class="train-image"
              ref="train-image"
              :alt="$t('hints.train_snapshot_alt')"
              :src="snapshotDataUrl"
            />
          </div>
          <div v-show="!existsSnapshot" class="brand-logo-container">
            <img
              class="brand-logo"
              src="@/assets/logos/answer-logo-notext.svg"
              :alt="$t('hints.logo_alt')"
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
              @change="onChangeEmit"
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

      <v-col cols="12" sm="6" md="6" lg="6" xl="6">
        <p :class="subtitleClass">{{ $t('labels.query_image') }}</p>
        <div ref="media-player-placeholder">
          <media-player
            ref="media-player"
            hover-system-bar
            hide-controller
            :group="$route.params.group"
            :project="$route.params.project"
            :device="$route.params.device"
            :use-annotation-tools="annotationMode"
            :use-roi-absolute-position="useRoiAbsolutePosition"
            :value="device"
            :event-config="value"
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
import {CAPTION_CLASS} from '@/styles/caption';
import type {VmsDeviceA, VmsEventConfigMatchingQ} from '@/packet/vms';
import {
  EVENT_CONFIG_OPERATOR_DEFAULT,
  EVENT_CONFIG_OPERATORS,
  imageDataUrlToVmsUploadImageQ,
  VmsEventConfigExtra,
} from '@/packet/vms';
import {valueToRatio, ratioToValue} from '@/math/ratio';

function createEmptyObject() {
  return {};
}

@Component({
  components: {
    MediaPlayer,
  },
})
export default class FormVmsEventConfigsMatching extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;
  readonly operators = EVENT_CONFIG_OPERATORS;

  @Prop({type: Boolean, default: false})
  readonly showOperator!: boolean;

  @Prop({type: Number, default: 0})
  readonly minDistance!: number;

  @Prop({type: Number, default: 100})
  readonly maxDistance!: number;

  @Prop({type: Number, default: 50})
  readonly defaultDistance!: number;

  @Prop({type: Number, default: 0})
  readonly minThreshold!: number;

  @Prop({type: Number, default: 100})
  readonly maxThreshold!: number;

  @Prop({type: Number, default: 50})
  readonly defaultThreshold!: number;

  @Prop({type: Boolean, default: false})
  readonly useRoiAbsolutePosition!: boolean;

  @Prop({type: Object, required: true})
  readonly device!: VmsDeviceA;

  @Prop({type: Object, required: true})
  readonly value!: VmsEventConfigMatchingQ;

  @Prop({type: Boolean, required: true})
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

  distance = 0;
  threshold = 0;
  operator = '';
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

  mounted() {
    const defaultDistance = valueToRatio(
      this.defaultDistance,
      this.minDistance,
      this.maxDistance,
    );
    const defaultThreshold = valueToRatio(
      this.defaultThreshold,
      this.minThreshold,
      this.maxThreshold,
    );

    this.value.train_image_uuid = this.value.train_image_uuid ?? '';
    this.value.train_x1 = this.value.train_x1 ?? 0;
    this.value.train_y1 = this.value.train_y1 ?? 0;
    this.value.train_x2 = this.value.train_x2 ?? 0;
    this.value.train_y2 = this.value.train_y2 ?? 0;
    this.value.distance = this.value.distance ?? defaultDistance;
    this.value.threshold = this.value.threshold ?? defaultThreshold;
    this.value.operator = this.value.operator ?? EVENT_CONFIG_OPERATOR_DEFAULT;
    this.value.emit_condition = this.value.emit_condition ?? true;
    this.value.x1 = this.value.x1 ?? 0;
    this.value.y1 = this.value.y1 ?? 0;
    this.value.x2 = this.value.x2 ?? 0;
    this.value.y2 = this.value.y2 ?? 0;

    this.snapshotName = this.value.train_image_uuid;
    this.trainX1 = this.value.train_x1;
    this.trainY1 = this.value.train_y1;
    this.trainX2 = this.value.train_x2;
    this.trainY2 = this.value.train_y2;
    this.distance = ratioToValue(
      this.value.distance,
      this.minDistance,
      this.maxDistance,
    );
    this.threshold = ratioToValue(
      this.value.threshold,
      this.minThreshold,
      this.maxThreshold,
    );
    this.operator = this.value.operator;
    this.emitCondition = this.value.emit_condition;
    this.x1 = this.value.x1;
    this.y1 = this.value.y1;
    this.x2 = this.value.x2;
    this.y2 = this.value.y2;

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

      this.snapshotNames =
        await this.$api2.getVmsDeviceProcessDebugEventMatchingTrainSnapshots(
          group,
          project,
          device,
        );

      const snapshot =
        await this.$api2.getVmsDeviceProcessDebugEventMatchingTrainSnapshotsPsnapshot(
          group,
          project,
          device,
          this.value.train_image_uuid,
        );
      this.snapshotDataUrl = `data:${snapshot.content_type};${snapshot.encoding},${snapshot.content}`;

      await this.$api2.postVmsDeviceProcessDebugEventMatching(
        group,
        project,
        device,
        this.value,
      );
    } catch (error) {
      this.toastRequestFailure(error);
    } finally {
      this.loading = false;
    }
  }

  get existsSnapshot() {
    return !!this.snapshotDataUrl;
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

  requestEventMatching() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.loading = true;
    this.$api2
      .postVmsDeviceProcessDebugEventMatching(group, project, device, this.value)
      .then(() => {
        this.loading = false;
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  @Emit('update:valid')
  updateValid() {
    const valid1 = !!this.trainX1 && !!this.trainY1 && !!this.trainX2 && !!this.trainY2;
    const valid2 = !!this.x1 && !!this.y1 && !!this.x2 && !!this.y2;
    return !!this.snapshotName && valid1 && valid2;
  }

  @Emit()
  input() {
    this.requestEventMatching();
    this.updateValid();
    return this.value;
  }

  onInputSnapshot(value: string) {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;

    this.loading = true;
    this.$api2
      .getVmsDeviceProcessDebugEventMatchingTrainSnapshotsPsnapshot(
        group,
        project,
        device,
        value,
      )
      .then(item => {
        this.loading = false;
        this.snapshotDataUrl = `data:${item.content_type};${item.encoding},${item.content}`;
        this.snapshotName = value;
        this.value.train_image_uuid = value;

        // const context = this.canvasSnap.getContext('2d');
        // if (context) {
        //   const img = new Image();
        //   img.src = this.snapshotDataUrl;
        //   context.drawImage(img,0,0);
        // }

        this.updateVideoSize();
        this.input();
      })
      .catch(error => {
        this.loading = false;
        this.toastRequestFailure(error);
      });
  }

  onClickRemoveSnapshot() {
    if (!this.snapshotName) {
      return;
    }

    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const snapshot = this.snapshotName;
    this.$api2
      .deleteVmsDeviceProcessDebugEventMatchingTrainSnapshotsPsnapshot(
        group,
        project,
        device,
        snapshot,
      )
      .then(() => {
        const index = this.snapshotNames.findIndex(n => n === this.snapshotName);
        if (index >= 0) {
          this.snapshotNames.splice(index, 1);
        }
        this.snapshotDataUrl = '';
        this.snapshotName = '';
        this.value.train_image_uuid = '';
        this.input();
      })
      .catch(error => {
        this.toastRequestFailure(error);
      });
  }

  onChangeDistance(value: number) {
    this.value.distance = valueToRatio(value, this.minDistance, this.maxDistance);
    this.input();
  }

  onChangeThreshold(value: number) {
    this.value.threshold = valueToRatio(value, this.minThreshold, this.maxThreshold);
    this.input();
  }

  onChangeOperator(value: string) {
    this.value.operator = value;
    this.input();
  }

  onChangeEmit(value?: boolean) {
    this.value.emit_condition = !!value;
    this.input();
  }

  onClickSnapshot() {
    const image = this.mediaPlayer.snapshotAsDataUrl();
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    const body = imageDataUrlToVmsUploadImageQ(image);

    this.uploading = true;
    this.$api2
      .postVmsDeviceProcessDebugEventMatchingTrainSnapshots(
        group,
        project,
        device,
        body,
      )
      .then(item => {
        this.uploading = false;
        this.snapshotDataUrl = image;
        this.snapshotNames.push(item.name);
        this.snapshotName = item.name;
        this.value.train_image_uuid = item.name;
        this.updateVideoSize();
        this.input();
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
    this.value.x1 = 0;
    this.value.y1 = 0;
    this.value.x2 = 0;
    this.value.y2 = 0;
    this.mediaPlayer.clearAnnotations();
    this.input();
  }

  onClickTrainClear() {
    this.trainX1 = 0;
    this.trainY1 = 0;
    this.trainX2 = 0;
    this.trainY2 = 0;
    this.value.train_x1 = 0;
    this.value.train_y1 = 0;
    this.value.train_x2 = 0;
    this.value.train_y2 = 0;

    const context = this.canvasTrain.getContext('2d');
    if (context) {
      const width = this.canvasTrain.width;
      const height = this.canvasTrain.height;
      context.clearRect(0, 0, width, height);
    } else {
      console.error('Not exists 2d context from user-canvas');
    }

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
    this.value.train_x1 = this.x1;
    this.value.train_y1 = this.y1;
    this.value.train_x2 = this.x2;
    this.value.train_y2 = this.y2;

    const context = this.canvasTrain.getContext('2d');
    const width = this.canvasTrain.width;
    const height = this.canvasTrain.height;
    if (context) {
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
    } else {
      console.error('Not exists 2d context from user-canvas');
    }

    this.input();
  }

  onClickSelection() {
    this.annotationMode = !this.annotationMode;
  }

  updateEventConfig() {
    if (!(this.trainX1 && this.trainY1 && this.trainX2 && this.trainY2)) {
      return;
    }
    const context = this.canvasTrain.getContext('2d');
    if (!context) {
      return;
    }
    const width = this.canvasTrain.width;
    const height = this.canvasTrain.height;
    if (!(width && height)) {
      return;
    }

    this.trainRoiLeft = this.trainX1 * width;
    this.trainRoiRight = this.trainX2 * width;
    this.trainRoiTop = this.trainY1 * height;
    this.trainRoiBottom = this.trainY2 * height;

    const roiWidth = this.trainRoiRight - this.trainRoiLeft;
    const roiHeight = this.trainRoiBottom - this.trainRoiTop;

    context.lineWidth = 5;
    context.strokeStyle = 'red';
    context.clearRect(0, 0, width, height);
    context.strokeRect(this.trainRoiLeft, this.trainRoiTop, roiWidth, roiHeight);
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
          this.trainRoiBottom,
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
    this.value.train_x1 = left;
    this.value.train_y1 = top;
    this.value.train_x2 = right;
    this.value.train_y2 = bottom;
    this.enableTrainAnnotation = false;
    this.input();
  }

  onRoi(roi) {
    this.x1 = roi.x1;
    this.y1 = roi.y1;
    this.x2 = roi.x2;
    this.y2 = roi.y2;
    this.value.x1 = roi.x1;
    this.value.y1 = roi.y1;
    this.value.x2 = roi.x2;
    this.value.y2 = roi.y2;
    this.annotationMode = false;
    // console.debug(`onRoi -> x1=${roi.x1},y1=${roi.y1},x2=${roi.x2},y2=${roi.y2}`);
    this.input();
  }

  onVideoResize({width, height}) {
    // console.debug(`onVideoResize(width=${width},height=${height})`);
    this.videoWidth = width;
    this.videoHeight = height;

    this.$nextTick(() => {
      this.updateEventConfig();
    });
  }
}
</script>

<style lang="scss" scoped>
@mixin common-media {
  position: absolute;

  padding: 0;
  margin: 0;

  width: 100%;
  height: 100%;

  object-fit: contain;
  object-position: center;
}

.train-content {
  // Important:
  // Required to fix the position of the 'absolute block' among the child elements.
  // https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block
  position: relative;

  display: flex;

  padding: 0;
  margin: 0;
  border: 0;

  min-width: 64px;
  min-height: 64px;

  background: gray;

  .train-placeholder {
    padding: 0;
    margin: 0;

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

  .brand-logo-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;

    width: 100%;
    height: 100%;

    padding: 0;
    margin: 0;

    .brand-logo {
      min-width: 8px;
      min-height: 8px;

      max-width: 256px;
      max-height: 256px;
    }
  }
}
</style>
