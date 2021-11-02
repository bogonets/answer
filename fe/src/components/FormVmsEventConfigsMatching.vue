<i18n lang="yaml">
en:
  labels:
    sensitive: "Sensitive"
    train_image: "Train Image"
    query_image: "Query Image"
  hints:
    sensitive: >
      The higher the sensitivity value, the more exact the similarity must be.
  tools:
    snapshot: "Snapshot"
    clear: "Clear selection"
    selection: "Selection"
    copy: "Copy"

ko:
  labels:
    sensitive: "민감도"
    train_image: "기준 이미지"
    query_image: "비교 대상"
  hints:
    sensitive: "민감도 값이 클 수록, 유사도가 정확히 일치해야 합니다."
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
        <v-img>
        </v-img>
        <div class="mt-2 d-flex justify-start">
          <v-btn small rounded class="mr-2">
            <v-icon left>mdi-close</v-icon>
            {{ $t('tools.clear') }}
          </v-btn>
          <v-btn small rounded class="mr-2">
            <v-icon left>mdi-selection-drag</v-icon>
            {{ $t('tools.selection') }}
          </v-btn>
          <v-btn small rounded>
            <v-icon left>mdi-vector-selection</v-icon>
            {{ $t('tools.copy') }}
          </v-btn>
        </div>

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
          sm="6"
          md="6"
          lg="6"
          xl="6"
      >
        <p :class="subtitleClass">{{ $t('labels.query_image') }}</p>
        <media-player
            hover-system-bar
            :value="device"
            :group="$route.params.group"
            :project="$route.params.project"
            :device="Number.parseInt($route.params.device)"
        ></media-player>
        <div class="mt-2 d-flex justify-end">
          <v-btn small rounded class="mr-2">
            <v-icon left>mdi-camera</v-icon>
            {{ $t('tools.snapshot') }}
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
import {CAPTION_CLASS} from "@/styles/caption";
import type {VmsDeviceA} from '@/packet/vms';

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

  readonly minSensitive = 0;
  readonly maxSensitive = 100;

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

  sensitive = 50;

  create() {
    this.requestModels();
  }

  requestModels() {
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
