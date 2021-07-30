<template>
  <v-app>
    <main-title-bar>
    </main-title-bar>

    <v-main>
      <router-view>
      </router-view>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { Component } from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import MainTitleBar from '@/components/MainTitleBar.vue';

@Component({
  components: {
    MainTitleBar,
  }
})
export default class MainPage extends VueBase {
  mounted() {
    this.moveTo(this.paths.mainProjects);
  }
}
</script>
