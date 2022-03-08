<i18n lang="yaml">
en:
  labels:
    create_env: "Create a new environment"
  msg:
    no_env: "The environment is not ready for the daemon."

ko:
  labels:
    create_env: "새로운 환경 생성"
  msg:
    no_env: "데몬을 사용할 준비가 되지 않았습니다."
</i18n>

<template>
  <div>
    <div v-if="ready">
    </div>
    <div v-else class="ma-4 d-flex flex-column align-center">
      <v-icon size="160">mdi-package-variant-closed</v-icon>
      <span class="my-8 text-body-1 text--secondary">
        {{ $t('msg.no_env') }}
      </span>
      <v-btn
          class="d-block my-4 px-10 secondary"
          text
          rounded
          @click="onClickCreateEnv"
      >
        {{ $t('labels.create_env') }}
      </v-btn>
    </div>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import TitleLogo from '@/components/TitleLogo.vue';

@Component({
  components: {
    TitleLogo,
  }
})
export default class AdminDaemonsEditEnv extends VueBase {

  ready = false;

  created() {
  }

  createEnv() {
  }

  onClickLogo() {
    this.createEnv();
  }

  onClickCreateEnv() {
    this.createEnv();
  }
}
</script>
