<template>
  <div>
    <navi-dev>
    </navi-dev>

    <router-view>
    </router-view>
  </div>
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
export default class RouterNaviDev extends VueBase {
}
</script>
