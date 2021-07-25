<i18n lang="yaml">
en:
  title: "Features"
  subtitle: "Add or remove extensible features."

ko:
  title: "기능 관리"
  subtitle: "확장 가능한 기능을 추가하거나 제거합니다."
</i18n>

<template>
  <v-container>
    <app-bar-title
        flat
        :title="$t('title')"
        :subtitle="$t('subtitle')"
    ></app-bar-title>

  </v-container>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import AppBarTitle from "@/components/AppBarTitle.vue";

@Component({
  components: {
    AppBarTitle
  }
})
export default class FeaturesPage extends VueBase {
}
</script>
