<template>
  <v-container>
    <breadcrumb-main name="Dashboard"></breadcrumb-main>
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
export default class MainDashboard extends VueBase {
}
</script>
