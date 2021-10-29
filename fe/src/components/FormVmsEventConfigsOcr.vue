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
            :value="checkpoint"
            @input="inputCheckpoint"
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
            hover-system-bar
            :value="device"
            :group="$route.params.group"
            :project="$route.params.project"
            :device="Number.parseInt($route.params.device)"
        ></media-player>
        <div class="mt-2 d-flex justify-end">
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
                v-for="i in filters.length"
                :key="`filter-${i}`"
                class="mb-2 d-flex flex-row justify-center"
            >
              <v-btn class="mr-2" :disabled="i === 1" rounded>
                {{ i === 1 ? 'where' : filters[i-1]['logical'] }}
              </v-btn>
              <v-btn class="mr-2" rounded>
                {{ filters[i-1]['operator'] }}
              </v-btn>
              <v-text-field
                  class="mr-2"
                  dense
                  outlined
                  rounded
                  hide-details
                  type="text"
                  autocomplete="off"
                  :value="filters[i-1]['value']"
                  @input="inputFiltersValue"
              ></v-text-field>
              <v-btn icon>
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
import {Component, Emit, Prop} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MediaPlayer from '@/media/MediaPlayer.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from "@/styles/caption";
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
export default class FormVmsEventConfigsOcr extends VueBase {
  readonly subtitleClass = SUBTITLE_CLASS;
  readonly captionClass = CAPTION_CLASS;

  readonly minThreshold = 0;
  readonly maxThreshold = 100;

  @Prop({type: Object, default: createEmptyObject})
  readonly value!: any;

  loading = false;
  device = {} as VmsDeviceA;

  model = '';
  models = [] as Array<string>;

  checkpoint = '';
  checkpoints = [] as Array<string>;

  labels = [] as Array<string>;
  searchLabel = '';

  threshold = 50;

  showFilterDialog = false;
  filters = [] as Array<object>;

  create() {
    this.requestModels();
  }

  requestModels() {
  }

  get dialogWidth() {
    return "60%";
  }

  onClickFilter() {
    this.showFilterDialog = true;
  }

  onClickFilterAdd() {
    this.filters.push({});
  }

  inputFiltersValue(event) {
  }

  onClickFilterCancel() {
    this.showFilterDialog = false;
  }

  onClickFilterOk() {
  }

  inputModel(event) {
  }

  inputCheckpoint(event) {
  }

  inputLabel(event) {
  }

  @Emit()
  input() {
    return this.value;
  }
}
</script>
