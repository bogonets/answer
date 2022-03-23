<i18n lang="yaml">
en:
  kanban: "Kanban"

ko:
  kanban: "간반보드"
</i18n>

<template>
  <v-container>
    <breadcrumb-main name="Kanban"></breadcrumb-main>
    <v-divider></v-divider>

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
export default class MainKanban extends VueBase {

  loading = false;

  created() {
  }
}
</script>
