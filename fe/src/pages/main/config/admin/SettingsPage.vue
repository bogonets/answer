<i18n lang="yaml">
en:
  title: "Settings"
  subtitle: "Modify environment variables used in the system."

ko:
  title: "환경설정"
  subtitle: "시스템에서 사용되는 환경변수를 수정합니다."
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
export default class SettingsPage extends VueBase {
}
</script>
