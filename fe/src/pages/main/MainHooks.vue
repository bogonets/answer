<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <p :class="subtitleClass">
          웹훅을 사용하면 특정 이벤트가 발생할 때 외부 서비스에 알림을 보낼 수 있습니다.
          <br />
          지정된 이벤트가 발생하면 사용자가 제공한 URL로 POST 요청이 전송됩니다.
        </p>
      </v-col>

      <v-col cols="12" class="px-6">
        <p :class="subtitleClass">Payload URL</p>
        <v-text-field
          dense
          persistent-hint
          hint="이벤트를 보낼 원격지 주소"
        ></v-text-field>
      </v-col>

      <v-col cols="12">
        <left-title
          x-small
          no-gutter
          no-wrap-xs
          :left-ratio="8"
          :right-ratio="4"
          header="Active"
          subheader="활성화되면 웹훅 기능을 사용합니다"
        >
          <div class="d-flex flex-row justify-end">
            <v-switch inset></v-switch>
          </div>
        </left-title>

        <left-title
          x-small
          no-gutter
          no-wrap-xs
          :left-ratio="8"
          :right-ratio="4"
          header="Send Payload"
          subheader="활성화되면 이벤트와 함께 데이터도 전송됩니다"
        >
          <div class="d-flex flex-row justify-end">
            <v-switch inset></v-switch>
          </div>
        </left-title>
      </v-col>

      <v-col cols="12" class="pl-7">
        <p :class="subtitleClass">사용할 이벤트 목록</p>
        <v-switch hide-details dense inset label="Project updated"></v-switch>
        <v-switch hide-details dense inset label="Task created"></v-switch>
        <v-switch hide-details dense inset label="Task start"></v-switch>
        <v-switch hide-details dense inset label="Task end"></v-switch>
        <v-switch hide-details dense inset label="Task deleted"></v-switch>
        <v-switch hide-details dense inset label="Annotation created"></v-switch>
        <v-switch hide-details dense inset label="Annotation updated"></v-switch>
        <v-switch hide-details dense inset label="Annotation deleted"></v-switch>
        <v-switch hide-details dense inset label="Category created"></v-switch>
        <v-switch hide-details dense inset label="Category updated"></v-switch>
        <v-switch hide-details dense inset label="Category deleted"></v-switch>
      </v-col>
    </v-row>

    <v-row class="mt-2" no-gutters>
      <v-spacer></v-spacer>
      <v-btn class="mr-2">Cancel</v-btn>
      <v-btn color="primary">Submit</v-btn>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import LeftTitle from '@/components/LeftTitle.vue';
import {SUBTITLE_CLASS} from '@/styles/subtitle';
import {TITLE_CLASS} from '@/styles/title';

@Component({
  components: {
    LeftTitle,
  },
})
export default class MainStorage extends VueBase {
  private readonly titleClass = TITLE_CLASS;
  private readonly subtitleClass = SUBTITLE_CLASS;
}
</script>
