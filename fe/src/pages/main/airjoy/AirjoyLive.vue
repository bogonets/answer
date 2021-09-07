<template>
  <v-container>
    <breadcrumb-main name="Live"></breadcrumb-main>
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
export default class AirjoyLive extends VueBase {
}
</script>
