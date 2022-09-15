<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <p :class="subtitleClass">
          자동 라벨링 및 결과 예측에 필요한 추론을 위해, 시각 프로그래밍과 연동합니다.
        </p>
      </v-col>

      <v-col cols="6">
        <p :class="titleClass">시작 람다</p>
        <v-select
          :items="['Button']"
          value="Button"
          label="시작 람다를 선택해 주세요"
        ></v-select>
        <p>추론을 시작할 경우 선택된 시각 프로그래밍의 람다 부터 실행됩니다.</p>
      </v-col>

      <v-col cols="6">
        <p :class="titleClass">출력 람다</p>
        <v-select
          :items="['Inference']"
          value="Inference"
          label="출력 람다를 선택해 주세요"
        ></v-select>
        <v-select
          :items="['image']"
          value="image"
          label="이미지를 출력하는 데이터 슬롯을 선택해 주세요"
        ></v-select>
        <v-select
          :items="['annotations']"
          value="annotations"
          label="추론 결과를 출력하는 데이터 슬롯을 선택해 주세요"
        ></v-select>
        <p>
          실행된 추론 프로세스가 완료될 경우 선택된 람다의 슬롯으로 부터 데이터를
          추출합니다.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import LeftTitle from '@/components/LeftTitle.vue';
import {TITLE_CLASS} from '@/styles/title';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

@Component({
  components: {
    LeftTitle,
  },
})
export default class MainMachineLearning extends VueBase {
  private readonly titleClass = TITLE_CLASS;
  private readonly subtitleClass = SUBTITLE_CLASS;
}
</script>
