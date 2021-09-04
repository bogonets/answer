<template>
  <div class="router-navi-admin">
    <navi-admin>
    </navi-admin>

    <router-view>
    </router-view>
  </div>
</template>

<script lang="ts">
import {Component} from 'vue-property-decorator';
import VueBase from '@/base/VueBase';
import BarMain from '@/pages/bar/BarMain.vue';
import NaviAdmin from '@/pages/navigation/NaviAdmin.vue';

@Component({
  components: {
    BarMain,
    NaviAdmin,
  }
})
export default class RouterNaviAdmin extends VueBase {
}
</script>

<style lang="scss" scoped>
.router-navi-admin {
}
</style>
