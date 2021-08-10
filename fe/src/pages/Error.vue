<i18n lang="yaml">
en:
  title: "404 Error"
  message: "Not found page"
  back: "Back"

ko:
  title: "404 에러"
  message: "페이지를 찾을 수 없습니다"
  back: "뒤로 가기"
</i18n>

<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-card>
        <v-card-title class="text-center">
          <span>{{ $t('title') }}</span>
        </v-card-title>

        <v-card-text class="text-center">
          <span>{{ $t('message') }}</span>
        </v-card-text>

        <v-card-actions>
          <v-btn
              block
              small
              color="success"
              @click="onClickBack"
          >
            {{ $t('back') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from "@/base/VueBase";

@Component
export default class Error extends VueBase {
  onClickBack() {
    this.$router.back();
  }
}
</script>
