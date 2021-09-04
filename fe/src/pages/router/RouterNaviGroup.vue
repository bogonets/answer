<template>
  <div class="router-navi-group">
    <navi-group>
    </navi-group>

    <router-view>
    </router-view>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BarMain from '@/pages/bar/BarMain.vue';
import NaviGroup from "@/pages/navigation/NaviGroup.vue";

@Component({
  components: {
    BarMain,
    NaviGroup,
  }
})
export default class RouterNaviGroup extends VueBase {
}
</script>

<style lang="scss" scoped>
.router-navi-group {
}
</style>
