<template>
  <div class="router-navi-main">
    <navi-main-airjoy v-if="isAirjoy">
    </navi-main-airjoy>
    <navi-main v-else>
    </navi-main>

    <router-view>
    </router-view>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BarMain from '@/pages/bar/BarMain.vue';
import NaviMain from '@/pages/navigation/NaviMain.vue';
import NaviMainAirjoy from '@/pages/navigation/airjoy/NaviMainAirjoy.vue';
import {OEM_AIRJOY} from '@/packet/oem';

@Component({
  components: {
    NaviMainAirjoy,
    NaviMain,
    BarMain,
  }
})
export default class RouterNaviMain extends VueBase {
  get oem() {
    return this.$localStore.preference.oem;
  }

  get isAirjoy() {
    return this.oem === OEM_AIRJOY;
  }
}
</script>

<style lang="scss" scoped>
.router-navi-main {
}
</style>
