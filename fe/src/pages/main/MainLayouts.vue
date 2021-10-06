<i18n lang="yaml">
en:
  empty: "Empty layouts"

ko:
  empty: "레이아웃이 존재하지 않습니다"
</i18n>

<template>
  <v-container>
    <breadcrumb-main name="Layouts"></breadcrumb-main>
    <v-divider></v-divider>

    <v-card>
      <v-card-subtitle>
        {{ $t('empty') }}
      </v-card-subtitle>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BreadcrumbMain from '@/pages/breadcrumb/BreadcrumbMain.vue';

@Component({
  components: {
    BreadcrumbMain,
  }
})
export default class MainLayouts extends VueBase {
}
</script>
