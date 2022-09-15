<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <p :class="subtitleClass">라벨링 지침</p>

        <left-title
          x-small
          no-gutter
          no-wrap-xs
          :left-ratio="8"
          :right-ratio="4"
          header="라벨링 전에 표시"
          subheader="라벨링 작업에 도움이 되는 지침"
        >
          <div class="d-flex flex-row justify-end">
            <v-switch inset></v-switch>
          </div>
        </left-title>

        <v-textarea
          dense
          auto-grow
          persistent-hint
          label="Instruction Text"
          placeholder="Please enter the instruction text"
          value="작업전, 꼭 오늘의 일정을 확인해 주세요!!"
        ></v-textarea>

        <v-btn color="primary">Submit</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import LeftTitle from '@/components/LeftTitle.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';

@Component({
  components: {
    LeftTitle,
  },
})
export default class MainInstructions extends VueBase {
  private readonly subtitleClass = SUBTITLE_CLASS;
}
</script>
