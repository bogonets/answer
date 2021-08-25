<template>
  <div>
    <navi-self>
    </navi-self>

    <router-view>
    </router-view>
  </div>
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
export default class RouterNaviSelf extends VueBase {
}
</script>
