<i18n lang="yaml">
en:
  vp: "VP"

ko:
  vp: "VP"
</i18n>

<template>
  <v-container>
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
export default class MainVisualProgramming extends VueBase {
}
</script>
