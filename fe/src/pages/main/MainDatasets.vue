<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <p :class="subtitleClass">데이터셋을 지정하고 원하는 포맷으로 추출합니다.</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="auto">
        <card-button class="px-4" height="240px">
          <v-icon large>mdi-fire</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap mt-2">
            화재 데이터셋
          </span>
          <p class="text--secondary text-caption mt-2">
            전체: 100
            <br />
            완료: 90
            <br />
            미완: 6
            <br />
            취소: 4
            <br />
            범주: 2
          </p>
          <v-progress-linear color="green" value="90"></v-progress-linear>
        </card-button>
      </v-col>

      <v-col cols="auto">
        <card-button class="px-4" height="240px">
          <v-icon large>mdi-car</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap mt-2">
            차량 데이터셋
          </span>
          <p class="text--secondary text-caption mt-2">동기화 중 ...</p>
          <v-progress-linear indeterminate color="warning"></v-progress-linear>
        </card-button>
      </v-col>

      <v-col cols="auto">
        <card-button class="px-4" height="240px">
          <span class="text--secondary text-h6 font-weight-bold text-no-wrap">
            COCO
          </span>
          <span class="text--secondary text-subtitle-2 text-no-wrap mt-2">
            COCO 데이터셋
          </span>
          <p class="text--secondary text-caption mt-2">
            전체: 1913
            <br />
            완료: 1913
            <br />
            미완: 0
            <br />
            취소: 0
            <br />
            범주: 91
          </p>
          <v-progress-linear value="100"></v-progress-linear>
        </card-button>
      </v-col>

      <v-col cols="auto">
        <card-button class="px-4" height="240px">
          <v-icon large>mdi-plus</v-icon>
          <span class="text--secondary text-subtitle-2 text-no-wrap mt-2">
            데이터셋 추가
          </span>
        </card-button>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import CardButton from '@/components/CardButton.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

@Component({
  components: {
    CardButton,
  },
})
export default class MainDatasets extends VueBase {
  private readonly subtitleClass = SUBTITLE_CLASS;
}
</script>
