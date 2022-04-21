<i18n lang="yaml">
en:
  title: 'Answer'
  version: 'Version'
  documentation: 'Official documentation'
  vender: 'Bogonet Homepage'
  label:
    codename: 'Enter the codename'
  msg:
    enable_dev_mode: 'Developer mode is enabled'
    disable_dev_mode: 'Developer mode is disabled'

ko:
  title: 'Answer'
  version: '버전'
  documentation: '공식 문서 페이지'
  vender: '보고넷 홈페이지'
  label:
    codename: '코드명을 입력하세요'
  msg:
    enable_dev_mode: '개발자 모드가 활성화 되었습니다'
    disable_dev_mode: '개발자 모드가 비활성화 되었습니다'
</i18n>

<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="8" sm="6" md="6" lg="6" xl="4">
        <div class="d-block my-16" @click="onClickLogo">
          <title-logo :max-width="300" :max-height="300"></title-logo>
        </div>

        <v-divider></v-divider>

        <v-btn block text rounded disabled class="d-block my-8">
          {{ versionText }}
        </v-btn>

        <v-btn
          block
          text
          rounded
          class="d-block my-4 secondary"
          @click="onClickDocumentation"
        >
          {{ $t('documentation') }}
        </v-btn>

        <v-btn block text rounded class="d-block my-4 secondary" @click="onClickVender">
          {{ $t('vender') }}
        </v-btn>

        <v-text-field
          v-if="showCodenameInput"
          outlined
          type="password"
          v-model="codename"
          :label="$t('label.codename')"
          @keypress.enter.stop="submitCodename"
        ></v-text-field>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import TitleLogo from '@/components/TitleLogo.vue';
import {encryptSha256} from '@/crypto/sha';

const DOCUMENTATION_HREF = 'https://answerdoc.bogonets.com';
const VENDER_HREF = 'https://www.bogonets.com';

const MAX_CLICK_COUNT = 20;

@Component({
  components: {
    TitleLogo,
  },
})
export default class RootAbout extends VueBase {
  logoClicker = 0;
  showCodenameInput = false;
  codename = '';

  get versionText(): string {
    const title = this.$t('title').toString();
    const version = this.$t('version').toString();
    const number = this.$versions.answer;
    return `${title} ${version} ${number}`;
  }

  mounted() {
    this.logoClicker = 0;
    this.showCodenameInput = false;
  }

  onClickLogo() {
    this.logoClicker++;
    if (this.logoClicker >= MAX_CLICK_COUNT) {
      this.showCodenameInput = true;
    }
  }

  submitCodename() {
    switch (encryptSha256(this.codename)) {
      case 'a71da3fe88d07bbd86cf296c6759fb2198451d58fc0707fecba0eeaf17982a83':
        if (this.$localStore.devEnable) {
          this.$localStore.devEnable = false;
          this.toastWarning(this.$t('msg.disable_dev_mode'));
        } else {
          this.$localStore.devEnable = true;
          this.toastInfo(this.$t('msg.enable_dev_mode'));
        }
        break;
      default:
        break;
    }
    this.codename = '';
  }

  onClickDocumentation() {
    window.open(DOCUMENTATION_HREF);
  }

  onClickVender() {
    window.open(VENDER_HREF);
  }
}
</script>
