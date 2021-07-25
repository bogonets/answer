<i18n lang="yaml">
en:
  title: "User Management"
  subtitle: "You can add, edit and remove users."

ko:
  title: "사용자 관리"
  subtitle: "사용자를 추가하거나 편집 및 제거할 수 있습니다."
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
export default class UsersPage extends VueBase {
}
</script>
