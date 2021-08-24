<template>
  <v-app>
    <bar-main>
    </bar-main>

    <v-main>
      <navi-self>
      </navi-self>

      <router-view>
      </router-view>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BarMain from '@/pages/bar/BarMain.vue';
import NaviSelf from '@/pages/navigation/NaviSelf.vue';

@Component({
  components: {
    BarMain,
    NaviSelf,
  }
})
export default class RouterBarMainNaviSelf extends VueBase {
}
</script>
