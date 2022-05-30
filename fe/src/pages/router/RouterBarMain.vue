<template>
  <div class="router-bar-main">
    <bar-main v-if="!$localStore.barHide || !isAirjoySummery"></bar-main>

    <v-main>
      <router-view>
      </router-view>
    </v-main>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BarMain from '@/pages/bar/BarMain.vue';
import mainNames from '@/router/names/main';

@Component({
  components: {
    BarMain,
  }
})
export default class RouterBarMain extends VueBase {
  get isAirjoySummery() {
    return this.$route.name === mainNames.mainAirjoySummary;
  }
}
</script>

<style lang="scss" scoped>
.router-bar-main {
}
</style>
