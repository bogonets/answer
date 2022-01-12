<i18n lang="yaml">
en:
  labels:
    threshold: "Threshold"
    operator: "Operator"
    emit_condition: "Emit Condition"
    true: "True"
    false: "False"
  hints:
    threshold: >
      The higher the threshold value,
      the more accurately the colors should match.
    operator: >
      An event is raised when the result
      of the comparison operation becomes {0}.
    emit_condition: >
      An event is emitted when the result
      of the comparison operation becomes {condition}.
  tools:
    pipette: "Pipette"
    clear: "Clear selection"
    selection: "Selection"

ko:
  labels:
    threshold: "임계점"
    operator: "비교 연산자"
    emit_condition: "방출 조건"
    true: "참"
    false: "거짓"
  hints:
    threshold: "임계점 값이 클 수록, 색상과 정확히 일치해야 합니다."
    operator: "비교 연산 결과가 {0}이 되면 이벤트가 발생됩니다."
    emit_condition: "비교 연산 결과가 {condition}이 되면 이벤트가 방출됩니다."
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
            :min="minThreshold"
            :max="maxThreshold"
            :label="$t('labels.threshold')"
            :hint="$t('hints.threshold')"
            :value="value.threshold"
            @change="onChangeThreshold"
        ></v-slider>
        <v-select
            v-if="showOperator"
            class="mt-2"
            dense
            persistent-hint
            :items="operators"
            :hint="$t('hints.operator', [emitConditionText])"
            :value="value.operator"
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
                :value="value.emit_condition"
                @change="onChangeEmitCondition"
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
            :device="$route.params.device"
            :use-color-picker="pipetteMode"
            :value="device"
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
import {
  EVENT_CONFIG_OPERATOR_DEFAULT,
  EVENT_CONFIG_OPERATORS,
} from '@/packet/vms';
import type {
  VmsEventConfigColorQ,
  VmsDeviceA,
} from '@/packet/vms';
import {rgbToHex, hexToRgb} from '@/color';

@Component({
  components: {
    MediaPlayer,
  }
})
export default class FormVmsEventConfigsColor extends VueBase {
  readonly operators = EVENT_CONFIG_OPERATORS

  @Prop({type: Boolean, default: false})
  readonly showOperator!: boolean;

  @Prop({type: Number, default: 0})
  readonly minThreshold!: number;

  @Prop({type: Number, default: 100})
  readonly maxThreshold!: number;

  @Prop({type: Object, default: () => new Object()})
  readonly device!: VmsDeviceA;

  @Prop({type: Object, default: () => new Object()})
  readonly value!: VmsEventConfigColorQ;

  @Prop({type: Boolean, default: false})
  readonly valid!: boolean;

  @Ref('media-player')
  readonly mediaPlayer!: MediaPlayer;

  loading = false;
  pipetteMode = false;
  annotationMode = false;

  mounted() {
    this.value.red = this.value.red ?? 0;
    this.value.green = this.value.green ?? 0;
    this.value.blue = this.value.blue ?? 0;
    this.value.threshold = this.value.threshold ?? 0;
    this.value.operator = this.value.operator ?? EVENT_CONFIG_OPERATOR_DEFAULT;
    this.value.emit_condition = this.value.emit_condition ?? false;
    this.value.x1 = this.value.x1 ?? 0;
    this.value.y1 = this.value.y1 ?? 0;
    this.value.x2 = this.value.x2 ?? 0;
    this.value.y2 = this.value.y2 ?? 0;

    this.requestEventColor();
    this.updateValid();
  }

  get color() {
    const r = this.value.red || 0;
    const g = this.value.green || 0;
    const b = this.value.blue || 0;
    return rgbToHex(r, g, b);
  }

  // get thresholdPercentage() {
  //   const min = this.minThreshold;
  //   const max = this.maxThreshold;
  //   const threshold = this.value.threshold || 0;
  //   console.assert(min >= 0);
  //   console.assert(max > min);
  //   console.assert(min <= threshold && threshold <= max);
  //   const x = Math.abs(threshold - min);
  //   const width = Math.abs(max - min);
  //   return x / width;
  // }

  get emitConditionText() {
    if (this.value.emit_condition) {
      return this.$t('labels.true');
    } else {
      return this.$t('labels.false');
    }
  }

  get emitConditionClass() {
    if (this.value.emit_condition) {
      return 'green--text';
    } else {
      return 'red--text';
    }
  }

  get pipetteButtonColor() {
    if (this.pipetteMode) {
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

  requestEventColor() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;

    this.loading = true;
    this.$api2.postVmsDeviceProcessDebugEventColor(group, project ,device, this.value)
        .then(() => {
          this.loading = false;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        })
  }

  get validColor() {
    return (0 <= this.value.red && this.value.red <= 255)
        && (0 <= this.value.green && this.value.green <= 255)
        && (0 <= this.value.blue && this.value.blue <= 255);
  }

  get validRoi() {
    return Math.abs(this.value.x2 - this.value.x1) > 0
        && Math.abs(this.value.y2 - this.value.y1) > 0;
  }

  @Emit('update:valid')
  updateValid() {
    return this.validColor && this.validRoi;
  }

  @Emit()
  input() {
    this.requestEventColor();
    this.updateValid();
    return this.value;
  }

  onInputColor(event: string) {
    const color = hexToRgb(event);
    const red = color?.r || 0;
    const green = color?.g || 0;
    const blue = color?.b || 0;

    this.$set(this.value, 'red', red);
    this.$set(this.value, 'green', green);
    this.$set(this.value, 'blue', blue);

    this.input();
  }

  onChangeThreshold(threshold: number) {
    this.$set(this.value, 'threshold', threshold);
    this.input();
  }

  onChangeOperator(operator: string) {
    this.$set(this.value, 'operator', operator);
    this.input();
  }

  onChangeEmitCondition(condition?: boolean) {
    this.$set(this.value, 'emit_condition', !!condition);
    this.input();
  }

  onClickPipette() {
    this.pipetteMode = !this.pipetteMode;
  }

  onClickClear() {
    this.$set(this.value, 'x1', 0);
    this.$set(this.value, 'y1', 0);
    this.$set(this.value, 'x2', 0);
    this.$set(this.value, 'y2', 0);
    this.mediaPlayer.clearAnnotations();
    this.input();
  }

  onClickSelection() {
    this.annotationMode = !this.annotationMode;
  }

  onPipette(color) {
    const red = color?.r || 0;
    const green = color?.g || 0;
    const blue = color?.b || 0;

    this.$set(this.value, 'red', red);
    this.$set(this.value, 'green', green);
    this.$set(this.value, 'blue', blue);

    this.pipetteMode = false;
    this.input();
  }

  onRoi(roi) {
    const x1 = roi.x1 || 0;
    const y1 = roi.y1 || 0;
    const x2 = roi.x2 || 0;
    const y2 = roi.y2 || 0;

    this.$set(this.value, 'x1', x1);
    this.$set(this.value, 'y1', y1);
    this.$set(this.value, 'x2', x2);
    this.$set(this.value, 'y2', y2);

    this.annotationMode = false;
    this.input();
  }
}
</script>
