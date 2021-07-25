<i18n lang="yaml">
en:
  title: "Groups"
  subtitle: "By creating independent teams, you can create sub-projects."

ko:
  title: "그룹 관리"
  subtitle: "독립적인 팀을 만들어 하위 프로젝트를 만들 수 있습니다."
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
export default class GroupsPage extends VueBase {
}
</script>
