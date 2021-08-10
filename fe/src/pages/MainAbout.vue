<i18n lang="yaml">
en:
  title: "Answer"
  version: "Version"
  documentation: "Official documentation"
  vender: "Bogonet Homepage"

ko:
  title: "Answer"
  version: "버전"
  documentation: "공식 문서 페이지"
  vender: "보고넷 홈페이지"
</i18n>

<template>
  <v-container class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="8" sm="6" md="6" lg="6" xl="4">

        <div class="d-block mb-16">
          <title-logo
              max-width="300px"
              max-height="300px"
          ></title-logo>
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

        <v-btn
            block
            text
            rounded
            class="d-block my-4 secondary" @click="onClickVender"
        >
          {{ $t('vender') }}
        </v-btn>

      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import TitleLogo from '@/components/TitleLogo.vue';

const DOCUMENTATION_HREF = 'https://answerdoc.bogonets.com';
const VENDER_HREF = 'https://www.bogonets.com';

@Component({
  components: {
    TitleLogo,
  }
})
export default class MainAbout extends VueBase {
  get versionText(): string {
    const title = this.$t('title').toString();
    const version = this.$t('version').toString();
    const number = this.$versions.answer;
    return `${title} ${version} ${number}`;
  }

  onClickDocumentation() {
    window.open(DOCUMENTATION_HREF);
  }

  onClickVender() {
    window.open(VENDER_HREF);
  }
}
</script>
