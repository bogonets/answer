<template>
  <div class="router-navi-main">
    <navi-skeleton v-if="loading">
    </navi-skeleton>
    <navi-main-airjoy v-else-if="isAirjoy">
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
import NaviMain from "@/pages/navigation/NaviMain.vue";
import NaviMainAirjoy from "@/pages/navigation/NaviMainAirjoy.vue";
import {OEM_AIRJOY} from "@/packet/oem";
import NaviSkeleton from "@/pages/navigation/NaviSkeleton.vue";

@Component({
  components: {
    NaviSkeleton,
    NaviMainAirjoy,
    NaviMain,
    BarMain,
  }
})
export default class RouterNaviMain extends VueBase {
  loading = false;
  oem = '';

  get isAirjoy() {
    return this.oem === OEM_AIRJOY;
  }

  created() {
    this.requestOem()
  }

  requestOem() {
    this.loading = true;
    this.$api2.getMainInfosOem()
        .then(info => {
          this.oem = info.value || '';
          this.loading = false;
        })
        .catch(error => {
          this.oem = '';
          this.loading = false;
          this.toastRequestFailure(error);
        });
  }
}
</script>

<style lang="scss" scoped>
.router-navi-main {
}
</style>
