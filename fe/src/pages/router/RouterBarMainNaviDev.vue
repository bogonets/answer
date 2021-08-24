<template>
  <v-app>
    <bar-main>
    </bar-main>

    <v-main>
      <navi-dev>
      </navi-dev>

      <router-view>
      </router-view>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BarMain from '@/pages/bar/BarMain.vue';
import NaviDev from '@/pages/navigation/NaviDev.vue';

@Component({
  components: {
    BarMain,
    NaviDev,
  }
})
export default class RouterBarMainNaviDev extends VueBase {
}
</script>
