<i18n lang="yaml">
en:
  title: "Overview"
  subtitle: "Prints a summary of the system status."

ko:
  title: "개요"
  subtitle: "시스템의 상태를 요약하여 출력합니다."
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
export default class OverviewPage extends VueBase {
}
</script>
