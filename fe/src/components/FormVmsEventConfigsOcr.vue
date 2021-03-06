<i18n lang="yaml">
en:
  labels:
    model: "Model"
    checkpoint: "Checkpoint"
    threshold: "Threshold"
    filter: "Filter ({0})"
  hints:
    model: "You can choose which model to use for object detection."
    checkpoint: "You can select checkpoints for weights to use for your model."
    threshold: "The larger the threshold value, the more accurate objects are detected."
  title:
    filter: "Filter"
  subtitle:
    filter: "Set the conditions to filter the OCR results."
  tools:
    clear: "Clear selection"
    selection: "Selection"
  no_matching: "No results matching \"{search}\". Press {key} to create a new one."
  cancel: "Cancel"
  ok: "Ok"
  add_filter: "Add Filter"

ko:
  labels:
    model: "모델"
    checkpoint: "체크포인트"
    threshold: "임계점"
    filter: "필터 설정 ({0})"
  hints:
    model: "객체 감지에 사용할 모델을 선택할 수 있습니다."
    checkpoint: "모델에 사용할 가중치의 체크포인트를 선택할 수 있습니다."
    threshold: "임계점 값이 클 수록, 보다 정확도가 높은 객체만 탐지합니다."
  title:
    filter: "필터 설정"
  subtitle:
    filter: "OCR 결과를 필터링 할 조건을 설정합니다."
  tools:
    clear: "영역 해제"
    selection: "영역 선택"
  no_matching: "\"{search}\" 와 일치하는 결과가 없습니다. {key} 키를 눌러 추가할 수 있습니다."
  cancel: "취소"
  ok: "확인"
  add_filter: "필터 추가"
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
            v-model="model"
            @change="onChangeModel"
            :items="models"
            :hint="$t('hints.model')"
        ></v-select>

        <p :class="subtitleClass">{{ $t('labels.checkpoint') }}</p>
        <v-select
            dense
            outlined
            persistent-hint
            disabled
            v-model="checkpoint"
            @change="onChangeCheckpoint"
            :items="checkpoints"
            :hint="$t('hints.checkpoint')"
        ></v-select>

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

        <v-btn width="100%" class="mt-4" @click="onClickFilter">
          <v-icon left>mdi-filter</v-icon>
          {{ $t('labels.filter', [filters.length]) }}
        </v-btn>
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
            :group="$route.params.group"
            :project="$route.params.project"
            :device="$route.params.device"
            :value="device"
            :event-config="value"
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

    <!-- Filter dialog. -->
    <v-dialog v-model="showFilterDialog" :max-width="dialogWidth">
      <v-card>
        <v-card-title>
          {{ $t('title.filter') }}
        </v-card-title>
        <v-card-subtitle>
          {{ $t('subtitle.filter') }}
        </v-card-subtitle>
        <v-divider></v-divider>

        <v-card-text>
          <v-sheet class="mt-4">
            <div
                v-for="n in filtersTemp.length"
                :key="`filter-${n}`"
                class="mb-2 d-flex flex-row justify-center"
            >
              <v-menu
                  left
                  bottom
                  offset-y
                  open-on-click
                  transition="slide-y-transition"
                  :close-on-content-click="true"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                      v-show="n >= 2"
                      class="mr-2"
                      rounded
                      v-bind="attrs"
                      v-on="on"
                  >
                    {{ n === 1 ? 'where' : filtersTemp[n-1]['logical'] }}
                  </v-btn>
                </template>
                <v-list dense>
                  <v-list-item @click="onClickLogicalAnd(n)">
                    <v-list-item-content>
                      <v-list-item-title>AND</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item @click="onClickLogicalOr(n)">
                    <v-list-item-content>
                      <v-list-item-title>OR</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>

              <v-menu
                  left
                  bottom
                  offset-y
                  open-on-click
                  transition="slide-y-transition"
                  :close-on-content-click="true"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                      class="mr-2"
                      rounded
                      v-bind="attrs"
                      v-on="on"
                  >
                    {{ filtersTemp[n-1]['operator'] }}
                  </v-btn>
                </template>
                <v-list dense>
                  <v-list-item @click="onClickOperatorEq(n)">
                    <v-list-item-content>
                      <v-list-item-title>&#61;</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item @click="onClickOperatorNe(n)">
                    <v-list-item-content>
                      <v-list-item-title>&#33;&#61;</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item @click="onClickOperatorLt(n)">
                    <v-list-item-content>
                      <v-list-item-title>&#60;</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item @click="onClickOperatorGt(n)">
                    <v-list-item-content>
                      <v-list-item-title>&#62;</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item @click="onClickOperatorLe(n)">
                    <v-list-item-content>
                      <v-list-item-title>&#60;&#61;</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item @click="onClickOperatorGe(n)">
                    <v-list-item-content>
                      <v-list-item-title>&#62;&#61;</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>

              <v-text-field
                  class="mr-2"
                  dense
                  outlined
                  rounded
                  hide-details
                  type="text"
                  autocomplete="off"
                  :value="filtersTemp[n-1]['value']"
                  @input="inputFiltersValue(n, $event)"
              ></v-text-field>
              <v-btn icon @click="onClickFilterRemove(n)">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
          </v-sheet>

          <div class="mt-4">
            <v-btn small rounded @click="onClickFilterAdd">
              <v-icon left>mdi-plus</v-icon>
              {{ $t('add_filter') }}
            </v-btn>
          </div>
        </v-card-text>

        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="onClickFilterCancel">
            {{ $t('cancel') }}
          </v-btn>
          <v-btn @click="onClickFilterOk">
            {{ $t('ok') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import {Component, Emit, Prop, Ref} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MediaPlayer from '@/media/MediaPlayer.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';
import type {
  VmsDeviceA,
  VmsEventConfigOcrFilterQ,
  VmsEventConfigOcrQ,
} from '@/packet/vms';
import * as _ from 'lodash';
import {valueToRatio, ratioToValue} from '@/math/ratio';

@Component({
  components: {
    MediaPlayer,
  }
})
export default class FormVmsEventConfigsOcr extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;

  @Prop({type: Number, default: 0})
  readonly minThreshold!: number;

  @Prop({type: Number, default: 100})
  readonly maxThreshold!: number;

  @Prop({type: Number, default: 50})
  readonly defaultThreshold!: number;

  @Prop({type: String, default: '60%'})
  readonly dialogWidth!: number;

  @Prop({type: Object, required: true})
  readonly device!: VmsDeviceA;

  @Prop({type: Object, required: true})
  readonly value!: VmsEventConfigOcrQ;

  @Prop({type: Boolean, required: true})
  readonly valid!: boolean;

  @Ref('media-player')
  readonly mediaPlayer!: MediaPlayer;

  loading = false;
  annotationMode = false;

  models = [] as Array<string>;
  model = ''

  checkpoints = [] as Array<string>;
  checkpoint = ''

  threshold = 0;

  showFilterDialog = false;
  filters = [] as Array<VmsEventConfigOcrFilterQ>;
  filtersTemp = [] as Array<VmsEventConfigOcrFilterQ>;

  mounted() {
    const defaultThreshold = valueToRatio(
        this.defaultThreshold, this.minThreshold, this.maxThreshold
    );

    this.value.model = this.value.model ?? '';
    this.value.checkpoint = this.value.checkpoint ?? '';
    this.value.threshold = this.value.threshold ?? defaultThreshold;
    this.value.filters = this.value.filters ?? [];
    this.value.x1 = this.value.x1 ?? 0;
    this.value.y1 = this.value.y1 ?? 0;
    this.value.x2 = this.value.x2 ?? 0;
    this.value.y2 = this.value.y2 ?? 0;

    this.model = this.value.model;
    this.checkpoint = this.value.checkpoint;
    this.threshold = ratioToValue(
        this.value.threshold, this.minThreshold, this.maxThreshold
    );
    this.filters = _.cloneDeep(this.value.filters);

    // TODO: deprecated
    const defaultModel = 'seven-segment';
    const defaultCheckpoint = 'seven_segment_20211028_adam.pth';
    this.models = [defaultModel];
    this.checkpoints = [defaultCheckpoint];
    this.value.model = defaultModel;
    this.value.checkpoint = defaultCheckpoint;
    this.model = defaultModel;
    this.checkpoint = defaultCheckpoint;

    this.requestEventOcr();
    this.updateValid();
  }

  get selectionButtonColor() {
    if (this.annotationMode) {
      return 'primary';
    } else {
      return '';
    }
  }

  requestEventOcr() {
    const group = this.$route.params.group;
    const project = this.$route.params.project;
    const device = this.$route.params.device;
    this.loading = true;
    this.$api2.postVmsDeviceProcessDebugEventOcr(group, project ,device, this.value)
        .then(() => {
          this.loading = false;
        })
        .catch(error => {
          this.loading = false;
          this.toastRequestFailure(error);
        })
  }

  @Emit('update:valid')
  updateValid() {
    return !!this.model && !!this.checkpoint && this.filters.length >= 1;
  }

  @Emit()
  input() {
    this.requestEventOcr();
    this.updateValid();
    return this.value;
  }

  onChangeModel(event: string) {
    this.value.model = event;
    this.input();
  }

  onChangeCheckpoint(event: string) {
    this.value.checkpoint = event;
    this.input();
  }

  onChangeThreshold(value: number) {
    this.value.threshold = valueToRatio(value, this.minThreshold, this.maxThreshold);
    this.input();
  }

  onClickFilter() {
    this.showFilterDialog = true;
    this.filtersTemp = _.cloneDeep(this.filters);
  }

  onClickFilterAdd() {
    const logical = this.filtersTemp.length === 0 ? '' : 'and';
    this.filtersTemp.push({
      logical: logical,
      operator: '=',
      value: 0,
    } as VmsEventConfigOcrFilterQ);
  }

  onClickLogicalAnd(number) {
    this.filtersTemp[number - 1].logical = 'and';
  }

  onClickLogicalOr(number) {
    this.filtersTemp[number - 1].logical = 'or';
  }

  onClickOperatorEq(number) {
    this.filtersTemp[number - 1].operator = '=';
  }

  onClickOperatorNe(number) {
    this.filtersTemp[number - 1].operator = '!=';
  }

  onClickOperatorLt(number) {
    this.filtersTemp[number - 1].operator = '<';
  }

  onClickOperatorGt(number) {
    this.filtersTemp[number - 1].operator = '>';
  }

  onClickOperatorLe(number) {
    this.filtersTemp[number - 1].operator = '<=';
  }

  onClickOperatorGe(number) {
    this.filtersTemp[number - 1].operator = '>=';
  }

  inputFiltersValue(number, event) {
    this.filtersTemp[number - 1].value = event;
  }

  onClickFilterRemove(number) {
    this.filtersTemp.splice(number - 1, 1);
  }

  onClickFilterCancel() {
    this.showFilterDialog = false;
    this.filtersTemp = [];
  }

  onClickFilterOk() {
    this.showFilterDialog = false;
    this.filters = this.filtersTemp;
    this.value.filters = this.filters;
    this.input();
  }

  onClickClear() {
    this.value.x1 = 0;
    this.value.y1 = 0;
    this.value.x2 = 0;
    this.value.y2 = 0;
    this.mediaPlayer.clearAnnotations();
    this.input();
  }

  onClickSelection() {
    this.annotationMode = !this.annotationMode;
  }

  onRoi(roi) {
    this.value.x1 = roi.x1 || 0;
    this.value.y1 = roi.y1 || 0;
    this.value.x2 = roi.x2 || 0;
    this.value.y2 = roi.y2 || 0;

    this.annotationMode = false;
    this.input();
  }
}
</script>
