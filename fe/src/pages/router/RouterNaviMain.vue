<template>
  <div>
    <navi-main>
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

@Component({
  components: {
    BarMain,
    NaviMain,
  }
})
export default class RouterNaviMain extends VueBase {
}
</script>
