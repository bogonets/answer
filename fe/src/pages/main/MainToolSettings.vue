<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <p :class="subtitleClass">
          라벨링에 필요한 도구를 드래그 앤 드롭 하여 추가 및 삭제할 수 있습니다.
        </p>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-card>
          <v-toolbar dense flat>
            <v-btn plain x-small>
              <v-icon small>mdi-cursor-default</v-icon>
            </v-btn>

            <v-btn plain x-small>
              <v-icon small>mdi-cursor-move</v-icon>
            </v-btn>

            <v-btn plain x-small>
              <v-icon small>mdi-magnify-plus</v-icon>
            </v-btn>

            <v-btn plain x-small>
              <v-icon small>mdi-magnify-minus</v-icon>
            </v-btn>

            <v-divider class="mx-3" vertical></v-divider>
          </v-toolbar>
        </v-card>
      </v-col>

      <v-col cols="12">
        <span :class="subtitleClass">Common Tools</span>
      </v-col>

      <v-col cols="12">
        <v-btn plain large>
          <div class="d-flex flex-column">
            <v-icon>mdi-border-vertical</v-icon>
            <span class="mt-1">세로 분할 선</span>
          </div>
        </v-btn>

        <v-btn plain large>
          <div class="d-flex flex-column">
            <v-icon>mdi-undo</v-icon>
            <span class="mt-1">되돌리기</span>
          </div>
        </v-btn>

        <v-btn plain large>
          <div class="d-flex flex-column">
            <v-icon>mdi-redo</v-icon>
            <span class="mt-1">되돌리기 취소</span>
          </div>
        </v-btn>
      </v-col>

      <v-col cols="12">
        <v-divider class="mb-4"></v-divider>
        <span :class="subtitleClass">Image Annotation</span>
      </v-col>

      <v-col cols="12">
        <v-btn plain large>
          <div class="d-flex flex-column">
            <v-icon>mdi-vector-polyline</v-icon>
            <span class="mt-1">선 그리기</span>
          </div>
        </v-btn>

        <v-btn plain large>
          <div class="d-flex flex-column">
            <v-icon>mdi-vector-polygon</v-icon>
            <span class="mt-1">면 그리기</span>
          </div>
        </v-btn>

        <v-btn plain large>
          <div class="d-flex flex-column">
            <v-icon>mdi-vector-ellipse</v-icon>
            <span class="mt-1">원 그리기</span>
          </div>
        </v-btn>
      </v-col>

      <v-col cols="12">
        <v-divider class="mb-4"></v-divider>
        <span :class="subtitleClass">Machine Learning</span>
      </v-col>

      <v-col cols="12">
        <v-btn plain large>
          <div class="d-flex flex-column">
            <v-icon>mdi-image-search</v-icon>
            <span class="mt-1">추론</span>
          </div>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import {TITLE_CLASS} from '@/styles/title';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {CAPTION_CLASS} from '@/styles/caption';

@Component
export default class MainToolSettings extends VueBase {
  private readonly titleClass = TITLE_CLASS;
  private readonly subtitleClass = SUBTITLE_CLASS;
  private readonly captionClass = CAPTION_CLASS;
}
</script>
